import builtins
from core import user_mgmt
from core import crypto


def test_guardar_e_ler_utilizador(tmp_path):
    original = user_mgmt.FICHEIRO_UTILIZADORES
    file_path = tmp_path / "users.txt"
    user_mgmt.FICHEIRO_UTILIZADORES = str(file_path)

    # Cria ficheiro com admin default
    user_mgmt.ler_utilizadores()

    user_mgmt.guardar_utilizador("alice", "secret", "user")
    users = user_mgmt.ler_utilizadores()
    assert "alice" in users
    assert users["alice"]["role"] == "user"
    decrypted = crypto.caesar_decrypt(users["alice"]["password"], 3)
    assert decrypted == "secret"

    user_mgmt.FICHEIRO_UTILIZADORES = original


def test_login_success(monkeypatch, tmp_path):
    original = user_mgmt.FICHEIRO_UTILIZADORES
    file_path = tmp_path / "users.txt"
    user_mgmt.FICHEIRO_UTILIZADORES = str(file_path)

    user_mgmt.ler_utilizadores()  # cria admin
    user_mgmt.guardar_utilizador("bob", "mypwd", "user")

    inputs = iter(["bob", "mypwd"])  # login uma vez com sucesso

    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(user_mgmt.getpass, "getpass", lambda _: next(inputs))
    username, role = user_mgmt.login()

    assert username == "bob"
    assert role == "user"

    user_mgmt.FICHEIRO_UTILIZADORES = original