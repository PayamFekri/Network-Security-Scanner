# action_mode.py - حالت اکشن خودکار

import time
import threading
import subprocess
from datetime import datetime
from rich.console import Console
from rich.table import Table

from utils import clear_screen, print_header, save_json_file, load_json_file
from scanner import quick_scan_network
from database_manager import db
from config import GREEN, RED, YELLOW, CYAN, BLUE, MAGENTA, RESET

console = Console()

# فایل تنظیمات حالت اکشن
ACTION_CONFIG_FILE = "action_mode_config.json"

class ActionMode:
    """کلاس مدیریت حالت اکشن"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.config = self.load_config()
        self.scan_history = []
        self.auto_fix_count = 0
    
    def load_config(self):
        """بارگذاری تنظیمات"""
        default_config = {
            "auto_scan_interval": 60,  # minutes
            "auto_save_to_db": True,
            "auto_close_ports": False,
            "auto_alert_sound": True,
            "auto_report_hour": 8,  # 8 AM daily report
            "last_scan_time": None,
            "enabled_features": {
                "network_scan": True,
                "threat_detection": True,
                "vulnerability_scan": True,
                "wifi_scan": False,
                "bandwidth_monitor": False
            }
        }
        
        data = load_json_file(ACTION_CONFIG_FILE, default_config)
        # اطمینان از وجود همه کلیدها
        for key, value in default_config.items():
            if key not in data:
                data[key] = value
        return data
    
    def save_config(self):
        """ذخیره تنظیمات"""
        save_json_file(ACTION_CONFIG_FILE, self.config)
    
    def start(self):
        """شروع حالت اکشن"""
        if self.running:
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self._action_loop, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        """توقف حالت اکشن"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _action_loop(self):
        """حلقه اصلی حالت اکشن"""
        console.print(f"{GREEN}✅ Action Mode Started!{RESET}")
        console.print(f"{CYAN}   Auto-scan every {self.config['auto_scan_interval']} minutes{RESET}")
        
        last_report_date = datetime.now().date()
        
        while self.running:
            try:
                # اسکن خودکار شبکه
                if self.config['enabled_features']['network_scan']:
                    self._auto_network_scan()
                
                # گزارش روزانه
                today = datetime.now().date()
                if today != last_report_date and datetime.now().hour >= self.config['auto_report_hour']:
                    self._generate_daily_report()
                    last_report_date = today
                
                # منتظر ماندن برای اسکن بعدی
                for _ in range(self.config['auto_scan_interval'] * 60):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                console.print(f"{RED}Error in action mode: {e}{RESET}")
                time.sleep(60)
    
    def _auto_network_scan(self):
        """اسکن خودکار شبکه"""
        console.print(f"\n{CYAN}[{datetime.now().strftime('%H:%M:%S')}] Running auto network scan...{RESET}")
        
        devices = quick_scan_network("192.168.1", 'fast', None)
        
        if devices:
            console.print(f"{GREEN}   Found {len(devices)} device(s){RESET}")
            
            # ذخیره در دیتابیس
            if self.config['auto_save_to_db']:
                db.save_network_scan("auto", devices)
                console.print(f"{BLUE}   Saved to database{RESET}")
            
            # بررسی تهدیدات
            if self.config['enabled_features']['threat_detection']:
                self._check_threats(devices)
            
            self.scan_history.append({
                "time": datetime.now(),
                "devices": len(devices),
                "devices_list": devices
            })
            
            # نگهداری فقط 50 تاریخچه آخر
            if len(self.scan_history) > 50:
                self.scan_history.pop(0)
    
    def _check_threats(self, devices):
        """بررسی تهدیدات در دستگاه‌های پیدا شده"""
        threats_found = []
        
        for device in devices:
            # اسکن پورت‌های رایج
            ip = device['ip']
            critical_ports = [21, 23, 445, 3389, 5900]
            
            for port in critical_ports:
                if port in device.get('ports', []):
                    threats_found.append({
                        "ip": ip,
                        "port": port,
                        "device": device['os']
                    })
                    
                    if self.config['auto_alert_sound']:
                        self._play_alert()
                    
                    console.print(f"{RED}   ⚠️ THREAT: {ip} - Port {port} open!{RESET}")
                    
                    # بستن خودکار پورت (اگر فعال باشه)
                    if self.config['auto_close_ports']:
                        self._close_port(ip, port)
        
        if threats_found:
            self._save_threat_report(threats_found)
    
    def _close_port(self, ip, port):
        """بستن خودکار پورت با فایروال ویندوز"""
        try:
            # فقط برای سیستم خودمون (127.0.0.1) می‌تونیم ببندیم
            if ip == "127.0.0.1" or ip.startswith("192.168.1.") and ip != "192.168.1.1":
                rule_name = f"Block_Port_{port}_Auto"
                subprocess.run([
                    "netsh", "advfirewall", "firewall", "add", "rule",
                    f"name={rule_name}", "dir=in", "action=block",
                    f"protocol=TCP", f"localport={port}"
                ], capture_output=True)
                console.print(f"{GREEN}   🔒 Port {port} blocked automatically{RESET}")
                self.auto_fix_count += 1
        except:
            pass
    
    def _play_alert(self):
        """پخش صدای هشدار"""
        try:
            import winsound
            winsound.Beep(1000, 300)
        except:
            pass
    
    def _save_threat_report(self, threats):
        """ذخیره گزارش تهدید"""
        filename = f"auto_threat_report_{datetime.now().strftime('%Y%m%d')}.json"
        existing = load_json_file(filename, [])
        existing.append({
            "time": datetime.now().isoformat(),
            "threats": threats
        })
        save_json_file(filename, existing)
    
    def _generate_daily_report(self):
        """تولید گزارش روزانه"""
        console.print(f"\n{CYAN}[{datetime.now().strftime('%H:%M:%S')}] Generating daily report...{RESET}")
        
        today = datetime.now().strftime('%Y%m%d')
        filename = f"daily_report_{today}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"DAILY SECURITY REPORT - {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Action Mode Status: {'Running' if self.running else 'Stopped'}\n")
            f.write(f"Auto-fixes applied: {self.auto_fix_count}\n")
            f.write(f"Scans performed today: {len([h for h in self.scan_history if h['time'].date() == datetime.now().date()])}\n\n")
            
            f.write("SCAN HISTORY:\n")
            f.write("-" * 40 + "\n")
            for hist in self.scan_history[-10:]:
                f.write(f"  {hist['time'].strftime('%H:%M:%S')} - {hist['devices']} devices\n")
            
            f.write("\n" + "=" * 60 + "\n")
        
        console.print(f"{GREEN}   Daily report saved to {filename}{RESET}")
    
    def show_status(self):
        """نمایش وضعیت فعلی"""
        console.print(f"\n{CYAN}{'='*50}{RESET}")
        console.print(f"{GREEN}📡 ACTION MODE STATUS{RESET}")
        console.print(f"{CYAN}{'='*50}{RESET}")
        
        status = "RUNNING" if self.running else "STOPPED"
        status_color = GREEN if self.running else RED
        console.print(f"\nStatus: {status_color}{status}{RESET}")
        
        console.print(f"\n{YELLOW}Settings:{RESET}")
        console.print(f"  Auto-scan interval: {self.config['auto_scan_interval']} minutes")
        console.print(f"  Auto-save to DB: {'✅' if self.config['auto_save_to_db'] else '❌'}")
        console.print(f"  Auto-close ports: {'✅' if self.config['auto_close_ports'] else '❌'}")
        console.print(f"  Auto-alert sound: {'✅' if self.config['auto_alert_sound'] else '❌'}")
        
        console.print(f"\n{BLUE}Statistics:{RESET}")
        console.print(f"  Total scans: {len(self.scan_history)}")
        console.print(f"  Auto-fixes: {self.auto_fix_count}")
        
        if self.scan_history:
            last = self.scan_history[-1]
            console.print(f"\n{CYAN}Last scan:{RESET}")
            console.print(f"  Time: {last['time'].strftime('%Y-%m-%d %H:%M:%S')}")
            console.print(f"  Devices found: {last['devices']}")

def show_action_menu():
    """نمایش منوی حالت اکشن"""
    action = ActionMode()
    
    while True:
        clear_screen()
        print_header("ACTION MODE (AUTO) 🔧")
        
        console.print("\n[bold cyan]🤖 Automated Security Mode[/bold cyan]")
        console.print("[dim]Let the program do everything automatically[/dim]\n")
        
        if action.running:
            console.print(f"{GREEN}✅ STATUS: RUNNING{RESET}")
            console.print(f"   Auto-scan every {action.config['auto_scan_interval']} minutes")
            console.print(f"\n[1] Stop Action Mode")
            console.print("[2] Show status")
            console.print("[3] Show scan history")
            console.print("[4] Configure settings")
        else:
            console.print(f"{RED}❌ STATUS: STOPPED{RESET}")
            console.print(f"\n[1] Start Action Mode")
            console.print("[2] Configure settings before start")
        
        console.print("[b] Back to main menu")
        
        choice = input(f"\n{YELLOW}👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            if action.running:
                action.stop()
            break
        
        elif choice == '1' and not action.running:
            action.start()
            console.print(f"{GREEN}Action Mode started!{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '1' and action.running:
            action.stop()
            console.print(f"{YELLOW}Action Mode stopped{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '2' and action.running:
            action.show_status()
            input(f"\nPress Enter...")
        
        elif choice == '2' and not action.running or choice == '4':
            # تنظیمات
            clear_screen()
            print_header("ACTION MODE SETTINGS")
            
            console.print(f"\n{CYAN}Current Settings:{RESET}")
            console.print(f"  1. Auto-scan interval: {action.config['auto_scan_interval']} minutes")
            console.print(f"  2. Auto-save to database: {'ON' if action.config['auto_save_to_db'] else 'OFF'}")
            console.print(f"  3. Auto-close dangerous ports: {'ON' if action.config['auto_close_ports'] else 'OFF'}")
            console.print(f"  4. Alert sound: {'ON' if action.config['auto_alert_sound'] else 'OFF'}")
            console.print(f"  5. Daily report hour: {action.config['auto_report_hour']}:00")
            
            console.print(f"\n{YELLOW}Enter setting number to change (or Enter to save & exit):{RESET}")
            setting = input(f"👉 ").strip()
            
            if setting == '1':
                try:
                    new_val = int(input(f"New interval (minutes, 15-1440): "))
                    if 15 <= new_val <= 1440:
                        action.config['auto_scan_interval'] = new_val
                except:
                    pass
            elif setting == '2':
                action.config['auto_save_to_db'] = not action.config['auto_save_to_db']
            elif setting == '3':
                action.config['auto_close_ports'] = not action.config['auto_close_ports']
                if action.config['auto_close_ports']:
                    console.print(f"{YELLOW}⚠️ Warning: Auto-closing ports may block legitimate apps{RESET}")
            elif setting == '4':
                action.config['auto_alert_sound'] = not action.config['auto_alert_sound']
            elif setting == '5':
                try:
                    new_val = int(input(f"New report hour (0-23): "))
                    if 0 <= new_val <= 23:
                        action.config['auto_report_hour'] = new_val
                except:
                    pass
            
            action.save_config()
            console.print(f"{GREEN}Settings saved!{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '3' and action.running:
            if action.scan_history:
                table = Table(title="Scan History")
                table.add_column("Time", style="cyan")
                table.add_column("Devices", style="green")
                
                for hist in action.scan_history[-20:]:
                    table.add_row(
                        hist['time'].strftime('%H:%M:%S'),
                        str(hist['devices'])
                    )
                console.print(table)
            else:
                console.print(f"{YELLOW}No scans yet{RESET}")
            input(f"\nPress Enter...")
        
        else:
            console.print(f"{RED}Invalid choice{RESET}")
            input(f"\nPress Enter...")