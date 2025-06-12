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
    print("3. Vigenere Cipher")
    while True:
        escolha = input("Escolha o método: ").strip()
        if escolha == "1":
            while True:
                shift = input("Shift do Caesar (1-25): ").strip()
                if shift.isdigit() and 1 <= int(shift) <= 25:
                    set_metodo("caesar", shift)
                    print("Método definido para Caesar Cipher.")
                    return
                else:
                    print("Shift inválido. Deve ser um número entre 1 e 25.")
        elif escolha == "2":
            while True:
                chave = input("Chave XOR (0-255): ").strip()
                if chave.isdigit() and 0 <= int(chave) <= 255:
                    set_metodo("xor", chave)
                    print("Método definido para XOR Cipher.")
                    return
                else:
                    print("Chave inválida. Deve ser um número entre 0 e 255.")
        elif escolha == "3":
            while True:
                chave = input("Palavra-chave para Vigenère (só letras): ").strip()
                if chave.isalpha():
                    set_metodo("vigenere", chave.lower())
                    print("Método definido para Vigenère Cipher.")
                    return
                else:
                    print("Chave inválida. Deve conter apenas letras (a-z, A-Z).")
 
        else:
            print("Opção inválida. Escolha 1 para Caesar ou 2 para XOR.")