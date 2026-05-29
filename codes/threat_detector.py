from datetime import datetime
from config import *
from utils import load_json_file, save_json_file

class ThreatDetector:
    
    @staticmethod
    def analyze_device(ip, os_name, open_ports):
        """تحلیل امنیتی"""
        threats = []
        risk_level = "safe"
        
        for port in open_ports:
            if port in CRITICAL_PORTS:
                threats.append({
                    "type": "critical",
                    "port": port,
                    "message": f"Critical port {port} open: {CRITICAL_PORTS[port]}"
                })
                risk_level = "critical"
            elif port in WARNING_PORTS:
                if risk_level != "critical":
                    risk_level = "warning"
                threats.append({
                    "type": "warning",
                    "port": port,
                    "message": f"Warning: Port {port} open - {WARNING_PORTS[port]}"
                })
        
        return {
            "ip": ip,
            "os": os_name,
            "risk_level": risk_level,
            "threats": threats,
            "timestamp": datetime.now().isoformat(),
            "open_ports": open_ports
        }

def save_alert(alert):
    """ذخیره هشدار"""
    alerts = load_json_file(ALERT_LOG_FILE, [])
    alerts.append(alert)
    if len(alerts) > 100:
        alerts = alerts[-100:]
    save_json_file(ALERT_LOG_FILE, alerts)

def display_alert(analysis):
    """نمایش هشدار"""
    from config import RED, YELLOW, RESET
    
    if analysis['risk_level'] == "critical":
        print(f"\n{RED}╔══════════════════════════════════════════════════════════╗{RESET}")
        print(f"{RED}║                    🚨 CRITICAL THREAT! 🚨                    ║{RESET}")
        print(f"{RED}╚══════════════════════════════════════════════════════════╝{RESET}")
        print(f"{RED}[!] Device: {analysis['ip']} - {analysis['os']}{RESET}")
        for threat in analysis['threats']:
            if threat['type'] == 'critical':
                print(f"{RED}    ⚠ {threat['message']}{RESET}")
    elif analysis['risk_level'] == "warning":
        print(f"\n{YELLOW}╔══════════════════════════════════════════════════════════╗{RESET}")
        print(f"{YELLOW}║                    ⚠ WARNING DETECTED ⚠                    ║{RESET}")
        print(f"{YELLOW}╚══════════════════════════════════════════════════════════╝{RESET}")
        print(f"{YELLOW}[!] Device: {analysis['ip']} - {analysis['os']}{RESET}")
        for threat in analysis['threats']:
            print(f"{YELLOW}    ⚠ {threat['message']}{RESET}")
    
    save_alert(analysis)