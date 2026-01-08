from src.core.security import crypto


def test_crypto_functions_exist():
    assert callable(crypto.encrypt)
    assert callable(crypto.decrypt)
    assert callable(crypto.get_webhook_hash)
    assert callable(crypto.is_encrypted)
    assert callable(crypto.deep_decrypt)


def test_encrypt_decrypt_roundtrip():
    text = "hello world"
    encrypted = crypto.encrypt(text)
    decrypted = crypto.decrypt(encrypted)
    assert decrypted == text


def test_is_encrypted():
    encrypted = crypto.encrypt("test")
    assert not crypto.is_encrypted(encrypted)
    assert not crypto.is_encrypted("plain")
