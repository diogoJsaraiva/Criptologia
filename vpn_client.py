import asyncio
import websockets
import socket
from crypto import caesar_encrypt, generate_shared_key, generate_public_key, generate_private_key

prime = 23
base = 5
private_key = generate_private_key()
public_key = generate_public_key(base, prime, private_key)
shared_key = None

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

        loop = asyncio.get_event_loop()

        while True:
            try:
                # corre recvfrom em background para não bloquear
                data, _ = await loop.run_in_executor(None, sock.recvfrom, 1024)
                message = data.decode()
                encrypted = caesar_encrypt(message, shared_key)
                await websocket.send(encrypted)
                print(f"[VPN Client] Mensagem cifrada enviada: {encrypted}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                await asyncio.sleep(1)

asyncio.run(vpn_client())
