# 🚀 PyPortScanner - Advanced Python Port Scanner

**PyPortScanner** là một công cụ quét cổng mạng (Port Scanner) đa luồng được xây dựng bằng Python, phục vụ cho mục đích học tập về Network Security và Pentesting.

Tool hỗ trợ:

* 🔍 Service Probing
* 🏷 Banner Grabbing
* 🧠 Basic OS Inference

---

## ✨ Features

* ⚡ Multithreaded scanning (tăng tốc độ quét)
* 🎯 Quét port linh hoạt (custom range / default ports)
* 🔍 Service detection & banner grabbing
* 🧠 Basic OS inference (dựa trên phản hồi dịch vụ)
* 🛡 Stealth mode (giảm khả năng bị phát hiện)
* ⏱ Configurable timeout & worker threads

---

## 📂 Project Structure

```bash
py-port-scanner/
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── src/
    ├── __init__.py
    ├── cli.py
    └── scanner.py
```

---

## 🚀 Installation

Clone project:

```bash
git clone https://github.com/quan20122006-stack/port_scanner.git
cd py-port-scanner
```

Tạo virtual environment (khuyến nghị):

```bash
python -m venv venv
```

Kích hoạt:

```bash
# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

Cài dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Hiển thị help:

```bash
python run.py -h
```

### 🔹 Quét cơ bản (nhanh)

```bash
python run.py -t 192.168.1.1
```

---

### 🔹 Quét nâng cao (Service + OS detection)

```bash
python run.py -t 127.0.0.1 -P
```

---

### 🔹 Stealth Scan (né firewall / IDS cơ bản)

```bash
python run.py -t 10.10.10.5 -w 1 --timeout 2.0
```

---

## 📌 Example Output

```bash
[+] Target: 192.168.1.1
[+] Port 22 (SSH) OPEN
[+] Port 80 (HTTP) OPEN
[+] Banner: Apache/2.4.41 (Ubuntu)

[+] OS Guess: Linux

Scan completed.
```

---

## 🧠 How It Works

Tool hoạt động theo các bước:

1. Tạo TCP socket
2. Kết nối tới từng port trên target
3. Nếu connect thành công → port OPEN
4. Gửi payload để lấy banner (service probing)
5. Phân tích response để đoán OS
6. Sử dụng multithreading để tăng tốc

---

## 🛠 Technologies Used

* **Python 3**
* **Socket Programming**
* **Threading**
* **Networking Fundamentals**

---

## 🎯 Learning Objectives

Project này giúp bạn luyện:

* Python networking
* Port scanning techniques
* Multithreading
* Service enumeration
* Basic reconnaissance mindset

---

## ⚠️ Disclaimer

Tool này chỉ dùng cho:

* Học tập
* Lab cá nhân
* Pentest có sự cho phép

❗ Không sử dụng để scan hệ thống khi chưa được phép.

---

## 📈 Future Improvements

* [ ] UDP scanning
* [ ] Full OS fingerprinting (giống Nmap)
* [ ] Export JSON / CSV
* [ ] CIDR / subnet scanning
* [ ] GUI interface

---

## 👨‍💻 Author

**Quan**
GitHub: https://github.com/quan20122006-stack

---

## ⭐ Support

Nếu thấy project hữu ích, hãy ⭐ repo để ủng hộ!
