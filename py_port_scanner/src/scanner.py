import socket
import concurrent.futures
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

class PortScanner:
    def __init__(self, target: str, max_workers: int = 100, timeout: float = 0.5, probe_services: bool = False):
        self.target = target
        self.max_workers = max_workers
        self.timeout = timeout
        self.probe_services = probe_services
        self.open_ports = []
        # Danh sách các hệ điều hành dự đoán dựa trên banner
        self.os_guesses = []

    def probe_service_and_os(self, port: int) -> tuple[str, str]:
        """
        Gửi các payload khác nhau để xác định chính xác dịch vụ và suy luận OS.
        Trả về: (Real Service, Banner/Version)
        """
        # Thử kết nối TCP cơ bản
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(max(1.0, self.timeout + 0.5))
            s.connect((self.target, port))
        except Exception:
            return "unknown", "N/A"

        banner = ""
        service_name = "unknown"

        # 1. Thử chờ Banner tự động (SSH, FTP, SMTP thường tự gửi banner ngay khi kết nối)
        try:
            # Chờ một lúc xem có banner tự động không
            s.settimeout(1.5)
            data = s.recv(1024).decode('utf-8', errors='ignore').strip()
            if data:
                banner = data.split('\n')[0].strip()
                if "SSH" in banner:
                    service_name = "ssh"
                elif "FTP" in banner or "220" in banner:
                    service_name = "ftp"
                elif "SMTP" in banner or "220" in banner:
                    service_name = "smtp"
        except socket.timeout:
            # Nếu không có banner tự động, thử gửi HTTP Request
            pass
        except Exception:
            pass

        # 2. Nếu chưa nhận diện được, gửi payload HTTP GET
        if not banner:
            try:
                # Gửi HTTP payload
                http_payload = f"GET / HTTP/1.1\r\nHost: {self.target}\r\n\r\n".encode()
                s.sendall(http_payload)
                data = s.recv(1024).decode('utf-8', errors='ignore')
                
                if "HTTP" in data:
                    service_name = "http/https"
                    # Lấy dòng Server hoặc X-Powered-By nếu có
                    for line in data.split('\n'):
                        if "Server:" in line:
                            banner = line.strip()
                            break
                        elif "HTTP/1." in line:
                            banner = line.strip()
            except Exception:
                pass

        s.close()
        
        # 3. Suy luận OS (Basic OS Fingerprinting Inference)
        self._infer_os_from_banner(banner)

        # Cắt bớt banner nếu quá dài
        banner = banner[:60] + "..." if len(banner) > 60 else banner
        
        return service_name if service_name != "unknown" else "unidentified", banner or "No Banner"

    def _infer_os_from_banner(self, banner: str):
        """Suy luận hệ điều hành từ các dấu hiệu trong banner"""
        banner_lower = banner.lower()
        if "ubuntu" in banner_lower:
            self.os_guesses.append("Ubuntu Linux")
        elif "debian" in banner_lower:
            self.os_guesses.append("Debian Linux")
        elif "centos" in banner_lower or "red hat" in banner_lower:
            self.os_guesses.append("CentOS/RHEL")
        elif "windows" in banner_lower or "microsoft-iis" in banner_lower:
            self.os_guesses.append("Windows")
        elif "freebsd" in banner_lower:
             self.os_guesses.append("FreeBSD")

    def scan_port(self, port: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                # Nếu tính năng probe được bật, tiến hành phân tích sâu
                if self.probe_services:
                    real_service, banner = self.probe_service_and_os(port)
                    self.open_ports.append((port, real_service, banner))
                else:
                    # Nếu không bật probe, chỉ tra cứu danh bạ (dễ sai lệch)
                    try:
                        guessed_service = socket.getservbyport(port)
                    except OSError:
                        guessed_service = "unknown"
                    self.open_ports.append((port, guessed_service, "-"))
            
            sock.close()
        except Exception:
            pass

    def run(self, start_port: int = 1, end_port: int = 1024):
        console.print(f"[bold blue][*] Mục tiêu: {self.target} | Ports: {start_port}-{end_port} | Threads: {self.max_workers}[/bold blue]")
        if self.probe_services:
             console.print("[bold yellow][!] Chế độ Service Probing & OS Inference đang bật (Kết quả có độ trễ)[/bold yellow]")
             
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                for port in range(start_port, end_port + 1):
                    executor.submit(self.scan_port, port)
        except KeyboardInterrupt:
            console.print("\n[bold yellow][!] Quá trình quét bị người dùng hủy.[/bold yellow]")
            return

        self._display_results()

    def _display_results(self):
        if not self.open_ports:
            console.print("[bold red][-][/bold red] Không tìm thấy port nào đang mở.")
            return

        self.open_ports.sort(key=lambda x: x[0])

        table = Table(title=f"Báo cáo quét Port - IP: {self.target}")
        table.add_column("PORT", justify="right", style="cyan", no_wrap=True)
        table.add_column("STATUS", justify="center", style="green")
        
        if self.probe_services:
            table.add_column("THỰC TẾ (PROBE)", style="magenta")
            table.add_column("BANNER / VERSION", style="white")
            for port, real_service, banner in self.open_ports:
                table.add_row(f"{port}/tcp", "open", real_service, banner)
        else:
            table.add_column("DỰ ĐOÁN (DANH BẠ)", style="magenta")
            for port, guessed_service, _ in self.open_ports:
                table.add_row(f"{port}/tcp", "open", guessed_service)

        console.print(table)
        
        # In ra dự đoán Hệ điều hành nếu có
        if self.probe_services and self.os_guesses:
            # Loại bỏ các dự đoán trùng lặp và đếm số lần xuất hiện
            from collections import Counter
            os_counts = Counter(self.os_guesses)
            most_likely_os = os_counts.most_common(1)[0][0]
            
            console.print(f"\n[bold green][+] Dự đoán Hệ điều hành (OS Inference):[/bold green] [bold white]{most_likely_os}[/bold white]")