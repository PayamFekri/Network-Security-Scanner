import socket

# رنگ‌ها
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

# فایل‌ها
ALERT_LOG_FILE = "threat_alerts.json"
KNOWN_DEVICES_FILE = "known_devices.json"

# شبکه پیش‌فرض
try:
    my_ip = socket.gethostbyname(socket.gethostname())
    DEFAULT_NETWORK = ".".join(my_ip.split(".")[:-1])
except:
    DEFAULT_NETWORK = "192.168.1"

# پورت‌های بحرانی و هشدار
CRITICAL_PORTS = {
    21: "FTP (Anonymous access risk)",
    23: "Telnet (Unencrypted communication)",
    445: "SMB (Ransomware risk)",
    3389: "RDP (Brute force target)",
    5900: "VNC (Weak authentication risk)"
}

WARNING_PORTS = {
    22: "SSH (Check for weak passwords)",
    80: "HTTP (Consider using HTTPS)",
    3306: "MySQL (Default port, check access)",
    1433: "MSSQL (Default port, check access)"
}

# پورت‌های معروف برای اسکن
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445,
                993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8080]