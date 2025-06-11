import asyncio
import websockets
import socket
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.crypto import (
    caesar_decrypt,
    xor_decrypt,
    caesar_encrypt,
    xor_encrypt,
    generate_shared_key,
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

    client_pub_key = int(await websocket.recv())
    server_pub_key = pow(base, private_key, prime)
    await websocket.send(str(server_pub_key))
    shared_key = generate_shared_key(client_pub_key, private_key, prime)
    print(f"[VPN Server] Shared key: {shared_key}")

    metodo, _ = get_metodo()

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if hasattr(udp_sock, "bind"):
        udp_sock.bind(("127.0.0.1", UDP_LISTEN_PORT))
    if hasattr(udp_sock, "setblocking"):
        udp_sock.setblocking(False)
    loop = asyncio.get_event_loop()

    async def ws_to_udp():
        if not hasattr(udp_sock, "recvfrom"):
            return
        while True:
            encrypted_msg = await websocket.recv()
            if metodo == "caesar":
                decrypted_msg = caesar_decrypt(encrypted_msg, shared_key)
            elif metodo == "xor":
                decrypted_msg = xor_decrypt(encrypted_msg, shared_key)
            else:
                decrypted_msg = encrypted_msg
            print(f"[VPN Server] Mensagem recebida e decifrada: {decrypted_msg}")
            udp_sock.sendto(decrypted_msg.encode(), UDP_TARGET_ADDR)

    async def udp_to_ws():
        while True:
            data, _ = await loop.run_in_executor(None, udp_sock.recvfrom, 1024)
            message = data.decode()
            if metodo == "caesar":
                encrypted = caesar_encrypt(message, shared_key)
            elif metodo == "xor":
                encrypted = xor_encrypt(message, shared_key)
            else:
                encrypted = message
            await websocket.send(encrypted)

    try:
        await asyncio.gather(ws_to_udp(), udp_to_ws())
    except Exception:
        print("[VPN Server] Ligação terminada (cliente fechou ligação).")
    finally:
        udp_sock.close()


async def main():
    host, port = get_tcp_params()
    async with websockets.serve(
        handle_client, host, int(port), ping_interval=60, ping_timeout=30
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())