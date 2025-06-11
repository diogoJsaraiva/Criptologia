import subprocess
import sys
import os
import time

from core.user_mgmt import login, registar_utilizador
from core.config import escolher_metodo, get_metodo, get_tcp_params
from core.crypto import cifrar_mensagem
from vpn import vpn_client, vpn_server
from vpn.vpn_client import enviar_mensagem_vpn

def start_background_services():
    processes = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env['PYTHONPATH'] = root_dir  # Força PYTHONPATH para raiz

    vpn_server_path = os.path.join(root_dir, 'vpn', 'vpn_server.py')
    vpn_client_path = os.path.join(root_dir, 'vpn', 'vpn_client.py')
    udp_receiver_path = os.path.join(root_dir, 'udp', 'prog_udp2.py')

    vpn_proc = subprocess.Popen([sys.executable, vpn_server_path], env=env)
    processes.append(vpn_proc)
    print("[MAIN] VPN Server iniciado.")
    time.sleep(1)

    vpn_client_proc = subprocess.Popen([sys.executable, vpn_client_path], env=env)
    processes.append(vpn_client_proc)
    print("[MAIN] VPN Client iniciado.")
    time.sleep(1)

    udp_proc = subprocess.Popen([sys.executable, udp_receiver_path], env=env)
    processes.append(udp_proc)
    print("[MAIN] UDP Receiver iniciado.")
    time.sleep(1)

    return processes


def menu_admin(username):
    while True:
        print(f"\nBem-vindo, admin => {username}!")
        print("1. Criar novo utilizador")
        print("2. Mudar modo de criptografia")
        print("3. Enviar mensagem")
        print("4. Ver parâmetros TCP")
        print("5. Ver menu VPN Client")
        print("6. Ver menu VPN Server")
        print("7. Logout")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            registar_utilizador()
        elif escolha == "2":
            escolher_metodo()
        elif escolha == "3":
            enviar_mensagem()
        elif escolha == "4":
            host, port = get_tcp_params()
            print(f"TCP -> host: {host}, port: {port}")
        elif escolha == "5":
            print(vpn_client.get_config_menu())
        elif escolha == "6":
            print(vpn_server.get_config_menu())
        elif escolha == "7":
            print("Sessão terminada. A voltar ao login.")
            break
        else:
            print("Opção inválida.")

def menu_user(username):
    while True:
        print(f"\nBem-vindo, User => {username}!")
        print("1. Enviar mensagem")
        print("2. Logout")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            enviar_mensagem()
        elif escolha == "2":
            print("Sessão terminada. A voltar ao login.")
            break
        else:
            print("Opção inválida.")

def enviar_mensagem():
    metodo, extra = get_metodo()
    while True:
        print(f"Método de cifragem atual: {metodo} ({extra if extra else 'default'})")
        mensagem = input("Mensagem a enviar: ")
        cifrada = cifrar_mensagem(mensagem, metodo, extra)
        print(f"\nMensagem original: {mensagem}")
        print(f"Mensagem cifrada: {cifrada}\n")
        enviar_mensagem_vpn(cifrada)
        print(f"Mensagem cifrada enviada via VPN.")
        nova = input("Deseja enviar outra mensagem? (s/n): ").strip().lower()
        if nova != "s":
            break


def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Login")
        print("2. Desligar aplicação")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            username, role = login()
            if not username:
                continue  # volta ao menu principal
            if role == "admin":
                menu_admin(username)
            else:
                menu_user(username)
        elif escolha == "2":
            print("A encerrar aplicação...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    # Arranca os serviços de background (VPN server e UDP receiver)
    processes = "" #start_background_services()
    try:
        main()
    finally:
        print("\n[MAIN] A terminar todos os processos filhos...")
        for proc in processes:
            try:
                proc.terminate()
            except Exception:
                pass
        print("[MAIN] Todos os processos terminados.")
