# internet_monitor.py - اینترنت مانیتور کامل

import time
import socket
import threading
from datetime import datetime
from utils import clear_screen, print_header, save_json_file, load_json_file

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
RESET = '\033[0m'

class InternetMonitor:
    def __init__(self):
        self.is_connected = False
        self.last_check = None
        self.outages = []
        self.running = False
        self.check_thread = None
        self.check_interval = 10  # seconds
        self.check_targets = ["8.8.8.8", "1.1.1.1", "4.2.2.4"]
    
    def check_internet(self):
        """چک کردن اتصال اینترنت"""
        for target in self.check_targets:
            try:
                socket.create_connection((target, 53), timeout=3)
                return True
            except:
                continue
        return False
    
    def start_monitoring(self):
        """شروع مانیتورینگ"""
        if self.running:
            return
        
        self.running = True
        self.is_connected = self.check_internet()
        self.last_check = datetime.now()
        
        self.check_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.check_thread.start()
        print(f"{GREEN}✅ Internet monitoring started{RESET}")
        print(f"{CYAN}   Checking every {self.check_interval} seconds{RESET}")
    
    def stop_monitoring(self):
        """توقف مانیتورینگ"""
        self.running = False
        if self.check_thread:
            self.check_thread.join(timeout=2)
        print(f"{YELLOW}🛑 Internet monitoring stopped{RESET}")
    
    def _monitor_loop(self):
        """حلقه اصلی مانیتورینگ"""
        last_state = self.is_connected
        outage_start = None
        
        while self.running:
            current_state = self.check_internet()
            now = datetime.now()
            
            # قطعی جدید
            if last_state and not current_state:
                outage_start = now
                print(f"\n{RED}🔴 INTERNET DOWN at {now.strftime('%H:%M:%S')}{RESET}")
            
            # برگشت نت
            if not last_state and current_state and outage_start:
                duration = (now - outage_start).total_seconds()
                self.outages.append({
                    'start': outage_start.isoformat(),
                    'end': now.isoformat(),
                    'duration': duration
                })
                print(f"\n{GREEN}🟢 INTERNET BACK after {duration:.1f} seconds at {now.strftime('%H:%M:%S')}{RESET}")
                
                # ذخیره خودکار در فایل
                self._save_outage_report()
                outage_start = None
            
            last_state = current_state
            self.is_connected = current_state
            self.last_check = now
            
            time.sleep(self.check_interval)
    
    def _save_outage_report(self):
        """ذخیره گزارش قطعی در فایل"""
        if not self.outages:
            return
        
        today = datetime.now().strftime('%Y%m%d')
        filename = f"internet_outages_{today}.json"
        
        # بارگذاری قطعی‌های قبلی امروز
        existing = load_json_file(filename, [])
        
        # اضافه کردن قطعی‌های جدید
        for outage in self.outages:
            if outage not in existing:
                existing.append(outage)
        
        save_json_file(filename, existing)
    
    def show_status(self):
        """نمایش وضعیت فعلی"""
        print(f"\n{CYAN}{'='*50}{RESET}")
        print(f"{GREEN}📡 INTERNET STATUS{RESET}")
        print(f"{CYAN}{'='*50}{RESET}")
        
        status_icon = "🟢 ONLINE" if self.is_connected else "🔴 OFFLINE"
        status_color = GREEN if self.is_connected else RED
        print(f"Status: {status_color}{status_icon}{RESET}")
        print(f"Last check: {self.last_check.strftime('%H:%M:%S') if self.last_check else 'Never'}")
        print(f"Check interval: {self.check_interval} seconds")
        
        total_outages = len(self.outages)
        print(f"\n{YELLOW}Total outages today: {total_outages}{RESET}")
        
        if self.outages:
            total_downtime = sum(o['duration'] for o in self.outages)
            avg_downtime = total_downtime / len(self.outages)
            print(f"Total downtime: {total_downtime:.0f} seconds ({total_downtime/60:.1f} minutes)")
            print(f"Average outage: {avg_downtime:.1f} seconds")
            
            last_outage = self.outages[-1]
            last_start = datetime.fromisoformat(last_outage['start'])
            print(f"\nLast outage: {last_outage['duration']:.1f} seconds at {last_start.strftime('%H:%M:%S')}")
    
    def show_history(self):
        """نمایش تاریخچه قطعی‌ها"""
        if not self.outages:
            print(f"\n{YELLOW}📭 No outages recorded yet{RESET}")
            return
        
        print(f"\n{CYAN}{'='*55}{RESET}")
        print(f"{GREEN}📜 INTERNET OUTAGE HISTORY{RESET}")
        print(f"{CYAN}{'='*55}{RESET}")
        print(f"{'Start Time':<12} {'End Time':<12} {'Duration':<10}")
        print(f"{'-'*55}")
        
        for outage in self.outages[-20:]:  # آخرین 20 قطعی
            start = datetime.fromisoformat(outage['start'])
            end = datetime.fromisoformat(outage['end'])
            duration = outage['duration']
            
            bar = self._get_duration_bar(duration)
            print(f"{start.strftime('%H:%M:%S'):<12} {end.strftime('%H:%M:%S'):<12} {duration:>5.1f}s {bar}")
        
        print(f"{CYAN}{'='*55}{RESET}")
    
    def _get_duration_bar(self, duration):
        """نوار گرافیکی برای مدت زمان قطعی"""
        if duration < 10:
            return "█"
        elif duration < 30:
            return "██"
        elif duration < 60:
            return "███"
        elif duration < 120:
            return "████"
        else:
            return "█████"
    
    def save_report(self):
        """ذخیره گزارش کامل"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"internet_report_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("INTERNET MONITORING REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Status: {'ONLINE' if self.is_connected else 'OFFLINE'}\n")
            f.write(f"Total outages: {len(self.outages)}\n")
            
            if self.outages:
                total_downtime = sum(o['duration'] for o in self.outages)
                f.write(f"Total downtime: {total_downtime:.0f} seconds\n\n")
                f.write("Outage Details:\n")
                f.write("-" * 40 + "\n")
                for i, o in enumerate(self.outages, 1):
                    start = datetime.fromisoformat(o['start'])
                    end = datetime.fromisoformat(o['end'])
                    f.write(f"{i}. {start.strftime('%H:%M:%S')} -> {end.strftime('%H:%M:%S')} ({o['duration']:.1f}s)\n")
        
        print(f"{GREEN}✅ Report saved to {filename}{RESET}")

# نمونه گلوبال
monitor = InternetMonitor()

def internet_monitor_menu():
    """منوی اینترنت مانیتور"""
    while True:
        clear_screen()
        print_header("INTERNET MONITOR")
        
        print(f"\n{CYAN}This tool monitors your internet connection and logs outages{RESET}\n")
        
        if monitor.running:
            print(f"{GREEN}✅ STATUS: RUNNING{RESET}")
            print(f"{CYAN}   Checking every {monitor.check_interval} seconds{RESET}")
            print(f"\n{BLUE}[1]{RESET} Stop monitoring")
            print(f"{BLUE}[2]{RESET} Show current status")
            print(f"{BLUE}[3]{RESET} Show outage history")
            print(f"{BLUE}[4]{RESET} Save report")
            print(f"{BLUE}[5]{RESET} Change interval")
        else:
            print(f"{RED}❌ STATUS: STOPPED{RESET}")
            print(f"\n{BLUE}[1]{RESET} Start monitoring (10 sec interval)")
            print(f"{BLUE}[2]{RESET} Start monitoring (30 sec interval)")
            print(f"{BLUE}[3]{RESET} Start monitoring (60 sec interval)")
            print(f"{BLUE}[4]{RESET} Show saved reports")
        
        print(f"{BLUE}[b]{RESET} Back to main menu")
        
        choice = input(f"\n{YELLOW}👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            if monitor.running:
                monitor.stop_monitoring()
            break
        
        elif not monitor.running:
            intervals = {'1': 10, '2': 30, '3': 60}
            if choice in intervals:
                monitor.check_interval = intervals[choice]
                monitor.start_monitoring()
                input(f"\n{YELLOW}Press Enter to continue...{RESET}")
            elif choice == '4':
                # نمایش گزارش‌های ذخیره شده
                import os
                reports = [f for f in os.listdir('.') if f.startswith('internet_outages_')]
                if reports:
                    print(f"\n{CYAN}Saved reports:{RESET}")
                    for r in reports[-10:]:
                        print(f"  - {r}")
                else:
                    print(f"\n{YELLOW}No saved reports found{RESET}")
                input(f"\n{YELLOW}Press Enter...{RESET}")
            else:
                print(f"{RED}Invalid choice{RESET}")
                input(f"\n{YELLOW}Press Enter...{RESET}")
        
        elif monitor.running:
            if choice == '1':
                monitor.stop_monitoring()
                input(f"\n{YELLOW}Press Enter...{RESET}")
            elif choice == '2':
                monitor.show_status()
                input(f"\n{YELLOW}Press Enter...{RESET}")
            elif choice == '3':
                monitor.show_history()
                input(f"\n{YELLOW}Press Enter...{RESET}")
            elif choice == '4':
                monitor.save_report()
                input(f"\n{YELLOW}Press Enter...{RESET}")
            elif choice == '5':
                try:
                    new_interval = int(input(f"{YELLOW}New interval (seconds): {RESET}"))
                    if new_interval >= 5:
                        monitor.check_interval = new_interval
                        print(f"{GREEN}Interval changed to {new_interval} seconds{RESET}")
                    else:
                        print(f"{RED}Interval must be at least 5 seconds{RESET}")
                except:
                    print(f"{RED}Invalid input{RESET}")
                input(f"\n{YELLOW}Press Enter...{RESET}")
            else:
                print(f"{RED}Invalid choice{RESET}")
                input(f"\n{YELLOW}Press Enter...{RESET}")