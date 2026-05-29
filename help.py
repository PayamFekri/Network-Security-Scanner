# help.py - راهنمای کامل برنامه (بروز شده)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from utils import clear_screen, print_header
from config import GREEN, RED, YELLOW, CYAN, BLUE, RESET

console = Console()

def show_main_help():
    """نمایش راهنمای اصلی برنامه"""
    clear_screen()
    print_header("PROGRAM HELP")
    
    console.print(Panel.fit(
        "[bold cyan]🔧 Network Security Scanner v5.0[/bold cyan]\n"
        "[green]Complete Network Security & Penetration Testing Tool[/green]\n"
        "[yellow]Created by: Payam Fekri[/yellow]",
        border_style="cyan"
    ))
    
    console.print("\n[bold yellow]📋 Main Menu Options:[/bold yellow]\n")
    
    menu_table = Table(show_header=True, header_style="bold cyan")
    menu_table.add_column("Option", style="green", width=8)
    menu_table.add_column("Name", style="yellow", width=22)
    menu_table.add_column("Description", style="white", width=50)
    
    menu_items = [
        ("1", "Scan single IP", "Full device scan including ports and threat detection"),
        ("2", "Quick scan network", "Find all live devices on your network quickly"),
        ("3", "Auto scan", "Periodic scheduled network scanning"),
        ("4", "Threat history", "View all previous security alerts"),
        ("5", "Known devices", "Manage trusted devices on your network"),
        ("6", "Wi-Fi Scanner", "Discover nearby wireless networks + channel analysis"),
        ("7", "Traceroute", "View route path to any IP or domain"),
        ("8", "Internet Monitor", "Track and log internet outages real-time"),
        ("9", "Vulnerability Scanner", "Advanced vulnerability detection (EternalBlue, etc)"),
        ("10", "Network Map", "Graphical/text map of your entire network"),
        ("11", "Bandwidth Monitor", "Real-time bandwidth usage monitoring"),
        ("12", "Database Manager", "SQLite database for all scan results"),
        ("13", "Action Mode (AUTO)", "Fully automated security monitoring"),
        ("14", "PDF Report", "Generate professional PDF security reports"),
        ("20", "Help", "Show this help menu"),
        ("0", "Exit", "Exit the program")
    ]
    
    for item in menu_items:
        menu_table.add_row(*item)
    
    console.print(menu_table)

def show_scan_help():
    """راهنمای اسکن شبکه"""
    clear_screen()
    print_header("NETWORK SCAN HELP")
    
    console.print(Panel(
        "[bold yellow]🎯 Single IP Scan (Option 1)[/bold yellow]\n\n"
        "Complete scan of a specific device:\n"
        "• [green]Open Ports[/green] - List of open ports\n"
        "• [green]OS Detection[/green] - Identify operating system via TTL\n"
        "• [green]Threat Analysis[/green] - Detect dangerous ports\n\n"
        "[bold]Example:[/bold] 192.168.1.1 (your router)\n\n"
        "[bold yellow]⚡ Quick Network Scan (Option 2)[/bold yellow]\n\n"
        "Scans entire network and finds all live devices:\n"
        "• [green]Scan Speed[/green] - Fast/Normal/Slow\n"
        "• [green]Device Detection[/green] - IP, OS type, signal strength\n\n"
        "[bold]Note:[/bold] Use 'Normal' speed for large networks.",
        border_style="cyan"
    ))

def show_wifi_help():
    """راهنمای اسکن وای‌فای"""
    clear_screen()
    print_header("WI-FI SCANNER HELP")
    
    console.print(Panel(
        "[bold yellow]📡 Wi-Fi Scanner (Option 6)[/bold yellow]\n\n"
        "Discover wireless networks around you:\n\n"
        "[bold]Displayed Information:[/bold]\n"
        "• [green]SSID[/green] - Network name\n"
        "• [green]Signal Strength[/green] - Percentage and graphical bar\n"
        "• [green]Security Type[/green] - WPA2/WPA3/Open/Weak\n"
        "• [green]Channel[/green] - Frequency channel\n"
        "• [green]Band[/green] - 2.4GHz or 5GHz\n\n"
        "[bold]Security Analysis:[/bold]\n"
        "• Detect open networks (no password)\n"
        "• Detect weak security (WEP/WPA1)\n"
        "• Recommend best channel for YOUR Wi-Fi\n"
        "• Channel interference analysis\n\n"
        "[bold]Tip:[/bold] Never connect to open networks!",
        border_style="cyan"
    ))

def show_traceroute_help():
    """راهنمای ردیابی مسیر"""
    clear_screen()
    print_header("TRACEROUTE HELP")
    
    console.print(Panel(
        "[bold yellow]🛤️ Traceroute (Option 7)[/bold yellow]\n\n"
        "Shows the route path to a destination:\n\n"
        "[bold]Use Cases:[/bold]\n"
        "• Network latency diagnosis\n"
        "• Connection troubleshooting\n"
        "• Internet route visualization\n\n"
        "[bold]Options:[/bold]\n"
        "• [green]Trace local router[/green] - To your modem (no internet needed)\n"
        "• [green]Trace localhost[/green] - To your own computer\n"
        "• [green]Trace IP/Domain[/green] - External target (requires internet)\n\n"
        "[bold]Note:[/bold] Without internet, only local options work.",
        border_style="cyan"
    ))

def show_internet_monitor_help():
    """راهنمای مانیتور اینترنت"""
    clear_screen()
    print_header("INTERNET MONITOR HELP")
    
    console.print(Panel(
        "[bold yellow]🌐 Internet Monitor (Option 8)[/bold yellow]\n\n"
        "Logs and reports internet outages:\n\n"
        "[bold]Features:[/bold]\n"
        "• [green]Automatic Monitoring[/green] - Regular interval checks\n"
        "• [green]Outage Logging[/green] - Records start/end times\n"
        "• [green]Detailed Statistics[/green] - Outage count, total downtime\n"
        "• [green]Export Reports[/green] - Save to JSON and TXT\n\n"
        "[bold]Settings:[/bold]\n"
        "• Check interval: 10, 30, or 60 seconds\n"
        "• Real-time online/offline display\n"
        "• Automatic daily report saving\n\n"
        "[bold]Use Case:[/bold] Perfect for unstable internet connections.",
        border_style="cyan"
    ))

def show_vulnerability_help():
    """راهنمای اسکن آسیب‌پذیری"""
    clear_screen()
    print_header("VULNERABILITY SCANNER HELP")
    
    console.print(Panel(
        "[bold yellow]🚨 Vulnerability Scanner (Option 9)[/bold yellow]\n\n"
        "Advanced vulnerability detection:\n\n"
        "[bold]Critical Ports Checked:[/bold]\n"
        "• [red]Port 21 (FTP)[/red] - Anonymous access risk\n"
        "• [red]Port 23 (Telnet)[/red] - Unencrypted communication\n"
        "• [red]Port 445 (SMB)[/red] - EternalBlue vulnerability\n"
        "• [red]Port 3389 (RDP)[/red] - Brute force target\n\n"
        "[bold]What it detects:[/bold]\n"
        "• Default credentials on services\n"
        "• Weak SSL/TLS versions\n"
        "• Information disclosure\n"
        "• Known vulnerabilities (EternalBlue, etc)\n\n"
        "[bold]Note:[/bold] Some checks are basic - use with Kali Linux for advanced testing.",
        border_style="cyan"
    ))

def show_network_map_help():
    """راهنمای نقشه شبکه"""
    clear_screen()
    print_header("NETWORK MAP HELP")
    
    console.print(Panel(
        "[bold yellow]🗺️ Network Map (Option 10)[/bold yellow]\n\n"
        "Visual representation of your entire network:\n\n"
        "[bold]Features:[/bold]\n"
        "• [green]Device Discovery[/green] - Find all devices on your network\n"
        "• [green]Topology View[/green] - Tree structure showing connections\n"
        "• [green]ASCII Map[/green] - Simple text-based network map\n"
        "• [green]Save/Load[/green] - Persist network maps to JSON\n"
        "• [green]Compare[/green] - Detect new/removed devices\n\n"
        "[bold]Use Case:[/bold]\n"
        "• See who is connected to your network\n"
        "• Detect unauthorized devices\n"
        "• Understand network layout",
        border_style="cyan"
    ))

def show_bandwidth_help():
    """راهنمای مانیتور پهنای باند"""
    clear_screen()
    print_header("BANDWIDTH MONITOR HELP")
    
    console.print(Panel(
        "[bold yellow]📊 Bandwidth Monitor (Option 11)[/bold yellow]\n\n"
        "Real-time network traffic monitoring:\n\n"
        "[bold]Features:[/bold]\n"
        "• [green]Real-time Speed[/green] - Upload/download speeds\n"
        "• [green]Total Traffic[/green] - Cumulative data transfer\n"
        "• [green]Per Device[/green] - Traffic per IP address\n"
        "• [green]Live View[/green] - Animated graphical display\n"
        "• [green]Peak Speed[/green] - Maximum recorded speed\n\n"
        "[bold]Requirements:[/bold]\n"
        "• [yellow]pip install psutil[/yellow] for accurate monitoring\n\n"
        "[bold]Note:[/bold] Per-device traffic is estimated.",
        border_style="cyan"
    ))

def show_database_help():
    """راهنمای دیتابیس"""
    clear_screen()
    print_header("DATABASE MANAGER HELP")
    
    console.print(Panel(
        "[bold yellow]🗄️ Database Manager (Option 12)[/bold yellow]\n\n"
        "SQLite database for all scan results:\n\n"
        "[bold]Features:[/bold]\n"
        "• [green]Auto-save[/green] - All scans saved automatically\n"
        "• [green]History[/green] - View past scan results\n"
        "• [green]Devices[/green] - Track device first/last seen\n"
        "• [green]Export[/green] - Export database to JSON\n"
        "• [green]Statistics[/green] - Overall database metrics\n\n"
        "[bold]Tables:[/bold]\n"
        "• network_scans - All network scans\n"
        "• devices - Device history\n"
        "• vulnerabilities - Detected vulnerabilities\n"
        "• wifi_scans - Wi-Fi network scans\n"
        "• internet_outages - Outage logs",
        border_style="cyan"
    ))

def show_action_mode_help():
    """راهنمای حالت اکشن"""
    clear_screen()
    print_header("ACTION MODE HELP")
    
    console.print(Panel(
        "[bold yellow]🤖 Action Mode (Option 13)[/bold yellow]\n\n"
        "Fully automated security monitoring:\n\n"
        "[bold]What it does:[/bold]\n"
        "• [green]Auto Network Scan[/green] - Every X minutes\n"
        "• [green]Auto Threat Detection[/green] - Real-time alerts\n"
        "• [green]Auto Save to DB[/green] - All results stored\n"
        "• [green]Auto Close Ports[/green] - Block dangerous ports\n"
        "• [green]Daily Reports[/green] - Automatic PDF generation\n\n"
        "[bold]Settings:[/bold]\n"
        "• Scan interval: 15-1440 minutes\n"
        "• Auto-close ports: Enable/disable\n"
        "• Alert sound: On/Off\n"
        "• Report hour: Daily report time\n\n"
        "[bold]Status:[/bold]\n"
        "• Shows running status\n"
        "• View scan history\n"
        "• Statistics (total scans, auto-fixes)",
        border_style="cyan"
    ))

def show_pdf_help():
    """راهنمای گزارش PDF"""
    clear_screen()
    print_header("PDF REPORT HELP")
    
    console.print(Panel(
        "[bold yellow]📄 PDF Report Generator (Option 14)[/bold yellow]\n\n"
        "Generate professional security reports:\n\n"
        "[bold]Report Types:[/bold]\n"
        "• [green]Quick Report[/green] - Network only\n"
        "• [green]Full Report[/green] - Network + Wi-Fi\n"
        "• [green]Network Report[/green] - Detailed device list\n"
        "• [green]Wi-Fi Report[/green] - Wireless networks\n"
        "• [green]Bandwidth Report[/green] - Usage statistics\n\n"
        "[bold]Features:[/bold]\n"
        "• [green]Clean Tables[/green] - Professional formatting\n"
        "• [green]Statistics[/green] - Device count, threats\n"
        "• [green]Risk Badges[/green] - Color-coded risks\n"
        "• [green]Timestamp[/green] - Generation time\n\n"
        "[bold]Requirements:[/bold]\n"
        "• [yellow]pip install reportlab[/yellow]\n\n"
        "[bold]Tip:[/bold] Run scans first for complete data.",
        border_style="cyan"
    ))

def show_tips():
    """نکات کاربردی"""
    clear_screen()
    print_header("TIPS & TRICKS")
    
    tips = [
        "[bold green]🔐 Network Security:[/bold green]",
        "  • Always change your router's default password",
        "  • Use WPA2 or WPA3 encryption (not WEP or WPA1)",
        "  • Set your Wi-Fi channel to the least congested one",
        "  • Close unnecessary router ports (Telnet, FTP)",
        "",
        "[bold blue]📡 Wi-Fi Improvement:[/bold blue]",
        "  • Use Wi-Fi Scanner to find the best channel",
        "  • Place router in a high, obstruction-free location",
        "  • Use 5GHz band for better speed",
        "",
        "[bold yellow]🌐 Network Troubleshooting:[/bold yellow]",
        "  • Use Auto Scan to detect new devices",
        "  • Use Internet Monitor to check for outages",
        "  • Use Traceroute to see internet routing path",
        "",
        "[bold cyan]🤖 Automation:[/bold cyan]",
        "  • Enable Action Mode for 24/7 monitoring",
        "  • Auto-save to database keeps history",
        "  • Daily PDF reports document everything",
        "",
        "[bold magenta]📁 Saved Files:[/bold magenta]",
        "  • scan_*.csv - Network scan results",
        "  • wifi_scan_*.csv - Wi-Fi scan results",
        "  • threat_alerts.json - Security alerts",
        "  • known_devices.json - Trusted devices",
        "  • internet_outages_*.json - Outage logs",
        "  • traceroute_*.txt - Traceroute results",
        "  • security_report_*.pdf - PDF reports"
    ]
    
    for tip in tips:
        if tip.startswith("[bold"):
            console.print(f"\n{tip}")
        else:
            console.print(f"  {tip}")

def show_help_menu():
    """منوی اصلی راهنما"""
    while True:
        clear_screen()
        print_header("HELP MENU")
        
        console.print("\n[bold cyan]📚 Help by Topic:[/bold cyan]\n")
        
        help_options = [
            ("1", "Overview", "All menu options explained"),
            ("2", "Network Scan", "Single IP and Quick scan"),
            ("3", "Wi-Fi Scanner", "Discover wireless networks"),
            ("4", "Traceroute", "Route tracing and diagnostics"),
            ("5", "Internet Monitor", "Track internet outages"),
            ("6", "Vulnerability Scanner", "Advanced vulnerability detection"),
            ("7", "Network Map", "Visual network topology"),
            ("8", "Bandwidth Monitor", "Real-time traffic monitoring"),
            ("9", "Database Manager", "SQLite database storage"),
            ("10", "Action Mode", "Fully automated security"),
            ("11", "PDF Report", "Professional report generation"),
            ("12", "Tips & Tricks", "Useful advice and suggestions"),
            ("b", "Back", "Return to main menu")
        ]
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Option", style="green", width=8)
        table.add_column("Topic", style="yellow", width=22)
        table.add_column("Description", style="white", width=45)
        
        for opt in help_options:
            table.add_row(opt[0], opt[1], opt[2])
        
        console.print(table)
        
        choice = input(f"\n{YELLOW}👉 Choose (or b to go back): {RESET}").strip().lower()
        
        if choice == 'b':
            break
        elif choice == '1':
            show_main_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '2':
            show_scan_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '3':
            show_wifi_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '4':
            show_traceroute_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '5':
            show_internet_monitor_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '6':
            show_vulnerability_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '7':
            show_network_map_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '8':
            show_bandwidth_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '9':
            show_database_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '10':
            show_action_mode_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '11':
            show_pdf_help()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        elif choice == '12':
            show_tips()
            input(f"\n{YELLOW}Press Enter...{RESET}")
        else:
            console.print("[red]Invalid option![/red]")
            input(f"\n{YELLOW}Press Enter...{RESET}")