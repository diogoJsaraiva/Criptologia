import asyncio
import websockets
import socket
from core.crypto import caesar_encrypt,cifrar_mensagem, generate_shared_key, generate_public_key, generate_private_key
from core.config import escolher_metodo, get_metodo,set_metodo
prime = 23
base = 5
private_key = generate_private_key()
public_key = generate_public_key(base, prime, private_key)
shared_key = None
'''
async def enviar_vpn_async(mensagem_cifrada):
    global shared_key
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send(str(public_key))
        server_pub_key = int(await websocket.recv())
        shared_key = generate_shared_key(server_pub_key, private_key, prime)
        await websocket.send(mensagem_cifrada)
        # Não é necessário receber nada, a função termina aqui.

def enviar_mensagem_vpn(mensagem_cifrada):
    asyncio.run(enviar_vpn_async(mensagem_cifrada))
    
'''
async def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8888))
    sock.setblocking(False)  # importante para não bloquear
    print("[VPN Client] À escuta em UDP 8888...")
    return sock

async def vpn_client():
    global shared_key
    sock = await udp_listener()

    async with websockets.connect("ws://localhost:8765") as websocket:
        # Diffie-Hellman
        await websocket.send(str(public_key))
        server_pub_key = int(await websocket.recv())
        shared_key = generate_shared_key(server_pub_key, private_key, prime)
        print(f"[VPN Client] Shared key: {shared_key}")
        set_metodo("caesar1", shared_key)
        loop = asyncio.get_event_loop()

        while True:
            try:
                # corre recvfrom em background para não bloquear
                data, _ = await loop.run_in_executor(None, sock.recvfrom, 1024)
                message = data.decode()
                metodo,extra = get_metodo()
                encrypted = cifrar_mensagem(message, metodo, extra)
                await websocket.send(encrypted)
                print(f"[VPN Client] Mensagem cifrada enviada: {encrypted}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                await asyncio.sleep(1)