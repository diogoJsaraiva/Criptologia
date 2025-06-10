import os
import getpass
from core.crypto import caesar_encrypt, caesar_decrypt

FICHEIRO_UTILIZADORES = "assets/utilizadores.txt"

def ler_utilizadores():
    # Verifica se o ficheiro existe, senão cria com admin cifrado
    if not os.path.exists(FICHEIRO_UTILIZADORES):
        with open(FICHEIRO_UTILIZADORES, "w") as f:
            # Password 'admin123' cifrada com Caesar shift 3
            password_cifrada = caesar_encrypt("admin123", 3)
            f.write(f"admin;{password_cifrada};admin\n")
    utilizadores = {}
    with open(FICHEIRO_UTILIZADORES, "r") as f:
        for linha in f:
            partes = linha.strip().split(";")
            if len(partes) == 3:
                utilizadores[partes[0]] = {"password": partes[1], "role": partes[2]}
    return utilizadores


def guardar_utilizador(username, password, role):
    # Usa shift 3 para cifrar (podes tornar configurável se quiseres)
    password_cifrada = caesar_encrypt(password, 3)
    with open(FICHEIRO_UTILIZADORES, "a") as f:
        f.write(f"{username};{password_cifrada};{role}\n")


def login():
    utilizadores = ler_utilizadores()
    while True:
        print("\n=== Ecrã de Login ===")
        username = input("Username: ")
        # Usa getpass para que a password n\xE3o fique vis\xEDvel no terminal
        password = getpass.getpass("Password: ")
        user = utilizadores.get(username)
        if user:
            password_decifrada = caesar_decrypt(user["password"], 3)
            if password_decifrada == password:
                print(f"Login bem-sucedido como {user['role'].capitalize()}")
                return username, user["role"]
        print("Login inválido.")
        tentar_novamente = input("Deseja tentar novamente? (s/n): ").strip().lower()
        if tentar_novamente != "s":
            return None, None


def registar_utilizador():
    print("\n=== Registar Novo Utilizador ===")
    username = input("Novo username: ")
    utilizadores = ler_utilizadores()
    userExists = utilizadores.get(username)
    if userExists:
        print("\n=== O utilizador já existe!!!  ===")
        return registar_utilizador()
    # Oculta a password enquanto \xE9 escrita
    password = getpass.getpass("Nova password: ")
    while True:
        role = input("Role ('admin' ou 'user'): ").strip().lower()
        if role in ("admin", "user"):
            break
        print("Role inválido. Tem de ser 'admin' ou 'user'.")
    guardar_utilizador(username, password, role)
    print(f"Utilizador {username} ({role}) criado com sucesso.")