# فایل جدید wifi_test.py - فقط برای تست مودم خودت

def test_common_passwords_on_own_router(router_ip="192.168.1.1"):
    """تست رمزهای رایج روی مودم خودت (فقط تست امنیتی شخصی)"""
    
    common_passwords = [
        "admin", "1234", "password", "12345678", "123456789",
        "admin123", "root", "user", "12345", "00000000"
    ]
    
    print(f"[*] Testing common passwords on {router_ip} (YOUR router only)")
    print("[!] This should only be done on your own device!\n")
    
    for pwd in common_passwords:
        # این فقط یه شبیه‌سازی ساده است
        print(f"   Testing: {pwd}...")
        # در واقعیت نیاز به ابزارهای خاص مثل hydra داره
    
    print("\n[!] Real testing requires tools like:")
    print("   - Hydra (for HTTP/FTP/SSH)")
    print("   - Aircrack-ng (for Wi-Fi password)")
    print("   - Wireshark (for packet analysis)")

# اجرا
test_common_passwords_on_own_router()