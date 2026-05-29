# bandwidth_monitor.py - نسخه اصلاح شده بدون خطای gray

import time
import threading
import psutil
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from utils import clear_screen, print_header
from config import GREEN, RED, YELLOW, CYAN, BLUE, MAGENTA, RESET

console = Console()

class BandwidthMonitor:
    """کلاس مانیتورینگ دقیق پهنای باند با psutil"""
    
    def __init__(self):
        self.running = False
        self.monitor_thread = None
        self.interval = 2
        self.history = []
        self.max_history = 120
        self.last_net_io = None
        self.last_time = None
    
    def get_network_stats(self):
        """دریافت آمار دقیق شبکه با psutil"""
        net_io = psutil.net_io_counters()
        
        if self.last_net_io is None:
            self.last_net_io = net_io
            self.last_time = time.time()
            return {
                "sent": 0,
                "recv": 0,
                "sent_rate": 0,
                "recv_rate": 0,
                "total_sent": net_io.bytes_sent,
                "total_recv": net_io.bytes_recv,
                "timestamp": datetime.now()
            }
        
        time_diff = time.time() - self.last_time
        sent_diff = net_io.bytes_sent - self.last_net_io.bytes_sent
        recv_diff = net_io.bytes_recv - self.last_net_io.bytes_recv
        
        sent_rate = sent_diff / time_diff if time_diff > 0 else 0
        recv_rate = recv_diff / time_diff if time_diff > 0 else 0
        
        self.last_net_io = net_io
        self.last_time = time.time()
        
        return {
            "sent": sent_diff,
            "recv": recv_diff,
            "sent_rate": sent_rate,
            "recv_rate": recv_rate,
            "total_sent": net_io.bytes_sent,
            "total_recv": net_io.bytes_recv,
            "timestamp": datetime.now()
        }
    
    def get_interface_details(self):
        """دریافت جزئیات همه اینترفیس‌های شبکه"""
        interfaces = []
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()
        
        for name, stat in stats.items():
            if stat.isup:
                interface_info = {
                    "name": name,
                    "speed": stat.speed,
                    "mtu": stat.mtu,
                    "is_up": stat.isup,
                    "addresses": []
                }
                
                for addr in addrs.get(name, []):
                    interface_info["addresses"].append({
                        "family": str(addr.family),
                        "address": addr.address
                    })
                
                interfaces.append(interface_info)
        
        return interfaces
    
    def get_process_bandwidth(self):
        """دریافت مصرف پهنای باند هر فرآیند"""
        processes = []
        
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED' and conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    processes.append({
                        "pid": conn.pid,
                        "name": proc.name(),
                        "laddr": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "status": conn.status
                    })
                except:
                    pass
        
        return processes
    
    def start_monitoring(self):
        """شروع مانیتورینگ"""
        if self.running:
            return
        
        self.running = True
        self.history = []
        self.last_net_io = None
        self.last_time = None
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        console.print(f"{GREEN}✅ Bandwidth monitoring started (interval: {self.interval}s){RESET}")
    
    def stop_monitoring(self):
        """توقف مانیتورینگ"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        console.print(f"{YELLOW}🛑 Bandwidth monitoring stopped{RESET}")
    
    def _monitor_loop(self):
        """حلقه اصلی مانیتورینگ"""
        while self.running:
            data = self.get_network_stats()
            self.history.append(data)
            
            if len(self.history) > self.max_history:
                self.history.pop(0)
            
            time.sleep(self.interval)
    
    def get_current_stats(self):
        """دریافت آمار فعلی"""
        if not self.history:
            return None
        return self.history[-1]
    
    def get_average_speed(self, seconds=60):
        """دریافت میانگین سرعت در چند ثانیه اخیر"""
        if not self.history:
            return 0, 0
        
        recent = [h for h in self.history if (datetime.now() - h['timestamp']).total_seconds() <= seconds]
        
        if not recent:
            return 0, 0
        
        avg_sent = sum(h['sent_rate'] for h in recent) / len(recent)
        avg_recv = sum(h['recv_rate'] for h in recent) / len(recent)
        
        return avg_sent, avg_recv
    
    def get_peak_speed(self):
        """دریافت حداکثر سرعت ثبت شده"""
        if not self.history:
            return 0, 0
        
        peak_sent = max(h['sent_rate'] for h in self.history)
        peak_recv = max(h['recv_rate'] for h in self.history)
        
        return peak_sent, peak_recv

def format_bytes(bytes_val):
    """تبدیل بایت به فرمت خوانا"""
    if bytes_val < 1024:
        return f"{bytes_val:.0f} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    elif bytes_val < 1024 * 1024 * 1024:
        return f"{bytes_val / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"

def format_speed(bytes_per_sec):
    """تبدیل سرعت به فرمت خوانا"""
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.0f} B/s"
    elif bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    else:
        return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"

def create_speed_bar(rate_bps, max_rate=10*1024*1024):
    """ساخت نوار گرافیکی برای سرعت"""
    if rate_bps > max_rate:
        rate_bps = max_rate
    
    bar_length = 25
    percent = rate_bps / max_rate
    filled = int(bar_length * percent)
    bar = '█' * filled + '░' * (bar_length - filled)
    return bar

def display_realtime_stats(monitor):
    """نمایش آمار لحظه‌ای با Live"""
    if not monitor.history:
        return None
    
    current = monitor.get_current_stats()
    sent_rate = current['sent_rate']
    recv_rate = current['recv_rate']
    
    layout = Layout()
    layout.split(
        Layout(name="header", size=6),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    layout["body"].split_row(
        Layout(name="total"),
        Layout(name="stats")
    )
    
    header_text = Text()
    header_text.append(f"📡 REAL-TIME BANDWIDTH MONITOR\n", style="bold cyan")
    header_text.append(f"Time: {current['timestamp'].strftime('%H:%M:%S')}", style="yellow")
    layout["header"].update(Panel(header_text, border_style="cyan"))
    
    total_content = Text()
    total_content.append(f"\n📊 TOTAL TRAFFIC\n", style="bold green")
    total_content.append(f"\n📤 Upload:   {format_bytes(current['total_sent'])}", style="yellow")
    total_content.append(f"\n📥 Download: {format_bytes(current['total_recv'])}", style="green")
    
    stats_content = Text()
    stats_content.append(f"\n⚡ CURRENT SPEED\n", style="bold cyan")
    stats_content.append(f"\n📤 Upload:   {format_speed(sent_rate)}")
    stats_content.append(f"\n   {create_speed_bar(sent_rate)}")
    stats_content.append(f"\n📥 Download: {format_speed(recv_rate)}")
    stats_content.append(f"\n   {create_speed_bar(recv_rate)}")
    
    avg_sent, avg_recv = monitor.get_average_speed(30)
    peak_sent, peak_recv = monitor.get_peak_speed()
    
    stats_content.append(f"\n\n📈 STATISTICS", style="bold cyan")
    stats_content.append(f"\n📤 Avg Upload (30s):   {format_speed(avg_sent)}")
    stats_content.append(f"\n📥 Avg Download (30s): {format_speed(avg_recv)}")
    stats_content.append(f"\n🔝 Peak Upload:   {format_speed(peak_sent)}")
    stats_content.append(f"\n🔝 Peak Download: {format_speed(peak_recv)}")
    
    layout["total"].update(Panel(total_content, title="📁 Total Data", border_style="green"))
    layout["stats"].update(Panel(stats_content, title="⚡ Speed & Stats", border_style="cyan"))
    
    footer_text = Text()
    footer_text.append(f"Update every {monitor.interval} seconds | Press Ctrl+C to stop", style="dim")
    layout["footer"].update(Panel(footer_text, border_style="grey35"))
    
    return layout

def display_simple_stats(monitor):
    """نمایش آمار ساده"""
    if not monitor.history:
        console.print(f"{YELLOW}No data yet. Run monitoring first.{RESET}")
        return
    
    current = monitor.get_current_stats()
    avg_sent, avg_recv = monitor.get_average_speed(30)
    peak_sent, peak_recv = monitor.get_peak_speed()
    
    sent_rate = current['sent_rate']
    recv_rate = current['recv_rate']
    
    console.print(f"\n{CYAN}{'='*65}{RESET}")
    console.print(f"{GREEN}📡 BANDWIDTH MONITOR - {current['timestamp'].strftime('%H:%M:%S')}{RESET}")
    console.print(f"{CYAN}{'='*65}{RESET}")
    
    console.print(f"\n{YELLOW}📊 TOTAL DATA TRANSFER:{RESET}")
    console.print(f"  📤 Upload:   {format_bytes(current['total_sent'])}")
    console.print(f"  📥 Download: {format_bytes(current['total_recv'])}")
    
    console.print(f"\n{CYAN}⚡ REAL-TIME SPEED:{RESET}")
    console.print(f"  📤 Upload:   {format_speed(sent_rate):>12}  {create_speed_bar(sent_rate)}")
    console.print(f"  📥 Download: {format_speed(recv_rate):>12}  {create_speed_bar(recv_rate)}")
    
    console.print(f"\n{BLUE}📈 AVERAGE (last 30s):{RESET}")
    console.print(f"  📤 Upload:   {format_speed(avg_sent):>12}")
    console.print(f"  📥 Download: {format_speed(avg_recv):>12}")
    
    console.print(f"\n{MAGENTA}🔝 PEAK SPEED:{RESET}")
    console.print(f"  📤 Upload:   {format_speed(peak_sent):>12}")
    console.print(f"  📥 Download: {format_speed(peak_recv):>12}")
    
    console.print(f"\n{CYAN}{'='*65}{RESET}")

def save_bandwidth_report(monitor):
    """ذخیره گزارش پهنای باند"""
    if not monitor.history:
        console.print(f"{RED}No data to save{RESET}")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"bandwidth_report_{timestamp}.txt"
    
    avg_sent, avg_recv = monitor.get_average_speed(60)
    peak_sent, peak_recv = monitor.get_peak_speed()
    current = monitor.get_current_stats()
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("BANDWIDTH MONITORING REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        
        f.write("TOTAL DATA TRANSFER:\n")
        f.write(f"  Upload:   {format_bytes(current['total_sent'])}\n")
        f.write(f"  Download: {format_bytes(current['total_recv'])}\n\n")
        
        f.write("SPEED STATISTICS:\n")
        f.write(f"  Current Upload:   {format_speed(current['sent_rate'])}\n")
        f.write(f"  Current Download: {format_speed(current['recv_rate'])}\n")
        f.write(f"  Avg Upload (60s):   {format_speed(avg_sent)}\n")
        f.write(f"  Avg Download (60s): {format_speed(avg_recv)}\n")
        f.write(f"  Peak Upload:   {format_speed(peak_sent)}\n")
        f.write(f"  Peak Download: {format_speed(peak_recv)}\n\n")
        
        f.write("HISTORY (last 20 samples):\n")
        f.write("-" * 40 + "\n")
        for data in monitor.history[-20:]:
            f.write(f"{data['timestamp'].strftime('%H:%M:%S')} | "
                   f"↑ {format_speed(data['sent_rate']):>12} | "
                   f"↓ {format_speed(data['recv_rate']):>12}\n")
    
    console.print(f"{GREEN}✅ Report saved to {filename}{RESET}")

def bandwidth_monitor_menu():
    """منوی مانیتورینگ پهنای باند"""
    monitor = BandwidthMonitor()
    
    while True:
        clear_screen()
        print_header("BANDWIDTH MONITOR")
        
        console.print("\n[bold cyan]📡 Real-time Bandwidth Monitor (Accurate with psutil)[/bold cyan]")
        console.print("[dim]Monitors actual network traffic on your system[/dim]\n")
        
        if monitor.running:
            console.print(f"{GREEN}✅ STATUS: MONITORING (every {monitor.interval}s){RESET}")
            console.print("\n[1] Stop monitoring")
            console.print("[2] Show current stats")
            console.print("[3] Show real-time Live view")
            console.print("[4] Save report")
            console.print("[5] Change interval")
        else:
            console.print(f"{RED}❌ STATUS: STOPPED{RESET}")
            console.print("\n[1] Start monitoring")
            console.print("[2] Show network interfaces")
            console.print("[3] Show active connections")
        
        console.print("[b] Back to main menu")
        
        choice = input(f"\n{YELLOW}👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            if monitor.running:
                monitor.stop_monitoring()
            break
        
        elif choice == '1' and not monitor.running:
            monitor.start_monitoring()
            console.print(f"{GREEN}Monitoring started!{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '2' and not monitor.running:
            interfaces = monitor.get_interface_details()
            if interfaces:
                console.print(f"\n{CYAN}Network Interfaces:{RESET}")
                for iface in interfaces:
                    console.print(f"\n  {GREEN}{iface['name']}{RESET}")
                    console.print(f"    Speed: {iface['speed']} Mbps")
                    console.print(f"    MTU: {iface['mtu']}")
                    for addr in iface['addresses']:
                        if 'AF_INET' in str(addr['family']) or '2' in str(addr['family']):
                            console.print(f"    IPv4: {addr['address']}")
            else:
                console.print(f"{YELLOW}No active interfaces found{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '3' and not monitor.running:
            processes = monitor.get_process_bandwidth()
            if processes:
                table = Table(title="Active Network Connections")
                table.add_column("PID", style="cyan")
                table.add_column("Process", style="green")
                table.add_column("Local Address", style="yellow")
                table.add_column("Remote Address", style="blue")
                table.add_column("Status", style="white")
                
                for proc in processes[:30]:
                    table.add_row(
                        str(proc['pid']),
                        proc['name'][:20],
                        proc['laddr'][:25],
                        proc['raddr'][:25],
                        proc['status']
                    )
                console.print(table)
            else:
                console.print(f"{YELLOW}No active connections found{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '1' and monitor.running:
            monitor.stop_monitoring()
            input(f"\nPress Enter...")
        
        elif choice == '2' and monitor.running:
            display_simple_stats(monitor)
            input(f"\nPress Enter...")
        
        elif choice == '3' and monitor.running:
            console.print(f"\n{CYAN}Press Ctrl+C to stop Live view{RESET}")
            console.print("[dim]Live updating every 2 seconds...[/dim]\n")
            
            try:
                with Live(auto_refresh=False, screen=False) as live:
                    while monitor.running:
                        layout = display_realtime_stats(monitor)
                        if layout:
                            live.update(layout, refresh=True)
                        time.sleep(monitor.interval)
            except KeyboardInterrupt:
                console.print(f"\n{YELLOW}Live view stopped{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '4' and monitor.running:
            save_bandwidth_report(monitor)
            input(f"\nPress Enter...")
        
        elif choice == '5' and monitor.running:
            try:
                new_interval = int(input(f"{YELLOW}New interval (seconds, min 1): {RESET}"))
                if new_interval >= 1:
                    monitor.interval = new_interval
                    console.print(f"{GREEN}Interval changed to {new_interval} seconds{RESET}")
                else:
                    console.print(f"{RED}Interval must be at least 1 second{RESET}")
            except:
                console.print(f"{RED}Invalid input{RESET}")
            input(f"\nPress Enter...")
        
        else:
            console.print(f"{RED}Invalid choice{RESET}")
            input(f"\nPress Enter...")