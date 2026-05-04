# 🚀 PyPortScanner - Advanced Python Port Scanner

**PyPortScanner** là một công cụ quét cổng mạng (Port Scanner) đa luồng được phát triển bằng Python. Công cụ hỗ trợ thăm dò dịch vụ (Service Probing), nhận diện phiên bản (Banner Grabbing) và suy luận hệ điều hành (Basic OS Inference).

---

## 📂 Cấu trúc thư mục dự án

Để chạy dự án theo cấu trúc chuẩn, bạn cần tạo các file với nội dung tương ứng ở phần "Mã Nguồn" bên dưới theo đúng cấu trúc sau:
```text
py-port-scanner/
│
├── .env                    # Biến môi trường
├── .gitignore              # Bỏ qua file rác khi dùng Git
├── requirements.txt        # Danh sách thư viện
├── run.py                  # File khởi chạy chính
└── src/                    # Thư mục mã nguồn
    ├── __init__.py         # File rỗng đánh dấu package
    ├── cli.py              # Xử lý tham số dòng lệnh
    └── scanner.py          # Logic quét port cốt lõi


💻 Hướng dẫn Cài đặt & Sử dụng

 1. CÀI ĐẶT MÔI TRƯỜNG 
Clone project
git clone <your-repo-url>
cd PY_PORT_SCANNER

 # Tạo môi trường ảo (Khuyến nghị)
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows: venv\Scripts\activate
# Trên Linux/macOS: source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

2.Các lệnh quét tiêu biểu:
python run.py -h Dùng để xem các option chạy của tool 

# Quét cơ bản IP nội bộ (Dùng danh bạ mặc định, chạy cực nhanh)
python run.py -t 192.168.1.1

# Quét sâu (Service Probing & OS Inference) - Tốn thời gian hơn
python run.py -t 127.0.0.1 -P

# Quét tàng hình (Stealth) - Né Firewall bằng cách chạy 1 luồng, delay 2s
python run.py -t 10.10.10.5 -w 1 --timeout 2.0