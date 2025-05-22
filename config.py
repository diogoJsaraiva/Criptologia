import os

FICHEIRO_CONFIG = "assets/config.txt"

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

def escolher_metodo():
    print("\n=== Mudar modo de criptografia ===")
    print("1. Caesar Cipher")
    escolha = input("Escolha o método [1]: ").strip()
    if escolha == "1" or escolha == "":
        shift = input("Shift do Caesar (ex: 3): ").strip()
        if not shift.isdigit():
            shift = "3"
        set_metodo("caesar", shift)
        print("Método definido para Caesar Cipher.")
    else:
        print("Opção inválida.")
