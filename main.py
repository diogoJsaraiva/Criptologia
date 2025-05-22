from user_mgmt import login, registar_utilizador
from config import escolher_metodo, get_metodo
from crypto import cifrar_mensagem
from vpn_client import enviar_mensagem_vpn

def menu_admin(username):
    while True:
        print(f"\nBem-vindo, admin => {username}!")
        print("1. Criar novo utilizador")
        print("2. Mudar modo de criptografia")
        print("3. Enviar mensagem")
        print("4. Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            registar_utilizador()
        elif escolha == "2":
            escolher_metodo()
        elif escolha == "3":
            enviar_mensagem()
        elif escolha == "4":
            break
        else:
            print("Opção inválida.")

def menu_user(username):
    while True:
        print(f"\nBem-vindo, User => {username}!")
        print("1. Enviar mensagem")
        print("2. Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            enviar_mensagem()
        elif escolha == "2":
            break
        else:
            print("Opção inválida.")

def enviar_mensagem():
    metodo, extra = get_metodo()
    print(f"Método de cifragem atual: {metodo} ({extra if extra else 'default'})")
    mensagem = input("Mensagem a enviar: ")
    cifrada = cifrar_mensagem(mensagem, metodo, extra)
    enviar_mensagem_vpn(cifrada)
    print(f"Mensagem cifrada enviada via VPN.")

def main():
    username, role = login()
    if not username:
        return
    if role == "admin":
        menu_admin(username)
    else:
        menu_user(username)

if __name__ == "__main__":
    main()
