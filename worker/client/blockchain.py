import hashlib
import json
from time import time
from typing import List, Dict, Any


class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof: int, previous_hash: str = None) -> Dict[str, Any]:
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, transaction: Dict[str, Any]) -> int:
        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Dict[str, Any]:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def merkle_tree_root(self, transactions: List[Dict[str, Any]]) -> str:
        if not transactions:
            return ''

        hashes = [hashlib.sha256(json.dumps(
            tx, sort_keys=True).encode()).hexdigest() for tx in transactions]

        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])

            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined_hash = hashes[i] + hashes[i+1]
                new_hashes.append(hashlib.sha256(
                    combined_hash.encode()).hexdigest())

            hashes = new_hashes

        return hashes[0]
