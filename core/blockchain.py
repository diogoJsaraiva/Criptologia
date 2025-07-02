import hashlib
import time
import json

class Blockchain:
    def __init__(self, dificuldade=4, ficheiro_output="blockchain.json"):
        self.dificuldade = dificuldade
        self.ficheiro_output = ficheiro_output
        self.chain = [self.criar_genesis()]

    def criar_genesis(self):
        return Block(0, "Bloco Génesis", time.time(), "0", self.dificuldade)

    def adicionar_bloco(self, mensagem):
        bloco_anterior = self.chain[-1]
        novo_bloco = Block(
            len(self.chain),
            mensagem,
            time.time(),
            bloco_anterior.hash,
            self.dificuldade
        )
        self.chain.append(novo_bloco)
        self.guardar_em_ficheiro()  # <-- guarda sempre que há novo bloco

    def validar_blockchain(self):
        for i in range(1, len(self.chain)):
            atual = self.chain[i]
            anterior = self.chain[i - 1]
            if atual.hash != atual.calcular_hash():
                return False
            if atual.hash_anterior != anterior.hash:
                return False
            if not atual.hash.startswith("0" * self.dificuldade):
                return False
        return True

    def guardar_em_ficheiro(self):
        dados = [bloco.to_dict() for bloco in self.chain]
        with open(self.ficheiro_output, "w") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def from_list(self, blocos_lista):
        self.chain = []
        for bloco_dict in blocos_lista:
            bloco = Block(
                bloco_dict['index'],
                bloco_dict['mensagem'],
                bloco_dict['timestamp'],
                bloco_dict['hash_anterior'],
                self.dificuldade
            )
            bloco.nonce = bloco_dict['nonce']
            bloco.hash = bloco_dict['hash']
            self.chain.append(bloco)

class Block:
    def __init__(self, index, mensagem, timestamp, hash_anterior, dificuldade):
        self.index = index
        self.mensagem = mensagem
        self.timestamp = timestamp
        self.hash_anterior = hash_anterior
        self.nonce = 0
        self.dificuldade = dificuldade
        self.hash = self.proof_of_work()

    def calcular_hash(self):
        conteudo = f"{self.index}{self.mensagem}{self.timestamp}{self.hash_anterior}{self.nonce}"
        return hashlib.sha256(conteudo.encode()).hexdigest()

    def proof_of_work(self):
        prefixo = "0" * self.dificuldade
        while True:
            hash_atual = self.calcular_hash()
            if hash_atual.startswith(prefixo):
                return hash_atual
            self.nonce += 1

    def to_dict(self):
        return {
            "index": self.index,
            "mensagem": self.mensagem,
            "timestamp": self.timestamp,
            "hash_anterior": self.hash_anterior,
            "nonce": self.nonce,
            "hash": self.hash
        }

blockchain = Blockchain()