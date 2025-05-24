# sender.py
import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import os

# Load khóa riêng
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

def sign_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def send_file(sock, data):
    # Gửi kích thước dữ liệu trước
    sock.sendall(len(data).to_bytes(8, byteorder='big'))
    # Gửi dữ liệu
    sock.sendall(data)

def main():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 5001

    file_path = "data.txt"
    signature = sign_file(file_path)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    # Gửi file
    with open(file_path, "rb") as f:
        file_data = f.read()

    print(f"Gửi file {file_path} (size={len(file_data)} bytes)")
    send_file(sock, file_data)

    print(f"Gửi chữ ký (size={len(signature)} bytes)")
    send_file(sock, signature)

    sock.close()
    print("Đã gửi file và chữ ký.")

if __name__ == "__main__":
    main()
