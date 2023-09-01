# Projeto Block-Chain-Python

## Objetivos

Este projeto tem como objetivo criar uma infraestrutura de blockchain distribuída. A arquitetura é composta por um servidor central e múltiplos workers que mantêm réplicas da blockchain. Os workers podem registrar transações, verificar a consistência dos dados e até mesmo despejar dados em um banco de dados PostgreSQL.

## Lógica do Blockchain

### O que é o Blockchain?

Blockchain é uma estrutura de dados composta por uma lista encadeada de blocos. Cada bloco contém um conjunto de transações e o hash do bloco anterior, formando assim uma "corrente" imutável de registros. O primeiro bloco da lista é o bloco gênese, que é o único bloco que não tem um bloco anterior.

### Como a Blockchain está implementada neste projeto?

#### Estrutura dos Blocos e Cadeia

Cada bloco contém:

- O índice do bloco.
- O tempo em que o bloco foi criado.
- Um conjunto de transações.
- O hash do bloco anterior.
- Um "nonce" que é usado no algoritmo de Prova de Trabalho (Proof of Work) ou Prova de Participação (Proof of Stake).
- Uma Árvore de Merkle para resumir e verificar a integridade das transações no bloco.

A classe `Blockchain` no arquivo `blockchain.py` é a principal responsável pela lógica da blockchain. Ela contém uma lista `chain` que armazena todos os blocos da blockchain.

#### Transações e Mempool

As transações são armazenadas em uma área temporária chamada "mempool" até serem incluídas em um novo bloco durante o processo de mineração.

#### Mineração e Consenso

O método `mine_block()` em `worker.py` é responsável por criar um novo bloco, incluindo transações do mempool, e adicioná-lo à blockchain. Além disso, ele utiliza um algoritmo de consenso (Prova de Trabalho ou Prova de Participação) para validar o novo bloco.

O método `broadcast_new_block` é usado para enviar o novo bloco para todos os outros workers, garantindo que todas as cópias da blockchain sejam atualizadas e mantenham a consistência.

#### Sincronização

Cada worker tem uma cópia da blockchain. Os métodos `check_consistency()` e `broadcast_new_transaction()` garantem que todas as cópias sejam mantidas sincronizadas. Se uma transação ou um novo bloco é adicionado por qualquer worker, a atualização é propagada para todos os outros workers.

#### Árvore de Merkle

Cada bloco usa uma Árvore de Merkle para resumir todas as transações que ele contém. Isso fornece uma maneira eficiente e segura de verificar a integridade das transações.

#### Worker Líder

Um dos workers é eleito como "líder" pelo servidor. O líder tem responsabilidades adicionais, como a finalização da mineração de um bloco ou a tomada de decisões em caso de inconsistências na rede.

#### Armazenamento de Dados

O método `dump_data()` permite que os dados da blockchain sejam armazenados em um banco de dados PostgreSQL, proporcionando uma maneira mais robusta e permanente de manter registros.

Dessa forma, este projeto oferece uma implementação completa e distribuída de uma blockchain, incluindo todos os aspectos fundamentais como transações, consenso, e armazenamento de dados.

## Como o projeto foi feito?

### Server (FastAPI - Porta 18000)

O servidor é construído usando FastAPI e roda na porta 18000. Ele é responsável por:

- Gerenciar os workers.
- Manter a consistência e a integridade da blockchain.
- Distribuir IDs aos workers.
- Eleger um "líder" entre os workers.

### Worker (CLI "block-chain-worker")

O worker é um cliente de linha de comando que permite aos usuários:

- Registrar o worker.
- Adicionar novas transações à blockchain.
- Verificar a consistência dos dados.
- Minerar novos blocos.
- Visualizar a cadeia atual de blocos.
- Despejar os dados da blockchain em um banco de dados PostgreSQL, caso fornecido.

## Requisitos

- Docker
- Docker Compose
- Python 3.6 ou superior

## Instalação e Execução

### Server

1. Clone o repositório.
2. Navegue até o diretório que contém o arquivo `docker-compose.yml`.
3. Execute `docker-compose up`.

O servidor estará disponível em `http://localhost:18000`.

### Worker (CLI "block-chain-worker")

1. Clone o repositório do worker.
2. Vá até o diretório do projeto.
3. Execute `python setup.py install`.

Isso instalará o CLI `block-chain-worker`.

## Utilização do CLI "block-chain-worker"

O código fornecido implementa diversos comandos no CLI. Abaixo estão os detalhes de cada comando:

### `register`

Observação: Caso o server esteja em outro endereço diferente de "http://localhost:18000", use o atributo --server {endereço do server}
Registra o worker no servidor.

```bash
block-chain-worker register
```

### `add_transaction`

Adiciona uma nova transação.

```bash
block-chain-worker add_transaction --key "chave" --value "valor"
```

### `get_id`

Retorna o ID do worker.

```bash
block-chain-worker get_id
```

### `get_leader`

Retorna o ID do worker líder.

```bash
block-chain-worker get_leader
```

### `check_consistency`

Verifica a consistência da blockchain.

```bash
block-chain-worker check_consistency
```

### `mine_block`

Minera um novo bloco e adiciona à blockchain.

```bash
block-chain-worker mine_block
```

### `get_chain`

Exibe a blockchain atual.

```bash
block-chain-worker get_chain
```

### `dump_data`

Despeja os dados da blockchain em um banco de dados PostgreSQL.

```bash
block-chain-worker dump_data --db-url "postgresql://username:password@localhost/dbname"
```

### `stop_dump_data`

Para o processo de despejo de dados no banco de dados.

```bash
block-chain-worker stop_dump_data
```

### `disconnect`

Desconecta o worker do servidor.

```bash
block-chain-worker disconnect
```
