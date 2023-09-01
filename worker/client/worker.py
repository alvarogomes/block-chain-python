import requests
import json
import asyncio
import websockets
from blockchain import SimpleBlockchain
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=False)


class Worker:
    def __init__(self, server_address='http://localhost:18000'):
        self.id = None
        self.blockchain = SimpleBlockchain()
        self.server_address = server_address
        self.worker_id = None
        self.leader_id = None
        self.session = None
        self.connected_nodes = []
        asyncio.get_event_loop().run_until_complete(
            self.listen(server_address.replace('http', 'ws')))

    def register(self):
        response = requests.post(f"{self.server_address}/register/")
        if response.status_code == 200:
            self.id = response.json()["worker_id"]
        return response.json()

    def get_id(self):
        return self.id

    def add_transaction(self, transaction_data):
        self.blockchain.new_transaction(transaction_data)
        self.broadcast_new_transaction(transaction_data)

    async def broadcast_new_transaction(self, transaction):
        message = json.dumps({
            'type': 'new_transaction',
            'transaction': transaction
        })
        await self.broadcast_message(message)

    async def broadcast_new_block(self, new_block):
        message = json.dumps({
            'type': 'new_block',
            'block': new_block
        })
        await self.broadcast_message(message)

    async def broadcast_message(self, message):
        if self.connected_nodes:
            tasks = []
            for node in self.connected_nodes:
                task = websockets.connect(node)
                tasks.append(task)

            connections = await asyncio.gather(*tasks)
            for connection in connections:
                await connection.send(message)
                connection.close()

    def mine_block(self):
        # Recuperar as informações do último bloco na cadeia
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']

        # Encontrar um novo "proof" usando o algoritmo de Proof of Work
        proof = self.blockchain.proof_of_work(last_proof)

        # Receber recompensa por encontrar o proof.
        # O remetente é "0" para significar que este nó encontrou uma nova moeda.
        self.blockchain.new_transaction({
            'sender': "0",
            'recipient': self.worker_id,
            'amount': 1,
        })

        # Adicionar o novo bloco à cadeia
        previous_hash = self.blockchain.hash(last_block)
        new_block = self.blockchain.new_block(proof, previous_hash)

        # Transmite o novo bloco para outros nós
        asyncio.run(self.broadcast_new_block(new_block))

        return new_block

    def get_chain(self):
        # Retorna a cadeia de blocos atual
        return self.blockchain.chain

    def connect_db(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def dump_data(self):
        if hasattr(self, 'session'):
            for block in self.blockchain.chain:
                for transaction in block['transactions']:
                    new_transaction = Transaction(data=transaction)
                    self.session.add(new_transaction)
            self.session.commit()
        else:
            print("DB not connected. Use connect_db first.")

    def stop_dump_data(self):
        self.session = None

    async def listen(self, uri):
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                await self.on_message(message)

    def on_message(self, message):
        # Atualize a blockchain com base na mensagem recebida
        data = json.loads(message)
        if "transaction" in data:
            self.blockchain.new_transaction(data["transaction"])
            if hasattr(self, 'session'):
                new_transaction = Transaction(data=data["transaction"])
                self.session.add(new_transaction)
                self.session.commit()
