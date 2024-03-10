import sys
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def pbkdf2_key_derivation(passphrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=100000,  # Ajuste o número de iterações conforme necessário
        length=32,  # Tamanho da chave em bytes
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())
    return key

def generate_nonce():
    return os.urandom(16)

def encrypt_chacha20(message, key, nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    return ct

def decrypt_chacha20(ciphertext, key, nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message

def main():
    if len(sys.argv) != 2:
        print("Utilização: python3 pbenc_chacha20.py <ficheiro>")
        sys.exit(1)

    passphrase = input("Introduza a passphrase: ")
    salt = b'\x00'  # Defina um valor de salt adequado
    key = pbkdf2_key_derivation(passphrase, salt)
    nonce = generate_nonce()

    with open(sys.argv[1], 'rb') as file:
        ciphertext = file.read()

    decrypted_bytes = decrypt_chacha20(ciphertext, key, nonce)
    # Faça o que for necessário com os bytes decifrados (salvar em um arquivo binário, etc.)
    print("Dados decifrados:", decrypted_bytes)

if __name__ == '__main__':
    main()