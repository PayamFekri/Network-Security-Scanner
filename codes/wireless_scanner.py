import subprocess
import re
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
last_wifi_scan = []

def scan_wifi_networks():
    """اسکن شبکه‌های بی‌سیم اطراف با netsh"""
    try:
        # اول ببین وای‌فای فعال هست یا نه
        interface_result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "There is 1 interface" not in interface_result.stdout and "Wi-Fi" not in interface_result.stdout:
            return "NO_WIFI_ADAPTER"
        
        # حالا شبکه‌ها رو اسکن کن
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if "There are 0 networks currently visible" in result.stdout:
            return "NO_NETWORKS"
            
        return result.stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def parse_wifi_output_simple(output):
    """پارس ساده خروجی netsh - خط به خط"""
    networks = []
    current = {}
    
    lines = output.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # پیدا کردن SSID
        if line.startswith('SSID'):
            # ذخیره شبکه قبلی
            if current and 'ssid' in current:
                networks.append(current)
                current = {}
            
            # استخراج نام SSID
            parts = line.split(':')
            if len(parts) >= 2:
                ssid = parts[1].strip()
                if ssid and ssid != '':
                    current['ssid'] = ssid
                    current['signal'] = 0
        
        # قدرت سیگنال
        elif 'Signal' in line and ':' in line:
            try:
                signal_str = line.split(':')[1].strip()
                signal_num = re.findall(r'\d+', signal_str)
                if signal_num:
                    current['signal'] = int(signal_num[0])
            except:
                pass
        
        # نوع احراز هویت
        elif 'Authentication' in line and ':' in line:
            auth = line.split(':')[1].strip()
            current['auth'] = auth
        
        # رمزگذاری
        elif 'Encryption' in line and ':' in line:
            enc = line.split(':')[1].strip()
            current['encryption'] = enc
        
        # باند فرکانسی
        elif 'Band' in line and ':' in line:
            band = line.split(':')[1].strip()
            current['band'] = band
        
        # کانال
        elif 'Channel' in line and ':' in line:
            try:
                ch = line.split(':')[1].strip()
                current['channel'] = int(ch)
            except:
                pass
        
        # BSSID
        elif 'BSSID' in line and ':' in line:
            bssid = line.split(':')[1].strip()
            current['bssid'] = bssid
    
    # اضافه کردن آخرین شبکه
    if current and 'ssid' in current:
        networks.append(current)
    
    return networks

def get_security_icon(auth):
    """آیکون امنیتی بر اساس نوع احراز هویت"""
    if not auth or auth == 'Open' or auth == '':
        return "🔓"
    elif 'WPA3' in str(auth):
        return "🛡️"
    elif 'WPA2' in str(auth):
        return "🔐"
    elif 'WPA' in str(auth):
        return "⚠️"
    elif 'WEP' in str(auth):
        return "❌"
    else:
        return "🔒"

def get_security_level(auth):
    """سطح امنیتی (برای تحلیل)"""
    if not auth or auth == 'Open':
        return ("CRITICAL", "red", "No password required - anyone can connect!")
    elif 'WEP' in str(auth):
        return ("WEAK", "red", "WEP encryption - can be cracked in minutes!")
    elif 'WPA1' in str(auth):
        return ("WEAK", "yellow", "WPA1 is outdated and vulnerable")
    elif 'WPA2' in str(auth):
        return ("GOOD", "green", "WPA2 is secure (with strong password)")
    elif 'WPA3' in str(auth):
        return ("EXCELLENT", "bright_green", "WPA3 - latest security standard")
    else:
        return ("UNKNOWN", "blue", "Unknown security type")

def get_signal_icon(signal):
    """آیکون قدرت سیگنال"""
    if signal >= 80:
        return "█████"
    elif signal >= 60:
        return "████▒"
    elif signal >= 40:
        return "███▒▒"
    elif signal >= 20:
        return "██▒▒▒"
    else:
        return "█▒▒▒▒"

def analyze_wifi_security(networks):
    """تحلیل کامل امنیتی شبکه‌های وای‌فای"""
    console.print(Panel.fit("[bold cyan]🔍 Wi-Fi Security Analysis[/bold cyan]", border_style="cyan"))
    
    # آمار کلی
    total = len(networks)
    console.print(f"\n[cyan]📊 Total networks found: {total}[/cyan]")
    
    # 1. شبکه‌های با امنیت ضعیف
    weak_nets = []
    critical_nets = []
    
    for net in networks:
        auth = net.get('auth', '')
        if auth == 'Open':
            critical_nets.append(net)
        elif 'WEP' in auth or 'WPA1' in auth:
            weak_nets.append(net)
    
    if critical_nets:
        console.print(f"\n[red]🔴 CRITICAL SECURITY ISSUES: {len(critical_nets)} network(s) with NO PASSWORD![/red]")
        for net in critical_nets:
            console.print(f"   🔓 {net.get('ssid')} - Anyone can connect!")
    
    if weak_nets:
        console.print(f"\n[yellow]⚠️ WEAK SECURITY: {len(weak_nets)} network(s)[/yellow]")
        for net in weak_nets:
            console.print(f"   ❌ {net.get('ssid')} - {net.get('auth')}")
    
    if not critical_nets and not weak_nets:
        console.print(f"\n[green]✅ All networks use WPA2/WPA3 encryption (good!)[/green]")
    
    # 2. تحلیل کانال‌ها (بهترین کانال برای وای‌فای خودت)
    channel_usage = {}
    for net in networks:
        ch = net.get('channel')
        if ch:
            channel_usage[ch] = channel_usage.get(ch, 0) + 1
    
    if channel_usage:
        console.print(f"\n[cyan]📡 Channel Analysis (for 2.4GHz):[/cyan]")
        
        # کانال‌های 2.4GHz (1, 6, 11 بهترین‌ها هستند)
        channels_24 = [(ch, count) for ch, count in channel_usage.items() if ch <= 11]
        if channels_24:
            channels_24.sort(key=lambda x: x[1])
            
            console.print("   Channel interference (fewer = better):")
            for ch, count in channels_24[:5]:
                bar = "█" * min(count, 10)
                console.print(f"   Channel {ch:2}: {bar} ({count} networks)")
            
            # پیشنهاد بهترین کانال
            best_channels = [1, 6, 11]  # کانال‌های غیر همپوشان
            best_channel = min(best_channels, key=lambda x: channel_usage.get(x, 0))
            console.print(f"\n   [bold green]🎯 Best channel for YOUR Wi-Fi: {best_channel}[/bold green]")
            console.print(f"      (Only {channel_usage.get(best_channel, 0)} network(s) using this channel)")
    
    # 3. شبکه‌های با قدرت سیگنال خوب
    strong_nets = [n for n in networks if n.get('signal', 0) >= 60]
    if strong_nets:
        console.print(f"\n[green]📶 Strong signal networks ({len(strong_nets)}):[/green]")
        for net in strong_nets[:5]:
            console.print(f"   {net.get('ssid')} - {net.get('signal')}%")
    
    # 4. شبکه‌های با نام مشابه (احتمال جعلی)
    ssid_names = {}
    for net in networks:
        ssid = net.get('ssid', '')
        if ssid:
            ssid_names[ssid] = ssid_names.get(ssid, 0) + 1
    
    duplicates = {name: count for name, count in ssid_names.items() if count > 1}
    if duplicates:
        console.print(f"\n[yellow]⚠️ Duplicate SSID names detected (possible Evil Twin attack):[/yellow]")
        for name, count in duplicates.items():
            console.print(f"   {name} appears {count} times")

def display_wifi_networks(networks):
    """نمایش شبکه‌های وای‌فای"""
    if not networks:
        console.print("[yellow]No Wi-Fi networks found![/yellow]")
        return
    
    # جدول اصلی شبکه‌ها
    table = Table(title=f"📡 Nearby Wi-Fi Networks ({len(networks)})")
    table.add_column("Sec", style="cyan", width=5)
    table.add_column("SSID", style="green", width=28)
    table.add_column("Signal", style="yellow", width=14)
    table.add_column("Channel", style="blue", width=8)
    table.add_column("Band", style="magenta", width=10)
    table.add_column("Security", style="dim", width=14)
    
    # مرتب‌سازی بر اساس قدرت سیگنال
    networks_sorted = sorted(networks, key=lambda x: x.get('signal', 0), reverse=True)
    
    for net in networks_sorted:
        ssid = net.get('ssid', '?')
        if not ssid or ssid == '':
            ssid = '🔒 Hidden'
        
        sec_icon = get_security_icon(net.get('auth'))
        signal_icon = get_signal_icon(net.get('signal', 0))
        signal = net.get('signal', 0)
        auth = net.get('auth', 'Unknown')
        
        # کوتاه کردن امنیت
        if 'WPA2' in auth:
            auth_short = "WPA2 🔐"
        elif 'WPA3' in auth:
            auth_short = "WPA3 🛡️"
        elif 'WEP' in auth:
            auth_short = "WEP ❌"
        elif 'Open' in auth:
            auth_short = "OPEN 🔓"
        else:
            auth_short = auth[:12]
        
        table.add_row(
            sec_icon,
            ssid[:28],
            f"{signal_icon} {signal}%",
            str(net.get('channel', '?')),
            net.get('band', '?')[:8],
            auth_short
        )
    
    console.print(table)
    
    # تحلیل امنیتی کامل
    analyze_wifi_security(networks)
    
    # نکات امنیتی
    console.print(Panel.fit(
        "[bold yellow]💡 Security Tips:[/bold yellow]\n"
        "• Change your router's default password\n"
        "• Use WPA2 or WPA3 encryption\n"
        "• Choose channel with least interference\n"
        "• Hide your SSID for extra privacy",
        border_style="yellow"
    ))

def save_wifi_results(networks):
    """ذخیره نتایج در CSV"""
    if not networks:
        console.print("[red]No data to save[/red]")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"wifi_scan_{timestamp}.csv"
    
    import csv
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['SSID', 'BSSID', 'Signal', 'Channel', 'Band', 'Authentication', 'Encryption', 'Scan Time'])
        for net in networks:
            writer.writerow([
                net.get('ssid', ''),
                net.get('bssid', ''),
                net.get('signal', 0),
                net.get('channel', ''),
                net.get('band', ''),
                net.get('auth', ''),
                net.get('encryption', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
    
    console.print(f"[green]✓ Saved to {filename}[/green]")

def wifi_scan_menu():
    """منوی اسکن وای‌فای"""
    global last_wifi_scan
    
    while True:
        console.print("\n[cyan]📡 Wi-Fi Security Scanner[/cyan]")
        console.print("[1] Scan nearby networks")
        console.print("[2] Save last scan to CSV")
        console.print("[b] Back to main menu")
        
        choice = input("\n[?] Choose: ").strip().lower()
        
        if choice == 'b':
            break
        
        elif choice == '1':
            console.print("\n[yellow]Scanning Wi-Fi networks...[/yellow]")
            
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                progress.add_task(description="Scanning...", total=None)
                output = scan_wifi_networks()
            
            if output == "NO_WIFI_ADAPTER":
                console.print("[red]No Wi-Fi adapter found or Wi-Fi is disabled![/red]")
                console.print("[yellow]Please turn on Wi-Fi and try again[/yellow]")
                continue
            
            elif output == "NO_NETWORKS":
                console.print("[yellow]No Wi-Fi networks found nearby[/yellow]")
                continue
            
            elif output == "TIMEOUT":
                console.print("[red]Scan timed out. Try again[/red]")
                continue
            
            elif output.startswith("ERROR"):
                console.print(f"[red]{output}[/red]")
                continue
            
            networks = parse_wifi_output_simple(output)
            last_wifi_scan = networks
            
            if networks:
                display_wifi_networks(networks)
            else:
                console.print("[yellow]No Wi-Fi networks found![/yellow]")
        
        elif choice == '2':
            if last_wifi_scan:
                save_wifi_results(last_wifi_scan)
            else:
                console.print("[red]No scan yet. Run scan first![/red]")
        
        else:
            console.print("[red]Invalid choice! Enter 1, 2, or b[/red]")