import os

FICHEIRO_CONFIG = "assets/config.txt"
FICHEIRO_TCP = "assets/tcp_params.txt"

def get_metodo():
    if not os.path.exists(FICHEIRO_CONFIG):
        set_metodo("caesar", "3")
    with open(FICHEIRO_CONFIG, "r") as f:
        linha = f.readline().strip()
        partes = linha.split(";")
        if len(partes) == 2:
            return partes[0], partes[1]
        else:
            return "caesar", "3"

def set_metodo(metodo, extra=""):
    with open(FICHEIRO_CONFIG, "w") as f:
        f.write(f"{metodo};{extra}\n")

def get_tcp_params():
    if not os.path.exists(FICHEIRO_TCP):
        set_tcp_params("localhost", "8765")
    with open(FICHEIRO_TCP, "r") as f:
        linha = f.readline().strip()
        partes = linha.split(";")
        if len(partes) == 2:
            return partes[0], partes[1]
        return "localhost", "8765"

def set_tcp_params(host, port):
    with open(FICHEIRO_TCP, "w") as f:
        f.write(f"{host};{port}\n")
        
def escolher_metodo():
    print("\n=== Mudar modo de criptografia ===")
    print("1. Caesar Cipher")
    print("2. XOR Cipher")

    escolha = input("Escolha o método [1]: ").strip()
    if escolha == "1" or escolha == "":
        shift = input("Shift do Caesar (ex: 3): ").strip()
        if not shift.isdigit():
            shift = "3"
        set_metodo("caesar", shift)
        print("Método definido para Caesar Cipher.")
    elif escolha == "2":
        chave = input("Chave XOR (0-255): ").strip()
        if not chave.isdigit():
            chave = "42"
        set_metodo("xor", chave)
        print("Método definido para XOR Cipher.")
    else:
        print("Opção inválida.")