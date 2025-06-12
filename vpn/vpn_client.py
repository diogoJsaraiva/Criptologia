import asyncio
import websockets
import socket

import logging
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.crypto import (
    caesar_encrypt,
    xor_encrypt,
    caesar_decrypt,
    xor_decrypt,
    vigenere_encrypt,
    vigenere_decrypt,
    shared_key_to_vigenere_key,
    generate_shared_key,
    generate_public_key,
    generate_private_key,
    calcular_hash_sha256
)
from core.config import get_metodo, get_tcp_params

logger = logging.getLogger(__name__)

prime = 23
base = 5
private_key = generate_private_key()
public_key = generate_public_key(base, prime, private_key)
shared_key = None

def get_config_menu():
    metodo, extra = get_metodo()
    host, port = get_tcp_params()
    return {
        "component": "vpn_client",
        "metodo": metodo,
        "extra": extra,
        "host": host,
        "port": port,
    }
   
async def udp_listener():
    """Create a UDP socket bound to 127.0.0.1:8888."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8888))
    sock.setblocking(False)
    logger.info("[VPN Client] À escuta em UDP 8888...")
    return sock


async def vpn_client():
    """Listen on UDP and forward datagrams encrypted to the VPN server."""
    global shared_key

    sock = await udp_listener()

    host, port = get_tcp_params()
    url = f"ws://{host}:{port}"

    async with websockets.connect(url) as websocket:
        # Diffie-Hellman handshake
        await websocket.send(str(public_key))
        server_pub_key = int(await websocket.recv())
        shared_key = generate_shared_key(server_pub_key, private_key, prime)

        logger.info(f"[VPN Client] Shared key: {shared_key}")

        loop = asyncio.get_running_loop()
        while True:
            try:
                data, _ = await loop.run_in_executor(None, sock.recvfrom, 1024)
            except BlockingIOError:
                await asyncio.sleep(0.1)
                continue
            except asyncio.CancelledError:
                break

            message = data.decode()
            metodo, _ = get_metodo()
            if metodo == "caesar":
                print("1")
                encrypted = caesar_encrypt(message, shared_key)
            elif metodo == "xor":
                print("2")
                encrypted = xor_encrypt(message, shared_key)
            elif metodo == "vigenere":
                print("3")
                vigenere_key = shared_key_to_vigenere_key(shared_key)
                encrypted = vigenere_encrypt(message, vigenere_key)
            else:
                encrypted = message
            hash_msg = calcular_hash_sha256(message)
            await websocket.send(json.dumps({
                "mensagem": encrypted,
                "hash": hash_msg
            }))
            logger.info(f"[VPN Client] Mensagem cifrada enviada: {encrypted}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(vpn_client())
