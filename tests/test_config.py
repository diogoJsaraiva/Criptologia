import os
from core import config


def test_set_and_get_metodo(tmp_path):
    original_file = config.FICHEIRO_CONFIG
    test_file = tmp_path / "config.txt"
    config.FICHEIRO_CONFIG = str(test_file)

    config.set_metodo("caesar", "7")
    metodo, extra = config.get_metodo()

    assert metodo == "caesar"
    assert extra == "7"

    config.FICHEIRO_CONFIG = original_file

def test_tcp_params(tmp_path):
    original = config.FICHEIRO_TCP
    file_path = tmp_path / "tcp.txt"
    config.FICHEIRO_TCP = str(file_path)

    config.set_tcp_params("1.1.1.1", "1234")
    host, port = config.get_tcp_params()

    assert host == "1.1.1.1"
    assert port == "1234"

    config.FICHEIRO_TCP = original