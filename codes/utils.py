import json
import csv
from datetime import datetime
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from config import *
import os

def show_progress_rich(total, description="Scanning"):
    """نوار پیشرفت حرفه‌ای با rich"""
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    
    progress = Progress(
        TextColumn(f"[cyan]{description}[/cyan]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=None
    )
    return progress

def save_to_csv(data, filename_prefix, scan_type):
    """ذخیره نتایج در CSV"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename_prefix}_{scan_type}_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        if scan_type == "single":
            fieldnames = ['IP', 'TTL', 'OS', 'Open_Ports', 'Risk_Level', 'Scan_Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'IP': data['ip'],
                'TTL': data['ttl'],
                'OS': data['os'],
                'Open_Ports': ','.join(map(str, data['ports'])),
                'Risk_Level': data.get('risk_level', 'unknown'),
                'Scan_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            fieldnames = ['IP', 'TTL', 'OS', 'Icon', 'Open_Ports']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device in data:
                writer.writerow({
                    'IP': device['ip'],
                    'TTL': device['ttl'],
                    'OS': device['os'],
                    'Icon': device['icon'],
                    'Open_Ports': ','.join(map(str, device['ports']))
                })
    
    print(f"[✓] CSV saved to {filename}")
    return filename

def load_json_file(filename, default=[]):
    """بارگذاری فایل JSON"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return default

def save_json_file(filename, data):
    """ذخیره فایل JSON"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def clear_screen():
    """پاک کردن صفحه"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """چاپ هدر"""
    print(f"\n{CYAN}╔{'═' * 50}╗{RESET}")
    print(f"{GREEN}║{title.center(50)}║{RESET}")
    print(f"{CYAN}╚{'═' * 50}╝{RESET}")
    
# utils.py - اضافه کردن این تابع به انتهای فایل

def clear_screen():
    """پاک کردن صفحه کنسول"""
    # ویندوز: cls, لینوکس/مک: clear
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_and_continue():
    """پاک کردن صفحه و منتظر ماندن برای ادامه"""
    input("\n[yellow]Press Enter to continue...[/yellow]")
    clear_screen()

def show_progress_rich(total, description="Scanning"):
    """نوار پیشرفت حرفه‌ای با rich"""
    progress = Progress(
        TextColumn(f"[cyan]{description}[/cyan]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=None
    )
    return progress

def save_to_csv(data, filename_prefix, scan_type):
    """ذخیره نتایج در CSV"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename_prefix}_{scan_type}_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        if scan_type == "single":
            fieldnames = ['IP', 'TTL', 'OS', 'Open_Ports', 'Risk_Level', 'Scan_Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'IP': data['ip'],
                'TTL': data['ttl'],
                'OS': data['os'],
                'Open_Ports': ','.join(map(str, data['ports'])),
                'Risk_Level': data.get('risk_level', 'unknown'),
                'Scan_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            fieldnames = ['IP', 'TTL', 'OS', 'Icon', 'Open_Ports']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device in data:
                writer.writerow({
                    'IP': device['ip'],
                    'TTL': device['ttl'],
                    'OS': device['os'],
                    'Icon': device['icon'],
                    'Open_Ports': ','.join(map(str, device['ports']))
                })
    
    print(f"[✓] CSV saved to {filename}")
    return filename

def load_json_file(filename, default=[]):
    """بارگذاری فایل JSON"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return default

def save_json_file(filename, data):
    """ذخیره فایل JSON"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def print_header(title):
    """چاپ هدر"""
    from config import CYAN, GREEN, RESET
    print(f"\n{CYAN}╔{'═' * 50}╗{RESET}")
    print(f"{GREEN}║{title.center(50)}║{RESET}")
    print(f"{CYAN}╚{'═' * 50}╝{RESET}")