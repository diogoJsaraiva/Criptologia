import asyncio
import websockets
import socket
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.crypto import (
    caesar_decrypt,
    xor_decrypt,
    caesar_encrypt,
    xor_encrypt,
    vigenere_encrypt,
    vigenere_decrypt,
    shared_key_to_vigenere_key,
    generate_shared_key,
    decifrar_mensagem,
    cifrar_mensagem,
    verificar_hash
)
from core.config import get_metodo, get_tcp_params


prime = 23
base = 5
private_key = 6  # VPN Server's private key
shared_key = None

UDP_LISTEN_PORT = 9998
UDP_TARGET_ADDR = ("127.0.0.1", 9999)

def get_config_menu():
    metodo, extra = get_metodo()
    host, port = get_tcp_params()
    return {
        "component": "vpn_server",
        "metodo": metodo,
        "extra": extra,
        "host": host,
        "port": port,
    }


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
                metodo, _ = get_metodo()
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
                else:
                    print("[VPN Server] ALERTA: Hash inválido!")

                udp_sock.sendto(decrypted_msg.encode(), UDP_TARGET_ADDR)

            except websockets.exceptions.ConnectionClosed:
                print("[VPN Server] WebSocket fechado (cliente terminou).")
                break
            except Exception as e:
                print(f"[VPN Server] Erro em ws_to_udp: {e}")
                break

    async def udp_to_ws():
        while True:
            try:
                data, _ = await loop.run_in_executor(None, udp_sock.recvfrom, 1024)
                message = data.decode()
                encrypted = cifrar_mensagem(message, metodo, extra)
                await websocket.send(encrypted)
            except websockets.exceptions.ConnectionClosed:
                print("[VPN Server] WebSocket fechado ao tentar enviar.")
                break
            except Exception as e:
                print(f"[VPN Server] Erro em udp_to_ws: {e}")
                break

    try:
        await asyncio.gather(ws_to_udp(), udp_to_ws())
    except Exception as e:
        print(f"[VPN Server] Erro geral na comunicação: {e}")
    finally:
        udp_sock.close()
        print("[VPN Server] Ligação terminada.")


async def main():
    host, port = get_tcp_params()
    async with websockets.serve(
        handle_client, host, int(port), ping_interval=60, ping_timeout=30
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
