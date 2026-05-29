import socket
import subprocess
import re
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from config import *
from utils import load_json_file, save_json_file

def get_ttl(ip, timeout=1):
    """دریافت TTL از پینگ"""
    try:
        output = subprocess.run(
            ["ping", "-n", "1", "-w", str(timeout*1000), ip],
            capture_output=True,
            text=True,
            timeout=timeout+0.5
        )
        match = re.search(r"TTL=(\d+)", output.stdout, re.IGNORECASE)
        if match:
            return int(match.group(1))
    except:
        pass
    return None

def detect_os_by_ttl(ttl):
    """تشخیص OS از روی TTL"""
    if ttl is None:
        return "Unknown", "?"
    
    if ttl <= 64:
        if ttl >= 60:
            return "Linux / macOS / Android", "🐧"
        elif ttl >= 50:
            return "Linux (older)", "🔵"
    elif ttl <= 128:
        if ttl >= 120:
            return "Windows", "🪟"
        elif ttl >= 110:
            return "Windows Server", "📡"
    elif ttl <= 255:
        return "Router / Switch", "📶"
    
    return "Unknown OS", "❓"

def scan_port(host, port, timeout=0.3):
    """اسکن یک پورت"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_service_name(port):
    """نام سرویس برای پورت"""
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
        139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
        445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
        5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy"
    }
    return services.get(port, "Unknown")

def quick_scan_network(base_ip, speed='fast', callback=None):
    """اسکن سریع شبکه با نوار پیشرفت"""
    speed_settings = {'fast': 0.2, 'normal': 0.5, 'slow': 1.0}
    timeout = speed_settings.get(speed, 0.2)
    
    devices = []
    
    with Progress(
        TextColumn("[cyan]Scanning network[/cyan]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=None
    ) as progress:
        # اصلاح: استفاده از add_task به جای add_total
        task = progress.add_task("[cyan]Scanning IPs...[/cyan]", total=254)
        
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            progress.update(task, advance=1, description=f"Scanning {ip}")
            
            ttl = get_ttl(ip, timeout)
            
            if ttl:
                os_name, icon = detect_os_by_ttl(ttl)
                
                device = {
                    "ip": ip,
                    "os": os_name,
                    "icon": icon,
                    "ttl": ttl,
                    "ports": []
                }
                devices.append(device)
                
                if callback:
                    callback(device)
    
    return devices

def scan_single_device(ip, callback=None):
    """اسکن کامل یک دستگاه (با پورت)"""
    print(f"\n[*] Scanning {ip}...")
    
    ttl = get_ttl(ip)
    if ttl is None:
        print(f"[!] Host {ip} is down")
        return None
    
    os_name, icon = detect_os_by_ttl(ttl)
    open_ports = []
    
    with Progress(
        TextColumn("[cyan]Port scanning[/cyan]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=None
    ) as progress:
        # اصلاح: استفاده از add_task به جای add_total
        task = progress.add_task("[cyan]Scanning ports...[/cyan]", total=len(COMMON_PORTS))
        
        for port in COMMON_PORTS:
            progress.update(task, advance=1, description=f"Checking port {port}")
            
            if scan_port(ip, port):
                open_ports.append(port)
    
    result = {
        "ip": ip,
        "os": os_name,
        "icon": icon,
        "ttl": ttl,
        "ports": open_ports
    }
    
    if callback:
        callback(result)
    
    return result

def is_unknown_device(ip):
    """بررسی ناشناس بودن دستگاه"""
    known = load_json_file(KNOWN_DEVICES_FILE, [])
    return ip not in known

def add_known_device(ip):
    """افزودن به لیست شناخته شده"""
    known = load_json_file(KNOWN_DEVICES_FILE, [])
    if ip not in known:
        known.append(ip)
        save_json_file(KNOWN_DEVICES_FILE, known)
        return True
    return False