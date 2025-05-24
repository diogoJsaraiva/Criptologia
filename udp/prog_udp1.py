import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    msg = input("[ProgUDP1] Mensagem a enviar: ")
    sock.sendto(msg.encode(), ("127.0.0.1", 8888))
