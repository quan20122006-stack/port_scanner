import argparse
import sys
import os
from dotenv import load_dotenv
from src.scanner import PortScanner

def main():
    load_dotenv()
    default_workers = int(os.getenv("DEFAULT_MAX_WORKERS", 100))
    default_timeout = float(os.getenv("DEFAULT_TIMEOUT", 0.5))

    parser = argparse.ArgumentParser(
        description="Advanced Python Port Scanner - Hỗ trợ Service Probing & OS Inference."
    )
    
    parser.add_argument("-t", "--target", required=True, help="IP hoặc Domain mục tiêu (VD: 192.168.1.1)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Phạm vi port (Mặc định: 1-1024)")
    parser.add_argument("-w", "--workers", type=int, default=default_workers, help="Số luồng chạy song song")
    parser.add_argument("--timeout", type=float, default=default_timeout, help="Thời gian chờ phản hồi (giây)")
    parser.add_argument("-P", "--probe", action="store_true", help="Kích hoạt Service Probing & OS Inference") # Đã đổi -b thành -P

    args = parser.parse_args()

    try:
        start_port, end_port = map(int, args.ports.split("-"))
    except ValueError:
        print("[!] Lỗi: Định dạng port không hợp lệ. Vui lòng dùng định dạng START-END (VD: 1-1000).")
        sys.exit(1)

    # Truyền cờ probe_services
    scanner = PortScanner(
        target=args.target, 
        max_workers=args.workers, 
        timeout=args.timeout,
        probe_services=args.probe # Sử dụng tham số mới
    )
    scanner.run(start_port=start_port, end_port=end_port)

if __name__ == "__main__":
    main()