# network_map.py - نقشه شبکه گرافیکی

import socket
import subprocess
import re
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.tree import Tree
from utils import clear_screen, print_header, save_json_file, load_json_file
from scanner import get_ttl, detect_os_by_ttl, scan_port
from config import *

console = Console()

# فایل ذخیره نقشه
NETWORK_MAP_FILE = "network_map.json"

class NetworkNode:
    """کلاس گره شبکه"""
    def __init__(self, ip, mac=None, hostname=None, os_type=None, device_type=None):
        self.ip = ip
        self.mac = mac
        self.hostname = hostname
        self.os_type = os_type
        self.device_type = device_type
        self.ports = []
        self.last_seen = datetime.now()
        self.is_gateway = False
        self.is_local = False
    
    def to_dict(self):
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "os_type": self.os_type,
            "device_type": self.device_type,
            "ports": self.ports,
            "last_seen": self.last_seen.isoformat(),
            "is_gateway": self.is_gateway,
            "is_local": self.is_local
        }
    
    @classmethod
    def from_dict(cls, data):
        node = cls(data["ip"], data.get("mac"), data.get("hostname"), data.get("os_type"), data.get("device_type"))
        node.ports = data.get("ports", [])
        node.last_seen = datetime.fromisoformat(data["last_seen"]) if data.get("last_seen") else datetime.now()
        node.is_gateway = data.get("is_gateway", False)
        node.is_local = data.get("is_local", False)
        return node

class NetworkMap:
    """کلاس نقشه شبکه"""
    def __init__(self):
        self.nodes = {}
        self.gateway_ip = None
        self.local_ip = None
    
    def detect_gateway(self):
        """تشخیص گیت وی (مودم)"""
        try:
            result = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # پیدا کردن Default Gateway
            lines = result.stdout.split('\n')
            for line in lines:
                if "Default Gateway" in line and ":" in line:
                    gateway = line.split(":")[-1].strip()
                    if gateway and gateway != "None":
                        self.gateway_ip = gateway
                        return gateway
        except:
            pass
        
        # پیش‌فرض
        self.gateway_ip = "192.168.1.1"
        return self.gateway_ip
    
    def detect_local_ip(self):
        """تشخیص IP خود سیستم"""
        try:
            hostname = socket.gethostname()
            self.local_ip = socket.gethostbyname(hostname)
            return self.local_ip
        except:
            self.local_ip = "127.0.0.1"
            return self.local_ip
    
    def get_hostname(self, ip):
        """دریافت hostname از IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None
    
    def get_device_icon(self, device_type, os_type):
        """آیکون بر اساس نوع دستگاه"""
        if device_type == "gateway":
            return "🌐"
        elif device_type == "computer":
            return "🖥️"
        elif device_type == "mobile":
            return "📱"
        elif device_type == "printer":
            return "🖨️"
        elif device_type == "camera":
            return "📷"
        elif "Windows" in str(os_type):
            return "🪟"
        elif "Linux" in str(os_type):
            return "🐧"
        elif "Android" in str(os_type):
            return "🤖"
        elif "iPhone" in str(os_type) or "iOS" in str(os_type):
            return "🍎"
        else:
            return "🔌"
    
    def scan_network(self, base_ip=None):
        """اسکن شبکه و ساخت نقشه"""
        if base_ip is None:
            base_ip = ".".join(self.detect_local_ip().split(".")[:-1])
        
        self.detect_gateway()
        self.detect_local_ip()
        
        devices = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scanning network...", total=254)
            
            for i in range(1, 255):
                ip = f"{base_ip}.{i}"
                progress.update(task, description=f"Scanning {ip}")
                
                ttl = get_ttl(ip, timeout=0.5)
                
                if ttl:
                    os_name, icon = detect_os_by_ttl(ttl)
                    
                    # تشخیص نوع دستگاه
                    device_type = "unknown"
                    if ip == self.gateway_ip:
                        device_type = "gateway"
                    elif ip == self.local_ip:
                        device_type = "local"
                    elif "Windows" in os_name:
                        device_type = "computer"
                    elif "Android" in os_name or "iOS" in os_name:
                        device_type = "mobile"
                    else:
                        device_type = "device"
                    
                    hostname = self.get_hostname(ip)
                    
                    node = NetworkNode(
                        ip=ip,
                        hostname=hostname,
                        os_type=os_name,
                        device_type=device_type
                    )
                    node.is_gateway = (ip == self.gateway_ip)
                    node.is_local = (ip == self.local_ip)
                    
                    # اسکن پورت‌های معروف
                    common_ports = [80, 443, 22, 23, 445, 3389]
                    for port in common_ports:
                        if scan_port(ip, port, timeout=0.3):
                            node.ports.append(port)
                    
                    self.nodes[ip] = node
                    devices.append(node)
                
                progress.advance(task)
        
        return devices
    
    def display_text_map(self):
        """نمایش نقشه به صورت متنی"""
        clear_screen()
        print_header("NETWORK MAP")
        
        console.print(f"\n[cyan]Gateway (Router):[/cyan] {self.gateway_ip}")
        console.print(f"[cyan]Your IP:[/cyan] {self.local_ip}")
        console.print(f"[cyan]Total devices:[/cyan] {len(self.nodes)}")
        
        if not self.nodes:
            console.print("[yellow]No devices found. Run scan first![/yellow]")
            return
        
        # ایجاد درخت شبکه
        tree = Tree(f"🌐 Network ({self.gateway_ip})")
        
        # گروه‌بندی بر اساس نوع دستگاه
        gateways = []
        computers = []
        mobiles = []
        others = []
        
        for ip, node in self.nodes.items():
            if node.is_gateway:
                gateways.append(node)
            elif "computer" in node.device_type or "Windows" in node.os_type or "Linux" in node.os_type:
                computers.append(node)
            elif "mobile" in node.device_type or "Android" in node.os_type:
                mobiles.append(node)
            else:
                others.append(node)
        
        # گیت وی
        if gateways:
            gw_tree = tree.add(f"[bold red]🌐 Router[/bold red]")
            for gw in gateways:
                gw_tree.add(f"{self.get_device_icon(gw.device_type, gw.os_type)} {gw.ip} - {gw.os_type[:30]}")
        
        # کامپیوترها
        if computers:
            pc_tree = tree.add(f"[bold green]🖥️ Computers ({len(computers)})[/bold green]")
            for pc in computers:
                pc_info = f"{self.get_device_icon(pc.device_type, pc.os_type)} {pc.ip}"
                if pc.hostname:
                    pc_info += f" [{pc.hostname}]"
                pc_info += f" - {pc.os_type[:25]}"
                if pc.ports:
                    pc_info += f" [ports: {','.join(map(str, pc.ports))}]"
                pc_tree.add(pc_info)
        
        # موبایل‌ها
        if mobiles:
            mob_tree = tree.add(f"[bold yellow]📱 Mobile Devices ({len(mobiles)})[/bold yellow]")
            for mob in mobiles:
                mob_info = f"{self.get_device_icon(mob.device_type, mob.os_type)} {mob.ip}"
                if mob.hostname:
                    mob_info += f" [{mob.hostname}]"
                mob_tree.add(mob_info)
        
        # سایر دستگاه‌ها
        if others:
            other_tree = tree.add(f"[bold blue]🔌 Other Devices ({len(others)})[/bold blue]")
            for dev in others:
                other_tree.add(f"{self.get_device_icon(dev.device_type, dev.os_type)} {dev.ip} - {dev.os_type[:30]}")
        
        console.print(tree)
        
        # جدول جزئیات
        console.print(f"\n[bold cyan]📋 Device Details:[/bold cyan]")
        details_table = Table(show_header=True, header_style="bold cyan")
        details_table.add_column("IP", style="green", width=16)
        details_table.add_column("Type", style="yellow", width=12)
        details_table.add_column("OS", style="white", width=25)
        details_table.add_column("Ports", style="red", width=15)
        
        for node in self.nodes.values():
            details_table.add_row(
                node.ip,
                node.device_type,
                node.os_type[:25],
                ','.join(map(str, node.ports)) if node.ports else "-"
            )
        
        console.print(details_table)
    
    def save_map(self):
        """ذخیره نقشه در فایل"""
        data = {
            "gateway": self.gateway_ip,
            "local_ip": self.local_ip,
            "scan_time": datetime.now().isoformat(),
            "devices": {ip: node.to_dict() for ip, node in self.nodes.items()}
        }
        
        save_json_file(NETWORK_MAP_FILE, data)
        console.print(f"[green]✅ Network map saved to {NETWORK_MAP_FILE}[/green]")
    
    def load_map(self):
        """بارگذاری نقشه از فایل"""
        data = load_json_file(NETWORK_MAP_FILE, None)
        if not data:
            return False
        
        self.gateway_ip = data.get("gateway")
        self.local_ip = data.get("local_ip")
        self.nodes = {}
        
        for ip, node_data in data.get("devices", {}).items():
            self.nodes[ip] = NetworkNode.from_dict(node_data)
        
        return True
    
    def compare_maps(self, old_map):
        """مقایسه دو نقشه (تشخیص دستگاه جدید/حذف شده)"""
        old_ips = set(old_map.nodes.keys())
        new_ips = set(self.nodes.keys())
        
        new_devices = new_ips - old_ips
        removed_devices = old_ips - new_ips
        
        if new_devices:
            console.print(f"\n[red]⚠️ New devices detected: {len(new_devices)}[/red]")
            for ip in new_devices:
                console.print(f"  + {ip} - {self.nodes[ip].os_type}")
        
        if removed_devices:
            console.print(f"\n[yellow]📴 Devices removed: {len(removed_devices)}[/yellow]")
            for ip in removed_devices:
                console.print(f"  - {ip} - {old_map.nodes[ip].os_type}")
        
        return new_devices, removed_devices

def display_ascii_map(devices):
    """نمایش نقشه ساده ASCII"""
    if not devices:
        return
    
    clear_screen()
    print_header("ASCII NETWORK MAP")
    
    # پیدا کردن گیت وی
    gateway = next((d for d in devices if d.is_gateway), None)
    local = next((d for d in devices if d.is_local), None)
    others = [d for d in devices if not d.is_gateway and not d.is_local]
    
    # رسم نقشه ساده
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{GREEN}                    NETWORK TOPOLOGY{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")
    
    if gateway:
        print(f"                      {RED}🌐 [GATEWAY]{RESET}")
        print(f"                      {RED}  |{RESET}")
        print(f"                      {RED}  |{RESET}")
    
    print(f"                      {BLUE}  |{RESET}")
    print(f"                      {BLUE}  |{RESET}")
    print(f"    {GREEN}🖥️ [YOU] {local.ip if local else '?'}{RESET} <----{BLUE}主干网络{RESET}----> {RED}🌐 [INTERNET]{RESET}")
    print(f"                      {BLUE}  |{RESET}")
    print(f"                      {BLUE}  |{RESET}")
    
    # دستگاه‌های دیگر
    for i, device in enumerate(others[:10]):
        indent = " " * 20
        print(f"{indent} {YELLOW}├── {device.ip} - {device.os_type[:20]}{RESET}")
    
    if len(others) > 10:
        print(f"{indent} {YELLOW}└── ... and {len(others)-10} more devices{RESET}")
    
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{GREEN}Total devices: {len(devices)}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}")

def network_map_menu():
    """منوی نقشه شبکه"""
    network_map = NetworkMap()
    
    while True:
        clear_screen()
        print_header("NETWORK MAP")
        
        console.print("\n[1] Scan network and create map")
        console.print("[2] Load saved map")
        console.print("[3] Save current map")
        console.print("[4] Compare with previous scan")
        console.print("[5] Show ASCII map")
        console.print("[b] Back to main menu")
        
        choice = input(f"\n[yellow]👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            break
        
        elif choice == '1':
            console.print("\n[yellow]Scanning network... This may take a moment[/yellow]\n")
            devices = network_map.scan_network()
            network_map.display_text_map()
            
            save_choice = input(f"\n[yellow]Save this map? (y/n): {RESET}").strip().lower()
            if save_choice == 'y':
                network_map.save_map()
            
            input(f"\n[yellow]Press Enter to continue...{RESET}")
        
        elif choice == '2':
            if network_map.load_map():
                console.print("[green]Map loaded successfully[/green]")
                network_map.display_text_map()
            else:
                console.print("[red]No saved map found. Run scan first.[/red]")
            input(f"\n[yellow]Press Enter to continue...{RESET}")
        
        elif choice == '3':
            if network_map.nodes:
                network_map.save_map()
            else:
                console.print("[red]No map data. Run scan first.[/red]")
            input(f"\n[yellow]Press Enter to continue...{RESET}")
        
        elif choice == '4':
            old_map = NetworkMap()
            if old_map.load_map():
                if network_map.nodes:
                    network_map.compare_maps(old_map)
                else:
                    console.print("[yellow]Current map empty. Run scan first.[/yellow]")
            else:
                console.print("[red]No previous map found. Run scan first.[/red]")
            input(f"\n[yellow]Press Enter to continue...{RESET}")
        
        elif choice == '5':
            if network_map.nodes:
                display_ascii_map(list(network_map.nodes.values()))
            else:
                console.print("[red]No map data. Run scan first.[/red]")
            input(f"\n[yellow]Press Enter to continue...{RESET}")
        
        else:
            console.print("[red]Invalid choice[/red]")
            input(f"\nPress Enter...")