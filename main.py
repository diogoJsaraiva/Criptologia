import subprocess
import sys
import os
import time
import socket
import json
from core.user_mgmt import (
    login,
    registar_utilizador,
    listar_utilizadores,
    remover_utilizador,
    alterar_role,
)
from core.config import escolher_metodo, get_metodo, get_tcp_params
from core.crypto import cifrar_mensagem
from vpn import vpn_client, vpn_server
from core.blockchain import blockchain
from core.blockchain import Blockchain 
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
def validar_blockchain_do_servidor():
    print("\n[CLIENTE] A pedir blockchain ao servidor VPN...")
    cadeia_json = pedir_blockchain_ao_vpn()
    if cadeia_json is None:
        print("[CLIENTE] Não foi possível obter a blockchain do servidor VPN.")
        return

    blockchain_local = Blockchain()
    blockchain_local.from_list(cadeia_json)

    print("[CLIENTE] A validar integridade da cadeia...")
    if blockchain_local.validar_blockchain():
        print("[CLIENTE] ✅ Blockchain válida!")
    else:
        print("[CLIENTE] ❌ Blockchain inválida!")
    input("Pressiona Enter para sair...")

def pedir_blockchain_ao_vpn():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 9999))
        sock.sendall("GET_BLOCKCHAIN".encode())
        
        dados = b""
        while True:
            parte = sock.recv(4096)
            if not parte:
                break
            dados += parte
        sock.close()
        
        cadeia = json.loads(dados.decode())
        return cadeia
    except Exception as e:
        print(f"[MAIN] Erro a pedir blockchain ao vpn_server: {e}")
        return None

def mostrar_blockchain():
    cadeia = pedir_blockchain_ao_vpn()
    if cadeia:
        print("\n--- Blockchain Recebida ---")
        print(json.dumps(cadeia, indent=4, ensure_ascii=False))
    else:
        print("Não foi possível obter a blockchain do servidor VPN.")
    input("Pressiona Enter para continuar...")
def menu_gestao_utilizadores():
    while True:
        print("\n=== Gestão de Utilizadores ===")
        print("1. Criar utilizador")
        print("2. Listar utilizadores")
        print("3. Remover utilizador")
        print("4. Alterar role")
        print("5. Voltar")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            registar_utilizador()
        elif escolha == "2":
            users = listar_utilizadores()
            for u, info in users.items():
                print(f"{u} -> {info['role']}")
        elif escolha == "3":
            username = input("Username a remover: ")
            remover_utilizador(username)
        elif escolha == "4":
            username = input("Username: ")
            role = input("Novo role ('admin' ou 'user'): ").strip().lower()
            if role in ("admin", "user"):
                alterar_role(username, role)
            else:
                print("Role inválido.")
        elif escolha == "5":
            print("A voltar ao login.")
            break
        else:
            print("Opção inválida.")


def menu_admin(username):
    while True:
        print(f"\nBem-vindo, admin => {username}!")
        print("1. Gestão de utilizadores")
        print("2. Mudar modo de criptografia")
        print("3. Enviar mensagem")
        print("4. Ver configurações")
        print("5. Validar Blockchain")
        print("6. Ver Blockchain (Proof of Work)")
        print("7. Logout")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            menu_gestao_utilizadores()
        elif escolha == "2":
            escolher_metodo()
        elif escolha == "3":
            enviar_mensagem()
        elif escolha == "4":
            menu_config()
        elif escolha == "5":
            validar_blockchain_do_servidor()
        elif escolha == "6":
            mostrar_blockchain()
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

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destino = ("127.0.0.1", 8888)
    while True:
        metodo, extra = get_metodo()
        mensagem = input("Mensagem a enviar: ")
        print(f"\nMensagem original: {mensagem}")
        udp_sock.sendto(mensagem.encode(), destino)

        print(f"Mensagem cifrada enviada via VPN.")
        nova = input("Deseja enviar outra mensagem? (s/n): ").strip().lower()
        if nova != "s":
            break
def menu_config():
    while True:
        print("\n")
        print("1. Ver parâmetros TCP")
        print("2. Ver menu VPN Client")
        print("3. Ver menu VPN Server")
        print("4. Voltar ao menu anterior")
        escolha = input("Escolha: ").strip()
        
        if escolha == "1":
            host, port = get_tcp_params()
            print(f"\nTCP -> host: {host}, port: {port}")
        elif escolha == "2":
            print("\nConfiguração VPN Client:")
            print(vpn_client.get_config_menu())
        elif escolha == "3":
            print("\nConfiguração VPN Server:")
            print(vpn_server.get_config_menu())
        elif escolha == "4":
            break
        else:
            print("Opção inválida.")
        input("Pressiona Enter para continuar...")

def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Login")
        print("2. Sair da Aplicação")
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
    processes = start_background_services()
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
