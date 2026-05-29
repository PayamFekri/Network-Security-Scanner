# database_manager.py - مدیریت دیتابیس SQLite

import sqlite3
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from utils import clear_screen, print_header
from config import GREEN, RED, YELLOW, CYAN, BLUE, RESET,MAGENTA

console = Console()

DB_PATH = "network_scanner.db"

class DatabaseManager:
    """کلاس مدیریت دیتابیس"""
    
    def __init__(self):
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """ایجاد جداول دیتابیس"""
        self.conn = sqlite3.connect(DB_PATH)
        cursor = self.conn.cursor()
        
        # جدول اسکن‌های شبکه
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_time TIMESTAMP,
                scan_type TEXT,
                total_devices INTEGER,
                devices_json TEXT,
                threats_found INTEGER
            )
        ''')
        
        # جدول دستگاه‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                hostname TEXT,
                os_type TEXT,
                device_type TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                times_seen INTEGER,
                ports_json TEXT,
                UNIQUE(ip)
            )
        ''')
        
        # جدول آسیب‌پذیری‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                ip TEXT,
                port INTEGER,
                vulnerability_name TEXT,
                risk_level TEXT,
                details TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY (scan_id) REFERENCES network_scans(id)
            )
        ''')
        
        # جدول وای‌فای اسکن‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wifi_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_time TIMESTAMP,
                ssid TEXT,
                bssid TEXT,
                signal INTEGER,
                channel INTEGER,
                band TEXT,
                auth TEXT
            )
        ''')
        
        # جدول قطعی‌های اینترنت
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS internet_outages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration REAL
            )
        ''')
        
        self.conn.commit()
    
    def save_network_scan(self, scan_type, devices, threats_found=0):
        """ذخیره اسکن شبکه در دیتابیس"""
        cursor = self.conn.cursor()
        
        devices_json = json.dumps(devices, default=str)
        
        cursor.execute('''
            INSERT INTO network_scans (scan_time, scan_type, total_devices, devices_json, threats_found)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now(), scan_type, len(devices), devices_json, threats_found))
        
        scan_id = cursor.lastrowid
        
        # به‌روزرسانی جدول دستگاه‌ها
        for device in devices:
            self.update_device_record(device, scan_id)
        
        self.conn.commit()
        console.print(f"{GREEN}✅ Network scan saved to database (ID: {scan_id}){RESET}")
        return scan_id
    
    def update_device_record(self, device, scan_id):
        """به‌روزرسانی یا ایجاد دستگاه در دیتابیس"""
        cursor = self.conn.cursor()
        
        ip = device.get('ip')
        hostname = device.get('hostname', '')
        os_type = device.get('os', 'Unknown')
        device_type = device.get('device_type', 'unknown')
        ports_json = json.dumps(device.get('ports', []))
        
        cursor.execute('''
            SELECT id, times_seen FROM devices WHERE ip = ?
        ''', (ip,))
        
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE devices 
                SET last_seen = ?, times_seen = times_seen + 1,
                    hostname = ?, os_type = ?, device_type = ?, ports_json = ?
                WHERE ip = ?
            ''', (datetime.now(), hostname, os_type, device_type, ports_json, ip))
        else:
            cursor.execute('''
                INSERT INTO devices (ip, hostname, os_type, device_type, first_seen, last_seen, times_seen, ports_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ip, hostname, os_type, device_type, datetime.now(), datetime.now(), 1, ports_json))
        
        self.conn.commit()
    
    def save_vulnerability(self, scan_id, ip, port, vuln_name, risk_level, details):
        """ذخیره آسیب‌پذیری در دیتابیس"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vulnerabilities (scan_id, ip, port, vulnerability_name, risk_level, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (scan_id, ip, port, vuln_name, risk_level, details, datetime.now()))
        self.conn.commit()
    
    def save_wifi_scan(self, networks):
        """ذخیره اسکن وای‌فای"""
        cursor = self.conn.cursor()
        scan_time = datetime.now()
        
        for net in networks:
            cursor.execute('''
                INSERT INTO wifi_scans (scan_time, ssid, bssid, signal, channel, band, auth)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (scan_time, net.get('ssid'), net.get('bssid'), net.get('signal'), 
                  net.get('channel'), net.get('band'), net.get('auth')))
        
        self.conn.commit()
        console.print(f"{GREEN}✅ Wi-Fi scan saved to database ({len(networks)} networks){RESET}")
    
    def save_internet_outage(self, start_time, end_time, duration):
        """ذخیره قطعی اینترنت"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO internet_outages (start_time, end_time, duration)
            VALUES (?, ?, ?)
        ''', (start_time, end_time, duration))
        self.conn.commit()
    
    def get_scan_history(self, limit=20):
        """دریافت تاریخچه اسکن‌ها"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, scan_time, scan_type, total_devices, threats_found
            FROM network_scans
            ORDER BY scan_time DESC
            LIMIT ?
        ''', (limit,))
        
        return cursor.fetchall()
    
    def get_devices_history(self, ip=None):
        """دریافت تاریخچه دستگاه‌ها"""
        cursor = self.conn.cursor()
        
        if ip:
            cursor.execute('''
                SELECT ip, hostname, os_type, device_type, first_seen, last_seen, times_seen, ports_json
                FROM devices WHERE ip = ?
            ''', (ip,))
        else:
            cursor.execute('''
                SELECT ip, hostname, os_type, device_type, first_seen, last_seen, times_seen, ports_json
                FROM devices
                ORDER BY last_seen DESC
            ''')
        
        return cursor.fetchall()
    
    def get_new_devices_since(self, days=7):
        """دریافت دستگاه‌های جدید در روزهای اخیر"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ip, hostname, os_type, first_seen, times_seen
            FROM devices
            WHERE first_seen > datetime('now', ?)
            ORDER BY first_seen DESC
        ''', (f'-{days} days',))
        
        return cursor.fetchall()
    
    def get_statistics(self):
        """دریافت آمار کلی"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # تعداد کل اسکن‌ها
        cursor.execute('SELECT COUNT(*) FROM network_scans')
        stats['total_scans'] = cursor.fetchone()[0]
        
        # تعداد کل دستگاه‌ها
        cursor.execute('SELECT COUNT(*) FROM devices')
        stats['total_devices'] = cursor.fetchone()[0]
        
        # تعداد آسیب‌پذیری‌ها
        cursor.execute('SELECT COUNT(*) FROM vulnerabilities')
        stats['total_vulnerabilities'] = cursor.fetchone()[0]
        
        # تعداد قطعی‌های اینترنت
        cursor.execute('SELECT COUNT(*) FROM internet_outages')
        stats['total_outages'] = cursor.fetchone()[0]
        
        # آخرین اسکن
        cursor.execute('SELECT scan_time, scan_type FROM network_scans ORDER BY scan_time DESC LIMIT 1')
        last = cursor.fetchone()
        stats['last_scan'] = last[0] if last else 'Never'
        stats['last_scan_type'] = last[1] if last else 'N/A'
        
        return stats
    
    def export_to_json(self, filename=None):
        """خروجی گرفتن از کل دیتابیس به JSON"""
        if not filename:
            filename = f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_time": datetime.now().isoformat(),
            "scans": [],
            "devices": [],
            "vulnerabilities": [],
            "wifi_scans": [],
            "outages": []
        }
        
        # اسکن‌ها
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM network_scans')
        for row in cursor.fetchall():
            export_data["scans"].append({
                "id": row[0], "scan_time": row[1], "scan_type": row[2],
                "total_devices": row[3], "devices_json": row[4], "threats_found": row[5]
            })
        
        # دستگاه‌ها
        cursor.execute('SELECT * FROM devices')
        for row in cursor.fetchall():
            export_data["devices"].append({
                "id": row[0], "ip": row[1], "hostname": row[2],
                "os_type": row[3], "device_type": row[4],
                "first_seen": row[5], "last_seen": row[6],
                "times_seen": row[7], "ports_json": row[8]
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        console.print(f"{GREEN}✅ Database exported to {filename}{RESET}")
        return filename
    
    def close(self):
        """بستن اتصال دیتابیس"""
        if self.conn:
            self.conn.close()

# نمونه گلوبال
db = DatabaseManager()

def show_statistics():
    """نمایش آمار دیتابیس"""
    stats = db.get_statistics()
    
    console.print(f"\n{CYAN}{'='*50}{RESET}")
    console.print(f"{GREEN}📊 DATABASE STATISTICS{RESET}")
    console.print(f"{CYAN}{'='*50}{RESET}")
    
    console.print(f"\n{YELLOW}📁 Total Scans:{RESET} {stats['total_scans']}")
    console.print(f"{BLUE}🖥️ Total Devices:{RESET} {stats['total_devices']}")
    console.print(f"{RED}🚨 Total Vulnerabilities:{RESET} {stats['total_vulnerabilities']}")
    console.print(f"{MAGENTA}🌐 Total Internet Outages:{RESET} {stats['total_outages']}")
    console.print(f"\n{CYAN}Last Scan:{RESET} {stats['last_scan']} ({stats['last_scan_type']})")

def show_scan_history():
    """نمایش تاریخچه اسکن‌ها"""
    scans = db.get_scan_history(20)
    
    if not scans:
        console.print(f"{YELLOW}No scans found in database{RESET}")
        return
    
    table = Table(title="Scan History")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Time", style="green", width=20)
    table.add_column("Type", style="yellow", width=15)
    table.add_column("Devices", style="blue", width=8)
    table.add_column("Threats", style="red", width=8)
    
    for scan in scans:
        table.add_row(
            str(scan[0]),
            scan[1][:19] if scan[1] else "N/A",
            scan[2],
            str(scan[3]),
            str(scan[4])
        )
    
    console.print(table)

def show_devices():
    """نمایش لیست دستگاه‌ها"""
    devices = db.get_devices_history()
    
    if not devices:
        console.print(f"{YELLOW}No devices found in database{RESET}")
        return
    
    table = Table(title="Devices History")
    table.add_column("IP", style="cyan", width=16)
    table.add_column("OS", style="green", width=25)
    table.add_column("First Seen", style="yellow", width=20)
    table.add_column("Times", style="blue", width=8)
    
    for device in devices:
        table.add_row(
            device[0],
            device[2][:25] if device[2] else "Unknown",
            device[4][:19] if device[4] else "N/A",
            str(device[6])
        )
    
    console.print(table)

def show_new_devices():
    """نمایش دستگاه‌های جدید"""
    new_devices = db.get_new_devices_since(7)
    
    if not new_devices:
        console.print(f"{GREEN}No new devices in the last 7 days{RESET}")
        return
    
    console.print(f"\n{YELLOW}📱 New devices in last 7 days:{RESET}\n")
    
    for device in new_devices:
        console.print(f"  {GREEN}{device[0]}{RESET} - {device[2]} (First seen: {device[3][:19]})")

def database_menu():
    """منوی مدیریت دیتابیس"""
    while True:
        clear_screen()
        print_header("DATABASE MANAGER")
        
        console.print("\n[bold cyan]🗄️ SQLite Database - Store all scan results[/bold cyan]\n")
        
        console.print("[1] Show statistics")
        console.print("[2] Show scan history")
        console.print("[3] Show all devices")
        console.print("[4] Show new devices (last 7 days)")
        console.print("[5] Export database to JSON")
        console.print("[b] Back to main menu")
        
        choice = input(f"\n{YELLOW}👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            break
        elif choice == '1':
            show_statistics()
            input(f"\nPress Enter...")
        elif choice == '2':
            show_scan_history()
            input(f"\nPress Enter...")
        elif choice == '3':
            show_devices()
            input(f"\nPress Enter...")
        elif choice == '4':
            show_new_devices()
            input(f"\nPress Enter...")
        elif choice == '5':
            filename = input(f"{YELLOW}Filename (Enter for auto): {RESET}").strip()
            if not filename:
                filename = None
            db.export_to_json(filename)
            input(f"\nPress Enter...")
        else:
            console.print(f"{RED}Invalid choice{RESET}")
            input(f"\nPress Enter...")