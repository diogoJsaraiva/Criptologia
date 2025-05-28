import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 9999))
print("[ProgUDP2] À escuta em UDP 9999...")
while True:
    data, addr = sock.recvfrom(1024)
    print(f"[ProgUDP2] Recebido: {data.decode()}")
