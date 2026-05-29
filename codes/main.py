
import time
import threading
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from config import *
from scanner import *
from threat_detector import *
from utils import *

from wireless_scanner import wifi_scan_menu
from traceroute import traceroute_menu
from internet_monitor import internet_monitor_menu
from help import show_help_menu
from vulnerability_scanner import vulnerability_scan_menu
from network_map import network_map_menu
from bandwidth_monitor import bandwidth_monitor_menu
from database_manager import database_menu, db
from action_mode import show_action_menu
from pdf_report import pdf_report_menu
from splash_screen import  show_simple_splash

console = Console()

auto_scan_running = False
auto_scan_thread = None
last_scan_results = []

def single_ip_menu():
    while True:
        clear_screen()
        print_header("Single IP Scan")
        
        ip = input("\n[?] Target IP (or 'b' to go back): ").strip()
        
        if ip.lower() == 'b':
            break
        
        if not ip:
            console.print("[red][!] IP cannot be empty[/red]")
            input("\n[yellow]Press Enter...[/yellow]")
            continue
        
        result = scan_single_device(ip)
        
        if result:
            clear_screen()
            print_header(f"Scan Result: {ip}")
            
            table = Table(title="Device Information")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("IP", result['ip'])
            table.add_row("OS", f"{result['icon']} {result['os']}")
            table.add_row("TTL", str(result['ttl']))
            table.add_row("Open Ports", ', '.join(map(str, result['ports'])) if result['ports'] else "None")
            console.print(table)
            
            analysis = ThreatDetector.analyze_device(result['ip'], result['os'], result['ports'])
            if analysis['risk_level'] != "safe":
                display_alert(analysis)
            else:
                console.print(f"\n[green][✓] No threats detected[/green]")
            
            save_choice = input("\n[?] Save to CSV? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_to_csv(result, "scan", "single")
            
            input("\n[yellow]Press Enter to continue...[/yellow]")
        else:
            input("\n[yellow]Press Enter to continue...[/yellow]")

def quick_scan_menu():
    speed = 'fast'
    
    while True:
        clear_screen()
        print_header("Quick Network Scan")
        
        console.print(f"\n[cyan]Network:[/cyan] {DEFAULT_NETWORK}.1 to {DEFAULT_NETWORK}.254")
        console.print(f"[cyan]Speed:[/cyan] {speed}")
        
        console.print("\n[1] Start scan")
        console.print("[2] Change speed")
        console.print("[b] Back to main menu")
        
        choice = input("\n[?] Your choice: ").strip().lower()
        
        if choice == 'b':
            break
        elif choice == '2':
            console.print("\nSpeed options:")
            console.print("  1. Fast (0.2s timeout)")
            console.print("  2. Normal (0.5s timeout)")
            console.print("  3. Slow (1.0s timeout)")
            speed_choice = input("Choose (1-3): ").strip()
            speeds = {'1': 'fast', '2': 'normal', '3': 'slow'}
            speed = speeds.get(speed_choice, 'fast')
            console.print(f"[green]Speed set to {speed}[/green]")
            input("\nPress Enter...")
        elif choice == '1':
            clear_screen()
            print_header("Scanning Network...")
            
            devices = quick_scan_network(DEFAULT_NETWORK, speed, None)
            
            clear_screen()
            print_header("Scan Results")
            
            console.print(f"\n[green][✓] Found {len(devices)} device(s)[/green]\n")
            
            for device in devices:
                console.print(f"  {device['icon']} {device['ip']} -> {device['os']}")
            
            if devices:
                save_choice = input("\n[?] Save to CSV? (y/n): ").strip().lower()
                if save_choice == 'y':
                    save_to_csv(devices, "scan", "network")
            
            input("\n[yellow]Press Enter to continue...[/yellow]")
        else:
            console.print("[red]Invalid choice[/red]")
            input("\nPress Enter...")

def auto_scan_worker(interval_minutes=5):
    global auto_scan_running, last_scan_results
    
    console.print(f"[cyan]Auto-scan started every {interval_minutes} minute(s)[/cyan]")
    
    while auto_scan_running:
        console.print(f"\n[yellow][{datetime.now().strftime('%H:%M:%S')}] Running auto-scan...[/yellow]")
        
        try:
            devices = quick_scan_network(DEFAULT_NETWORK, 'fast', None)
            new_devices = [d for d in devices if is_unknown_device(d['ip'])]
            
            if new_devices:
                console.print(f"[red][!] Found {len(new_devices)} new device(s)![/red]")
                for device in new_devices:
                    console.print(f"  {device['icon']} {device['ip']} -> {device['os']}")
                    
                    today = datetime.now().strftime('%Y%m%d')
                    alert_file = f"auto_scan_alerts_{today}.json"
                    alerts = load_json_file(alert_file, [])
                    alerts.append({
                        "type": "new_device",
                        "ip": device['ip'],
                        "os": device['os'],
                        "timestamp": datetime.now().isoformat()
                    })
                    save_json_file(alert_file, alerts)
            
            last_scan_results = devices
            
        except Exception as e:
            console.print(f"[red]Error in auto-scan: {e}[/red]")
        
        for _ in range(interval_minutes * 60):
            if not auto_scan_running:
                break
            time.sleep(1)
    
    console.print("[yellow]Auto-scan stopped[/yellow]")

def auto_scan_menu():
    global auto_scan_running, auto_scan_thread
    
    while True:
        clear_screen()
        print_header("Auto Scan (Scheduled)")
        
        if auto_scan_running:
            console.print(f"\n[green]Status: RUNNING[/green]")
            console.print("[1] Stop auto-scan")
            console.print("[2] View last results")
        else:
            console.print(f"\n[red]Status: STOPPED[/red]")
            console.print("[1] Start auto-scan (every 5 min)")
            console.print("[2] Start auto-scan (every 15 min)")
            console.print("[3] Start auto-scan (every 30 min)")
        
        console.print("[b] Back to main menu")
        
        choice = input("\n[?] Choose: ").strip().lower()
        
        if choice == 'b':
            break
        
        elif not auto_scan_running and choice in ['1', '2', '3']:
            intervals = {'1': 5, '2': 15, '3': 30}
            auto_scan_running = True
            auto_scan_thread = threading.Thread(target=auto_scan_worker, args=(intervals[choice],), daemon=True)
            auto_scan_thread.start()
            console.print(f"[green]Auto-scan started! (every {intervals[choice]} min)[/green]")
            input("\nPress Enter...")
        
        elif auto_scan_running and choice == '1':
            auto_scan_running = False
            if auto_scan_thread:
                auto_scan_thread.join(timeout=2)
            console.print("[yellow]Auto-scan stopped[/yellow]")
            input("\nPress Enter...")
        
        elif auto_scan_running and choice == '2':
            if last_scan_results:
                console.print(f"\n[cyan]Last scan results ({len(last_scan_results)} devices):[/cyan]")
                for device in last_scan_results[:20]:
                    console.print(f"  {device['icon']} {device['ip']} -> {device['os']}")
                if len(last_scan_results) > 20:
                    console.print(f"  ... and {len(last_scan_results) - 20} more")
            else:
                console.print("[yellow]No scan results yet[/yellow]")
            input("\nPress Enter...")
        
        else:
            console.print("[red]Invalid choice[/red]")
            input("\nPress Enter...")

def threat_history_menu():
    clear_screen()
    print_header("Threat Alert History")
    
    alerts = load_json_file(ALERT_LOG_FILE, [])
    
    if not alerts:
        console.print("[yellow][!] No threat alerts found[/yellow]")
        input("\n[yellow]Press Enter...[/yellow]")
        return
    
    critical = [a for a in alerts if a.get('risk_level') == 'critical']
    warning = [a for a in alerts if a.get('risk_level') == 'warning']
    
    console.print(f"\n[red]Critical threats: {len(critical)}[/red]")
    console.print(f"[yellow]Warnings: {len(warning)}[/yellow]")
    console.print(f"[green]Total alerts: {len(alerts)}[/green]")
    
    console.print(f"\n[cyan]Last 10 alerts:[/cyan]")
    for alert in alerts[-10:]:
        time_str = alert.get('timestamp', '')[:19]
        risk_icon = "🔴" if alert.get('risk_level') == 'critical' else "🟡"
        console.print(f"  {risk_icon} [{time_str}] {alert.get('ip', '?')} - {alert.get('risk_level', 'unknown').upper()}")
    
    input("\n[yellow]Press Enter...[/yellow]")

def known_devices_menu():
    while True:
        clear_screen()
        print_header("Known Devices")
        
        known = load_json_file(KNOWN_DEVICES_FILE, [])
        
        console.print(f"\n[cyan]Known devices ({len(known)}):[/cyan]")
        for ip in known:
            console.print(f"  - {ip}")
        
        console.print("\n[1] Add IP")
        console.print("[2] Clear all")
        console.print("[b] Back to main menu")
        
        choice = input("\n[?] Choose: ").strip().lower()
        
        if choice == 'b':
            break
        elif choice == '1':
            ip = input("Enter IP: ").strip()
            if add_known_device(ip):
                console.print(f"[green]Added {ip}[/green]")
            else:
                console.print(f"[yellow]{ip} already in list[/yellow]")
            input("\nPress Enter...")
        elif choice == '2':
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm == 'yes':
                save_json_file(KNOWN_DEVICES_FILE, [])
                console.print("[green]Cleared[/green]")
                input("\nPress Enter...")
        else:
            console.print("[red]Invalid choice[/red]")
            input("\nPress Enter...")

def main():
    global auto_scan_running
    show_simple_splash()
    while True:
        clear_screen()
        #show_banner()
        #time.sleep(4)
        #clear_screen()
        
        console.print(Panel.fit(
            "[green]OS Fingerprinter & Threat Detector v1.0[/green]\n[cyan]Network Security Tool + Wi-Fi + Traceroute[/cyan]",
            border_style="cyan"
        ))
        
        console.print(f"\n[cyan]╔{'═' * 50}╗[/cyan]")
        console.print(f"[green]║{'MAIN MENU'.center(50)}║[/green]")
        '''Created by: Payam Fekri'''
        console.print(f"[cyan]╚{'═' * 50}╝[/cyan]")
        
        console.print("\n[1] Scan single IP")
        console.print("[2] Quick scan network")
        console.print("[3] Auto scan (scheduled)")
        console.print("[4] Threat history")
        console.print("[5] Known devices")
        console.print("[6] Wi-Fi Scanner")
        console.print("[7] Traceroute")
        console.print("[8] Internet Monitor")
        console.print("[9] Vulnerability Scanner")  
        console.print("[10] Network Map")
        console.print("[11] Bandwidth Monitor")
        console.print("[12] Database Manager")
        console.print("[13] Action Mode (AUTO)")
        console.print("[14] PDF Report Generator")# جدید
        console.print("[20] Help")
        console.print("[0] Exit\n")
        
        console.print("[dim]Created by: github.com/PayamFekri[/dim]")
        
        choice = input(f"\n[?] Choose (1-9) [Network: {DEFAULT_NETWORK}.x]: ").strip()
        
        
        
        if choice == "1":
            single_ip_menu()
        elif choice == '14':
            pdf_report_menu()
        elif choice == '12':
            database_menu()
        elif choice == '13':
            show_action_menu()
        elif choice == '11':
            bandwidth_monitor_menu()
        elif choice == "2":
            quick_scan_menu()
        elif choice == "3":
            auto_scan_menu()
        elif choice == "4":
            threat_history_menu()
        elif choice == "5":
            known_devices_menu()
        elif choice == "6":
            wifi_scan_menu()
        elif choice == "7":
            traceroute_menu()
        elif choice == "8":
            internet_monitor_menu()
        elif choice == "9":
            vulnerability_scan_menu()
        elif choice == "20":
            show_help_menu()
        elif choice == '10':
            network_map_menu()
        elif choice == "0" or choice == "exit":
            if auto_scan_running:
                auto_scan_running = False
                console.print("Stopping auto-scan...")
                time.sleep(1)
            clear_screen()
            console.print("\n Goodbye! Stay secure! 🔒")
            break
        else:
            console.print("[red][!] Invalid choice[/red]")
            input("\n[yellow]Press Enter...[/yellow]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        console.print("\n[red]Interrupted. Goodbye![/red]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")