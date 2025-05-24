# Ứng dụng Truyền File có Ký Số RSA

Ứng dụng web đơn giản sử dụng thuật toán RSA để **tạo và xác minh chữ ký số** cho file. Người dùng có thể tải lên tệp tin, hệ thống sẽ ký số file bằng khóa riêng và cung cấp chữ ký để xác minh bằng khóa công khai.

---

## Giới thiệu về RSA

**RSA (Rivest–Shamir–Adleman)** là một thuật toán mã hóa bất đối xứng phổ biến trong lĩnh vực bảo mật. Nó sử dụng một cặp khóa:
- **Khóa công khai (public key)**: Dùng để xác minh chữ ký.
- **Khóa riêng (private key)**: Dùng để tạo chữ ký số.

Chữ ký số giúp:
- Đảm bảo tính **xác thực** của dữ liệu.
- Bảo vệ **toàn vẹn nội dung**.
- Ngăn chặn giả mạo.

---

## Chức năng chính

### 1. Tải lên & Ký file
- Người dùng chọn file và tải lên.
- Ứng dụng ký file bằng khóa riêng (`private_key.pem`).
- Tạo ra một file chữ ký `.sig`.

### 2. Xác minh chữ ký
- Người dùng chọn file và chữ ký.
- Ứng dụng xác minh bằng khóa công khai (`public_key.pem`).
- Hiển thị kết quả thành công hoặc thất bại.

---

## Hướng dẫn cài đặt & chạy ứng dụng

### Yêu cầu:
- Python 3.x
- Flask
- `cryptography` library

### Cài đặt:
```bash
pip install flask cryptography
▶️ Chạy ứng dụng:
python app.py

Sau đó mở trình duyệt và truy cập: http://127.0.0.1:5000
## 📁 Cấu trúc thư mục
RSA/
├── app.py                  # Ứng dụng Flask chính
├── rsa_utils.py            # Các hàm tiện ích liên quan đến RSA
├── public_key.pem          # Khóa công khai
├── private_key.pem         # Khóa riêng
├── templates/
│   └── index.html          # Giao diện người dùng
└── static/ (nếu có)        # Chứa CSS/JS tĩnh

