
# receiver.py
import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

def recv_all(sock, length):
    data = b""
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError("Socket closed trước khi nhận đủ dữ liệu")
        data += more
    return data

def recv_file(sock):
    # Nhận kích thước dữ liệu trước (8 bytes)
    size_bytes = recv_all(sock, 8)
    size = int.from_bytes(size_bytes, byteorder='big')
    # Nhận dữ liệu theo kích thước
    data = recv_all(sock, size)
    return data

# Load khóa công khai
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

def verify_signature(data, signature):
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

def main():
    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 5001

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(1)
    print(f"Đang chờ kết nối tại {SERVER_IP}:{SERVER_PORT}...")

    conn, addr = sock.accept()
    print(f"Đã kết nối với {addr}")

    # Nhận file
    file_data = recv_file(conn)
    print(f"Đã nhận file (size={len(file_data)} bytes)")

    # Nhận chữ ký
    signature = recv_file(conn)
    print(f"Đã nhận chữ ký (size={len(signature)} bytes)")

    # Kiểm tra chữ ký
    if verify_signature(file_data, signature):
        print("Chữ ký hợp lệ, lưu file thành công.")
        with open("received_data.txt", "wb") as f:
            f.write(file_data)
    else:
        print("Chữ ký không hợp lệ hoặc file đã bị sửa đổi!")

    conn.close()
    sock.close()

if __name__ == "__main__":
    main()
