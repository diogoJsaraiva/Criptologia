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