import os

FICHEIRO_UTILIZADORES = "assets/utilizadores.txt"

def ler_utilizadores():
    if not os.path.exists(FICHEIRO_UTILIZADORES):
        with open(FICHEIRO_UTILIZADORES, "w") as f:
            f.write("admin;admin123;admin\n")
    utilizadores = {}
    with open(FICHEIRO_UTILIZADORES, "r") as f:
        for linha in f:
            partes = linha.strip().split(";")
            if len(partes) == 3:
                utilizadores[partes[0]] = {"password": partes[1], "role": partes[2]}
    return utilizadores

def guardar_utilizador(username, password, role):
    with open(FICHEIRO_UTILIZADORES, "a") as f:
        f.write(f"{username};{password};{role}\n")

def login():
    utilizadores = ler_utilizadores()
    print("\n=== Ecrã de Login ===")
    username = input("Username: ")
    password = input("Password: ")
    user = utilizadores.get(username)
    if user and user["password"] == password:
        print(f"Login bem-sucedido como {user['role'].capitalize()}")
        return username, user["role"]
    else:
        print("Login inválido.")
        return None, None

def registar_utilizador():
    print("\n=== Registar Novo Utilizador ===")
    username = input("Novo username: ")
    password = input("Nova password: ")
    while True:
        role = input("Role ('admin' ou 'user'): ").strip().lower()
        if role in ("admin", "user"):
            break
        print("Role inválido. Tem de ser 'admin' ou 'user'.")
    guardar_utilizador(username, password, role)
    print(f"Utilizador {username} ({role}) criado com sucesso.")
