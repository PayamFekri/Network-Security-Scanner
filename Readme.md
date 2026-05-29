# Network Security Scanner

**Author:** Payam Fekri  
**Version:** 1.0  
**Year:** 2026  
**GitHub:** [https://github.com/PayamFekri](https://github.com/PayamFekri)

> A professional tool for network scanning, threat detection, internet monitoring, and generating security reports.

---

## English | [فارسی](#persian-version)

## Features

| Option | Description |
|--------|-------------|
| 1 | Single IP Scan – deep scan of a specific device |
| 2 | Fast Network Scan – discover all active devices |
| 3 | Automatic Scan – periodic scanning (5/15/30 min) |
| 4 | Threat History – view past security alerts |
| 5 | Known Devices – manage trusted devices |
| 6 | WiFi Scan – detect nearby wireless networks |
| 7 | Traceroute – step‑by‑step path to destination |
| 8 | Internet Monitor – log outages and instability |
| 9 | Advanced Vulnerability Scan – detect risky ports (FTP, Telnet, SMB, RDP, etc.) |
| 10 | Network Map – graphical tree view of your network |
| 11 | Bandwidth Monitor – real‑time upload/download speed |
| 12 | Database Management – store all scans in SQLite |
| 13 | Automatic Mode – hands‑off scheduled scanning with alerts |
| 14 | PDF Report – professional security report (requires reportlab) |
| 20 | Help – this guide |
| 0 | Exit |

## Output Files (saved in the program folder)

- `scan_*.csv` – network scan results
- `wifi_scan_*.csv` – WiFi scan results
- `threat_alerts.json` – security alerts
- `known_devices.json` – trusted devices list
- `internet_outages_*.json` – outage logs
- `traceroute_*.txt` – traceroute results
- `security_report_*.pdf` – PDF reports
- `network_scanner.db` – main SQLite database

## Security Recommendations

1. **Change your modem’s default password**
2. **Use WPA2 or WPA3 encryption** – avoid WEP/WPA1
3. **Close unnecessary ports** – disable Telnet and FTP
4. **Optimise your WiFi channel** – choose the least congested one
5. **Keep Windows updated** – install security patches

> **Important:** Always test on your own equipment. Written permission is required before scanning other people’s networks.

> this project was written during an internet outage 

---

## <a name="persian-version"></a>نسخه فارسی

**نویسنده:** پیام فکری  
**نسخه:** 1.0  
**سال انتشار:** 2026  

## قابلیت‌ها

| گزینه | توضیح |
|-------|-------|
| 1 | اسکن تک IP – بررسی کامل یک دستگاه خاص |
| 2 | اسکن سریع شبکه – پیدا کردن تمام دستگاه‌های روشن |
| 3 | اسکن خودکار – اسکن دوره‌ای (۵/۱۵/۳۰ دقیقه) |
| 4 | تاریخچه تهدیدات – مشاهده هشدارهای قبلی |
| 5 | دستگاه‌های شناخته شده – مدیریت دستگاه‌های مطمئن |
| 6 | اسکن وای‌فای – شناسایی شبکه‌های بی‌سیم اطراف |
| 7 | ردیابی مسیر – نمایش گام‌به‌گام مسیر تا مقصد |
| 8 | مانیتور اینترنت – ثبت قطعی‌ها و ناپایداری |
| 9 | اسکن آسیب‌پذیری پیشرفته – شناسایی پورت‌های خطرناک (FTP، Telnet، SMB، RDP و ...) |
| 10 | نقشه شبکه – نمایش گرافیکی درختی از شبکه |
| 11 | مانیتور پهنای باند – نمایش لحظه‌ای سرعت آپلود و دانلود |
| 12 | مدیریت دیتابیس – ذخیره همه اسکن‌ها در SQLite |
| 13 | حالت خودکار – اسکن زمان‌بندی شده بدون دخالت شما |
| 14 | گزارش PDF – گزارش حرفه‌ای امنیتی (نیازمند reportlab) |
| 20 | راهنما – این صفحه |
| 0 | خروج |

## فایل‌های ذخیره شده (در پوشه برنامه)

- `scan_*.csv` – نتایج اسکن شبکه
- `wifi_scan_*.csv` – نتایج اسکن وای‌فای
- `threat_alerts.json` – هشدارهای امنیتی
- `known_devices.json` – لیست دستگاه‌های شناخته شده
- `internet_outages_*.json` – گزارش قطعی‌های اینترنت
- `traceroute_*.txt` – نتایج ردیابی مسیر
- `security_report_*.pdf` – گزارش‌های PDF
- `network_scanner.db` – دیتابیس اصلی برنامه

## توصیه‌های امنیتی

۱. **رمز مودم خود را تغییر دهید** – هرگز از رمز پیش‌فرض استفاده نکنید  
۲. **از رمزگذاری WPA2 یا WPA3 استفاده کنید** – از WEP و WPA1 استفاده نکنید  
۳. **پورت‌های غیرضروری مودم را ببندید** – Telnet و FTP را غیرفعال کنید  
۴. **کانال وای‌فای خود را تنظیم کنید** – از کم‌تداخل‌ترین کانال استفاده کنید  
۵. **ویندوز خود را به‌روز نگه دارید** – وصله‌های امنیتی را نصب کنید  

> **نکته مهم:** همیشه روی تجهیزات خودتان تست کنید. برای اسکن شبکه دیگران حتماً اجازه کتبی داشته باشید.

> این پروژه در زمان قطعی اینترنت در ایران نوشته شده است.
---

## Quick Run & EXE Creation

### Run Directly (Python)

```bash
python main.py
```

### Create EXE with Icon

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Place `icon.ico` in the program folder

3. Build:
```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

> Output: `dist/network_scanner.exe`

### Without Icon
```bash
pyinstaller --onefile --windowed main.py
```


Ⓒ 2025 Payam Fekri – All rights reserved