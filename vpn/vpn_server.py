import asyncio
import websockets
import socket
import logging

# Ensure INFO level logs are emitted during tests
logging.basicConfig(level=logging.INFO)
from core.crypto import caesar_decrypt, decifrar_mensagem, generate_shared_key
from core.config import get_metodo
from core.config import get_metodo, get_tcp_params

logger = logging.getLogger(__name__)

prime = 23
base = 5
private_key = 6  # VPN Server's private key
shared_key = None

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

    metodo, extra = get_metodo()

    try:
        while True:
            encrypted_msg = await websocket.recv()
            decrypted_msg = decifrar_mensagem(encrypted_msg, metodo, extra)
            print(f"[VPN Server] Mensagem recebida e decifrada: {decrypted_msg}")
            # Also print so that tests capturing stdout see this message
            print(f"Mensagem recebida e decifrada: {decrypted_msg}")

            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_sock.sendto(decrypted_msg.encode(), ("127.0.0.1", 9999))
    except Exception as e:
        print("[VPN Server] Ligação terminada (cliente fechou ligação).")


async def main():
    async with websockets.serve(handle_client, "localhost", 8765, ping_interval=60, ping_timeout=30):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
'''
async def handle_client(websocket):
    global shared_key
    print("[VPN Server] Ligação estabelecida.")

    # Diffie-Hellman exchange
    client_pub_key = int(await websocket.recv())
    server_pub_key = pow(base, private_key, prime)
    await websocket.send(str(server_pub_key))
    shared_key = generate_shared_key(client_pub_key, private_key, prime)
    print(f"[VPN Server] Shared key: {shared_key}")

    while True:
        encrypted_msg = await websocket.recv()
        decrypted_msg = caesar_decrypt(encrypted_msg, shared_key)
        print(f"[VPN Server] Mensagem recebida e decifrada: {decrypted_msg}")

        # Reencaminhar via UDP para ProgUDP2
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.sendto(decrypted_msg.encode(), ("127.0.0.1", 9999))

async def main():
    async with websockets.serve(handle_client, "localhost", 8765, ping_interval=60,ping_timeout=30 ):
        await asyncio.Future()  # espera infinita

asyncio.run(main())

'''