import asyncio
import websockets
import socket
import logging
from core.crypto import (
    caesar_encrypt,
    xor_encrypt,
    caesar_decrypt,
    xor_decrypt,
    generate_shared_key,
    generate_public_key,
    generate_private_key,
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


async def enviar_vpn_async(mensagem):
    """Estabelece ligação ao servidor VPN e envia uma mensagem já cifrada
    usando a chave partilhada obtida via Diffie–Hellman."""
    global shared_key
    host, port = get_tcp_params()
    url = f"ws://{host}:{port}"
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(str(public_key))
            server_pub_key = int(await websocket.recv())
            shared_key = generate_shared_key(server_pub_key, private_key, prime)
            await websocket.send(mensagem)
            # Não é necessário receber nada, a função termina aqui.
    except websockets.exceptions.ConnectionClosedOK:
        pass


def enviar_mensagem_vpn(mensagem):
    """Wrapper síncrono para envio de mensagens através da VPN."""
    asyncio.run(enviar_vpn_async(mensagem))    

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
                encrypted = caesar_encrypt(message, shared_key)
            elif metodo == "xor":
                encrypted = xor_encrypt(message, shared_key)
            else:
                encrypted = message

            await websocket.send(encrypted)
            logger.info(f"[VPN Client] Mensagem cifrada enviada: {encrypted}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(vpn_client())


async def tunnel_vpn_async(mensagem):
    """Envia uma mensagem e aguarda uma resposta cifrada, reencaminhando-a
    para o ProgUDP1."""
    global shared_key
    host, port = get_tcp_params()
    url = f"ws://{host}:{port}"
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    async with websockets.connect(url) as websocket:
        await websocket.send(str(public_key))
        server_pub_key = int(await websocket.recv())
        shared_key = generate_shared_key(server_pub_key, private_key, prime)

        metodo, _ = get_metodo()
        if metodo == "caesar":
            encrypted = caesar_encrypt(mensagem, shared_key)
        elif metodo == "xor":
            encrypted = xor_encrypt(mensagem, shared_key)
        else:
            encrypted = mensagem

        await websocket.send(encrypted)
        try:
            encrypted_reply = await asyncio.wait_for(websocket.recv(), timeout=2)
        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedOK):
            return

        if metodo == "caesar":
            decrypted = caesar_decrypt(encrypted_reply, shared_key)
        elif metodo == "xor":
            decrypted = xor_decrypt(encrypted_reply, shared_key)
        else:
            decrypted = encrypted_reply

        udp_sock.sendto(decrypted.encode(), ("127.0.0.1", 8888))
        udp_sock.close()


def tunnel_mensagem_vpn(mensagem):
    """Wrapper síncrono para tunnel_vpn_async."""
    asyncio.run(tunnel_vpn_async(mensagem))

