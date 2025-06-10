import asyncio
import socket
import websockets
from core import crypto
from vpn import vpn_client, vpn_server

class DummySocket:
    def __init__(self):
        self.sent = []
    def sendto(self, data, addr):
        self.sent.append((data, addr))
    def close(self):
        pass

class DummySocketModule:
    AF_INET = socket.AF_INET
    SOCK_DGRAM = socket.SOCK_DGRAM
    def __init__(self, sock):
        self._sock = sock
    def socket(self, *a, **k):
        return self._sock

async def run_client(message):
    encrypted = crypto.cifrar_mensagem(message, "caesar", "3")
    await asyncio.to_thread(vpn_client.enviar_mensagem_vpn, encrypted)


def test_vpn_flow(monkeypatch, capsys):
    dummy = DummySocket()

    async def runner():
        async with websockets.serve(vpn_server.handle_client, "localhost", 8765):
            monkeypatch.setattr(vpn_server, "socket", DummySocketModule(dummy))
            monkeypatch.setattr(vpn_server, "get_metodo", lambda: ("caesar", "3"))
            await run_client("hello")
            await asyncio.sleep(0.1)

    asyncio.run(runner())

    output = capsys.readouterr().out
    assert "Mensagem recebida e decifrada: hello" in output
    assert dummy.sent == [(b"hello", ("127.0.0.1", 9999))]