import asyncio
import websockets
import socket
import sys
import os
import json
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.crypto import (
    caesar_decrypt,
    xor_decrypt,
    vigenere_decrypt,
    shared_key_to_vigenere_key,
    generate_shared_key,
    decifrar_mensagem,
    verificar_hash
)
from core.config import get_metodo, get_tcp_params
from core.blockchain import blockchain

prime = 23
base = 5
private_key = 6  # VPN Server's private key
shared_key = None

UDP_LISTEN_PORT = 9998
UDP_TARGET_ADDR = ("127.0.0.1", 9999)


def servidor_blockchain(blockchain, host='127.0.0.1', port=9999):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen()
    print(f"[VPN_SERVER] Servidor blockchain a escutar em {host}:{port}")

    def handle_client(conn):
        try:
            pedido = conn.recv(1024).decode()
            if pedido == "GET_BLOCKCHAIN":
                if pedido == "GET_BLOCKCHAIN":
                    cadeia_json = json.dumps([bloco.to_dict() for bloco in blockchain.chain])
                    conn.sendall(cadeia_json.encode())
        except Exception as e:
            print(f"[VPN_SERVER] Erro no handler: {e}")
        finally:
            conn.close()

    while True:
        conn, addr = server_sock.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


async def handle_client(websocket):
    global shared_key
    print("[VPN Server] Ligação estabelecida.")
    try:
        client_pub_key = int(await websocket.recv())
        server_pub_key = pow(base, private_key, prime)
        await websocket.send(str(server_pub_key))
        shared_key = generate_shared_key(client_pub_key, private_key, prime)
        print(f"[VPN Server] Shared key: {shared_key}")
    except Exception as e:
        print(f"[VPN Server] Erro durante handshake: {e}")
        return

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("127.0.0.1", UDP_LISTEN_PORT))
    udp_sock.setblocking(False)
    loop = asyncio.get_event_loop()

    async def ws_to_udp():
        while True:
            try:
                encrypted_payload = await websocket.recv()
                payload = json.loads(encrypted_payload)
                encrypted_msg = payload.get("mensagem")
                received_hash = payload.get("hash")
                metodo, extra = get_metodo()
                if metodo == "caesar":
                    decrypted_msg = caesar_decrypt(encrypted_msg, shared_key)
                elif metodo == "xor":
                    decrypted_msg = xor_decrypt(encrypted_msg, shared_key)
                elif metodo == "vigenere":
                    vigenere_key = shared_key_to_vigenere_key(shared_key)
                    decrypted_msg = vigenere_decrypt(encrypted_msg, vigenere_key)
                else:
                    decrypted_msg = decifrar_mensagem(encrypted_msg, metodo, extra)

                if verificar_hash(decrypted_msg, received_hash):
                    print(f"[VPN Server] Mensagem válida: {decrypted_msg}")
                    print(f"ID blockchain: {id(blockchain)}")
                    blockchain.adicionar_bloco(decrypted_msg)
                    print("[Blockchain] Bloco adicionado com sucesso!")
                else:
                    print("[VPN Server] ALERTA: Hash inválido!")

                udp_sock.sendto(decrypted_msg.encode(), UDP_TARGET_ADDR)

            except websockets.exceptions.ConnectionClosed:
                print("[VPN Server] WebSocket fechado (cliente terminou).")
                break
            except Exception as e:
                print(f"[VPN Server] Erro em ws_to_udp: {e}")
                break

    try:
        await ws_to_udp()
    finally:
        udp_sock.close()
        print("[VPN Server] Ligação terminada.")


async def main_websocket():
    host, port = get_tcp_params()
    async with websockets.serve(
        handle_client, host, int(port), ping_interval=60, ping_timeout=30
    ):
        await asyncio.Future()  # Run forever


def main():
    # Corre servidor blockchain numa thread paralela
    thread_blockchain = threading.Thread(target=servidor_blockchain, args=(blockchain,), daemon=True)
    thread_blockchain.start()
    print("[VPN_SERVER] Servidor blockchain thread iniciado.")

    # Corre servidor WebSocket no loop async principal
    asyncio.run(main_websocket())


if __name__ == "__main__":
    main()
