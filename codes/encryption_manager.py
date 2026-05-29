# encryption_manager.py - رمزنگاری فایل‌ها

import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from base64 import urlsafe_b64encode
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from utils import clear_screen, print_header
from config import GREEN, RED, YELLOW, CYAN, BLUE, RESET

console = Console()

KEY_FILE = ".encryption_key"
PASSWORD_FILE = ".password_hash"

class EncryptionManager:
    """کلاس مدیریت رمزنگاری فایل‌ها"""
    
    def __init__(self):
        self.key = None
        self.cipher = None
        self.is_initialized = False
        self.load_or_create_key()
    
    def _derive_key_from_password(self, password):
        """دریافت کلید از رمز عبور"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'network_scanner_salt_2024',
            iterations=100000,
        )
        key = urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def initialize_with_password(self, password):
        """راه‌اندازی با رمز عبور"""
        self.key = self._derive_key_from_password(password)
        self.cipher = Fernet(self.key)
        self.is_initialized = True
        
        # ذخیره رمز (نه خود رمز، بلکه هش شده)
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        with open(PASSWORD_FILE, 'w') as f:
            f.write(password_hash)
        
        return True
    
    def load_or_create_key(self):
        """بارگذاری یا ایجاد کلید"""
        if os.path.exists(KEY_FILE):
            try:
                with open(KEY_FILE, 'rb') as f:
                    self.key = f.read()
                self.cipher = Fernet(self.key)
                self.is_initialized = True
                return True
            except:
                pass
        
        # ایجاد کلید جدید
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.is_initialized = True
        
        with open(KEY_FILE, 'wb') as f:
            f.write(self.key)
        
        return True
    
    def encrypt_file(self, filepath):
        """رمزنگاری یک فایل"""
        if not self.is_initialized or not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            encrypted = self.cipher.encrypt(data)
            
            with open(filepath + '.enc', 'wb') as f:
                f.write(encrypted)
            
            # حذف فایل اصلی (اختیاری)
            # os.remove(filepath)
            
            return True
        except Exception as e:
            console.print(f"{RED}Encryption failed: {e}{RESET}")
            return False
    
    def decrypt_file(self, filepath):
        """رمزگشایی یک فایل"""
        if not self.is_initialized:
            return False
        
        enc_path = filepath if filepath.endswith('.enc') else filepath + '.enc'
        
        if not os.path.exists(enc_path):
            return False
        
        try:
            with open(enc_path, 'rb') as f:
                encrypted = f.read()
            
            decrypted = self.cipher.decrypt(encrypted)
            
            # ذخیره به عنوان فایل اصلی
            original_path = enc_path.replace('.enc', '')
            with open(original_path, 'wb') as f:
                f.write(decrypted)
            
            return True
        except Exception as e:
            console.print(f"{RED}Decryption failed: {e}{RESET}")
            return False
    
    def encrypt_json_file(self, filepath):
        """رمزنگاری فایل JSON"""
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            json_str = json.dumps(data, indent=2, default=str)
            encrypted = self.cipher.encrypt(json_str.encode())
            
            with open(filepath + '.enc', 'wb') as f:
                f.write(encrypted)
            
            return True
        except Exception as e:
            console.print(f"{RED}JSON encryption failed: {e}{RESET}")
            return False
    
    def decrypt_json_file(self, filepath):
        """رمزگشایی فایل JSON"""
        enc_path = filepath if filepath.endswith('.enc') else filepath + '.enc'
        
        if not os.path.exists(enc_path):
            return None
        
        try:
            with open(enc_path, 'rb') as f:
                encrypted = f.read()
            
            decrypted = self.cipher.decrypt(encrypted)
            data = json.loads(decrypted.decode())
            
            return data
        except Exception as e:
            console.print(f"{RED}JSON decryption failed: {e}{RESET}")
            return None
    
    def encrypt_all_logs(self):
        """رمزنگاری همه فایل‌های لاگ"""
        log_files = [
            "threat_alerts.json",
            "known_devices.json",
            "network_map.json",
            "bandwidth_report_*.txt",
            "vulnerability_report_*.json",
            "auto_threat_report_*.json",
            "daily_report_*.txt"
        ]
        
        import glob
        encrypted_count = 0
        
        for pattern in log_files:
            for filepath in glob.glob(pattern):
                if not filepath.endswith('.enc'):
                    if self.encrypt_file(filepath):
                        encrypted_count += 1
                        console.print(f"{GREEN}  Encrypted: {filepath}{RESET}")
        
        return encrypted_count
    
    def show_status(self):
        """نمایش وضعیت رمزنگاری"""
        console.print(f"\n{CYAN}{'='*50}{RESET}")
        console.print(f"{GREEN}🔐 ENCRYPTION STATUS{RESET}")
        console.print(f"{CYAN}{'='*50}{RESET}")
        
        if self.is_initialized:
            console.print(f"\n{GREEN}✅ Encryption is ACTIVE{RESET}")
            console.print(f"   Key length: {len(self.key) if self.key else 0} bytes")
            
            # پیدا کردن فایل‌های رمز شده
            import glob
            encrypted_files = glob.glob("*.enc")
            if encrypted_files:
                console.print(f"\n{YELLOW}Encrypted files ({len(encrypted_files)}):{RESET}")
                for f in encrypted_files[:10]:
                    console.print(f"  - {f}")
                if len(encrypted_files) > 10:
                    console.print(f"  ... and {len(encrypted_files)-10} more")
            else:
                console.print(f"\n{YELLOW}No encrypted files found{RESET}")
        else:
            console.print(f"\n{RED}❌ Encryption is INACTIVE{RESET}")

# نمونه گلوبال
encryption = EncryptionManager()

def setup_encryption():
    """راه‌اندازی رمزنگاری با رمز عبور"""
    clear_screen()
    print_header("ENCRYPTION SETUP")
    
    console.print(f"\n{CYAN}Set a password to protect your log files{RESET}")
    console.print("[dim]All JSON and TXT files will be encrypted[/dim]\n")
    
    password = input(f"{YELLOW}Enter password: {RESET}")
    confirm = input(f"{YELLOW}Confirm password: {RESET}")
    
    if password != confirm:
        console.print(f"{RED}Passwords do not match!{RESET}")
        input(f"\nPress Enter...")
        return False
    
    if len(password) < 4:
        console.print(f"{RED}Password must be at least 4 characters!{RESET}")
        input(f"\nPress Enter...")
        return False
    
    success = encryption.initialize_with_password(password)
    
    if success:
        console.print(f"{GREEN}✅ Encryption initialized successfully!{RESET}")
        console.print(f"{YELLOW}⚠️ Don't forget your password! You'll need it to decrypt files.{RESET}")
    else:
        console.print(f"{RED}Failed to initialize encryption{RESET}")
    
    input(f"\nPress Enter...")
    return success

def encryption_menu():
    """منوی رمزنگاری"""
    while True:
        clear_screen()
        print_header("ENCRYPTION MANAGER")
        
        console.print("\n[bold cyan]🔐 File Encryption - Protect your logs[/bold cyan]\n")
        
        console.print("[1] Show encryption status")
        console.print("[2] Encrypt all log files")
        console.print("[3] Decrypt a file")
        console.print("[4] Setup/Change password")
        console.print("[b] Back to main menu")
        
        choice = input(f"\n{YELLOW}👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            break
        
        elif choice == '1':
            encryption.show_status()
            input(f"\nPress Enter...")
        
        elif choice == '2':
            console.print(f"\n{YELLOW}Encrypting all log files...{RESET}")
            count = encryption.encrypt_all_logs()
            console.print(f"{GREEN}✅ Encrypted {count} file(s){RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '3':
            filename = input(f"{YELLOW}Enter filename to decrypt: {RESET}").strip()
            if filename:
                if encryption.decrypt_file(filename):
                    console.print(f"{GREEN}✅ Decrypted: {filename}{RESET}")
                else:
                    console.print(f"{RED}Failed to decrypt{RESET}")
            input(f"\nPress Enter...")
        
        elif choice == '4':
            setup_encryption()
        
        else:
            console.print(f"{RED}Invalid choice{RESET}")
            input(f"\nPress Enter...")