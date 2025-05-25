from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
from dask import delayed, compute

BLOCK_SIZE = 16 * 1024  # 16 KB

def create_cipher(key, iv):
    return Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

@delayed
def encrypt_file_dask(input_path, output_path, key, iv):
    cipher = create_cipher(key, iv)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        while chunk := fin.read(BLOCK_SIZE):
            padded_data = padder.update(chunk)
            fout.write(encryptor.update(padded_data))
        fout.write(encryptor.update(padder.finalize()) + encryptor.finalize())

def decrypt_file_dask(input_file, output_file, password):
    import dask
    import dask.bag as db

    def decrypt(data, password):
        return bytes(b ^ ord(password[i % len(password)]) for i, b in enumerate(data))

    with open(input_file, "rb") as f:
        content = f.read()

    encrypted_chunks = db.from_sequence([content], npartitions=1)
    decrypted = encrypted_chunks.map(lambda b: decrypt(b, password))
    result = decrypted.compute()[0]

    with open(output_file, "wb") as out:
        out.write(result)