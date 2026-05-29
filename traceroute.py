# traceroute.py - نسخه با جدول زیبا

import subprocess
import re
from datetime import datetime
import os

# رنگ‌ها
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(f"\n{CYAN}{'='*50}{RESET}")
    print(f"{GREEN}{title.center(50)}{RESET}")
    print(f"{CYAN}{'='*50}{RESET}")

def check_internet():
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def is_local_target(target):
    if not target:
        return False
    if target.startswith('192.168.') or target.startswith('10.') or target.startswith('172.'):
        return True
    if target == 'localhost' or target == '127.0.0.1':
        return True
    return False

def run_traceroute(target, max_hops=30):
    try:
        is_local = is_local_target(target)
        timeout_val = 8 if is_local else 25
        
        result = subprocess.run(
            ["tracert", "-d", "-h", str(max_hops), "-w", str(timeout_val * 1000), target],
            capture_output=True,
            text=True,
            timeout=timeout_val + 5
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def parse_traceroute_output(output):
    hops = []
    if not output or output == "TIMEOUT" or output.startswith("ERROR"):
        return hops
    
    lines = output.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = re.match(r'^(\d+)\s+([\d<]+ ms)?\s+([\d<]+ ms)?\s+([\d<]+ ms)?\s+(.+)$', line)
        if match:
            hop_num = int(match.group(1))
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
            ip = ip_match.group(1) if ip_match else 'Timeout'
            
            times = []
            for t in match.groups()[1:4]:
                if t and t != '*':
                    times.append(t)
            
            hops.append({'hop': hop_num, 'ip': ip, 'times': times})
        elif 'Request timed out' in line or '*' in line:
            if hops and hops[-1]['ip'] == '*':
                continue
            hops.append({'hop': len(hops) + 1, 'ip': '*', 'times': ['*']})
    
    return hops

def display_traceroute(target, hops):
    """نمایش نتایج به صورت جدول زیبا"""
    if not hops:
        print(f"{RED}[!] No route information received!{RESET}")
        return
    
    # هدر جدول
    print(f"\n{CYAN}╔{'═' * 58}╗{RESET}")
    print(f"{GREEN}║{'🛤️ Traceroute to ' + target.center(44)}║{RESET}")
    print(f"{CYAN}╚{'═' * 58}╝{RESET}")
    
    # سرستون‌ها
    print(f"{CYAN}┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{RESET}")
    print(f"{CYAN}┃{RESET}{'Hop':^6}{CYAN}┃{RESET}{'IP Address':^20}{CYAN}┃{RESET}{'Response Time':^28}{CYAN}┃{RESET}")
    print(f"{CYAN}┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩{RESET}")
    
    for hop in hops:
        if hop['ip'] == '*':
            time_str = f"{YELLOW}Timeout{RESET}"
            ip_str = f"{RED}---{RESET}"
        else:
            # نمایش حداکثر 3 زمان
            times_show = hop['times'][:3] if hop['times'] else ['<1 ms']
            time_str = f"{GREEN}{', '.join(times_show)}{RESET}"
            ip_str = f"{BLUE}{hop['ip']}{RESET}"
        
        print(f"{CYAN}│{RESET} {hop['hop']:<5} {CYAN}│{RESET} {ip_str:<18} {CYAN}│{RESET} {time_str:<26} {CYAN}│{RESET}")
    
    print(f"{CYAN}└━━━━━━┴━━━━━━━━━━━━━━━━━━━━┴━━━━━━━━━━━━━━━━━━━━━━━━━━━━┘{RESET}")
    
    # نتیجه نهایی
    last_hop = hops[-1] if hops else None
    if last_hop and last_hop['ip'] == target:
        print(f"\n{GREEN}✅ Successfully reached {target}{RESET}")
    elif last_hop and last_hop['ip'] != '*':
        print(f"\n{YELLOW}⚠️ Stopped at {last_hop['ip']}{RESET}")

def save_results(target, hops):
    if not hops:
        return
        
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"traceroute_{target.replace('.', '_')}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Traceroute to {target}\n")
        f.write(f"Time: {datetime.now()}\n")
        f.write("-" * 50 + "\n\n")
        f.write(f"{'Hop':<4} {'IP Address':<20} {'Times'}\n")
        f.write("-" * 50 + "\n")
        for hop in hops:
            times_str = ', '.join(hop['times']) if hop['times'] else '*'
            f.write(f"{hop['hop']:<4} {hop['ip']:<20} {times_str}\n")
    
    print(f"{GREEN}✅ Saved to {filename}{RESET}")

def traceroute_menu():
    """منوی اصلی traceroute"""
    while True:
        clear_screen()
        print_header("TRACEROUTE (ROUTE TRACING)")
        
        has_internet = check_internet()
        
        if has_internet:
            print(f"{GREEN}✅ Internet connection detected{RESET}")
        else:
            print(f"{RED}❌ No internet connection{RESET}")
            print(f"{YELLOW}   You can only trace local IPs (192.168.x.x, 127.0.0.1){RESET}")
        
        print(f"\n{CYAN}[1]{RESET} Trace route to IP/Domain")
        print(f"{CYAN}[2]{RESET} Trace local router {GREEN}(192.168.1.1){RESET}")
        print(f"{CYAN}[3]{RESET} Trace localhost {GREEN}(127.0.0.1){RESET}")
        print(f"{CYAN}[b]{RESET} Back to main menu")
        
        choice = input(f"\n{YELLOW}👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            break
        
        elif choice == '2':
            target = "192.168.1.1"
            clear_screen()
            print_header(f"Tracing: {target} (Your Router)")
            print(f"\n{YELLOW}⏳ Tracing to your router...{RESET}\n")
            
            output = run_traceroute(target, 10)
            
            if output == "TIMEOUT":
                print(f"{RED}❌ Router not responding!{RESET}")
            elif output.startswith("ERROR"):
                print(f"{RED}❌ {output}{RESET}")
            else:
                hops = parse_traceroute_output(output)
                if hops:
                    display_traceroute(target, hops)
                    save_choice = input(f"\n{YELLOW}💾 Save results? (y/n): {RESET}").strip().lower()
                    if save_choice == 'y':
                        save_results(target, hops)
                else:
                    print(f"{RED}❌ Could not trace to router{RESET}")
            
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        
        elif choice == '3':
            target = "127.0.0.1"
            clear_screen()
            print_header(f"Tracing: {target} (Localhost)")
            print(f"\n{YELLOW}⏳ Tracing to localhost...{RESET}\n")
            
            output = run_traceroute(target, 5)
            
            if output == "TIMEOUT":
                print(f"{RED}❌ Localhost not responding?{RESET}")
            elif output.startswith("ERROR"):
                print(f"{RED}❌ {output}{RESET}")
            else:
                hops = parse_traceroute_output(output)
                if hops:
                    display_traceroute(target, hops)
                else:
                    print(f"{GREEN}✅ Localhost is responding{RESET}")
            
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        
        elif choice == '1':
            target = input(f"{YELLOW}🌐 Enter IP or domain: {RESET}").strip()
            if not target:
                continue
            
            if not is_local_target(target) and not has_internet:
                print(f"{RED}❌ No internet! Cannot trace external targets.{RESET}")
                input(f"\n{YELLOW}Press Enter...{RESET}")
                continue
            
            max_hops = 30
            try:
                hops_input = input(f"{YELLOW}📏 Max hops (1-30, Enter=30): {RESET}").strip()
                if hops_input and hops_input.isdigit():
                    max_hops = min(int(hops_input), 30)
            except:
                pass
            
            clear_screen()
            print_header(f"Tracing: {target}")
            print(f"\n{YELLOW}⏳ Tracing route to {target} (max {max_hops} hops)...{RESET}\n")
            
            output = run_traceroute(target, max_hops)
            
            if output == "TIMEOUT":
                print(f"{RED}❌ Timeout! Try a local IP instead.{RESET}")
            elif output.startswith("ERROR"):
                print(f"{RED}❌ {output}{RESET}")
            else:
                hops = parse_traceroute_output(output)
                if hops:
                    display_traceroute(target, hops)
                    save_choice = input(f"\n{YELLOW}💾 Save results? (y/n): {RESET}").strip().lower()
                    if save_choice == 'y':
                        save_results(target, hops)
                else:
                    print(f"{RED}❌ No route information received{RESET}")
            
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        
        else:
            print(f"{RED}❌ Invalid choice! Enter 1, 2, 3, or b{RESET}")
            input(f"\n{YELLOW}Press Enter...{RESET}")