<p align="center">
  <img src="https://img.shields.io/badge/Network-Security%20Scanner-blue?style=for-the-badge&logo=wireshark"/>
  <img src="https://img.shields.io/badge/Version-1.0-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Author-Payam%20Fekri-orange?style=for-the-badge"/>
</p>

# 🔒 Network Security Scanner | اسکنر امنیت شبکه

**📅 سال انتشار:** 2026  
**📄 مجوز:** تمامی حقوق محفوست (All rights reserved)  
**🌐 زبان:** پشتیبانی از فارسی و انگلیسی

> ابزاری حرفه‌ای برای اسکن شبکه، تشخیص تهدیدات امنیتی، مانیتورینگ اینترنت و تولید گزارش‌های امنیتی.

---

## ✨ ویژگی‌های کلیدی | Key Features

| دسته | قابلیت‌ها (EN/FA) |
| :--- | :--- |
| **🔍 اسکن شبکه** | Single IP Scan / اسکن تک IP • Quick Scan / اسکن سریع • Auto Scan / اسکن خودکار |
| **🛡️ امنیت** | Vulnerability Scanner / آسیب‌پذیری‌ها • Threat History / تاریخچه تهدیدات • Known Devices / دستگاه‌های شناخته شده |
| **📡 بی‌سیم** | Wi-Fi Scanner / اسکن وای‌فای • Channel Analysis / تحلیل کانال • Security Audit / ممیزی امنیت |
| **📊 مانیتورینگ** | Internet Monitor / قطعی اینترنت • Bandwidth Monitor / پهنای باند • Network Map / نقشه شبکه |
| **📄 گزارشات** | PDF Report / گزارش PDF • Database Manager / مدیریت دیتابیس • Auto Mode / حالت خودکار ۲۴ ساعته |

---

## 🚀 نصب و راه‌اندازی سریع | Quick Start

### فارسی
1. مخزن را کلون کنید:
```
git clone https://github.com/PayamFekri/Network-Security-Scanner.git
cd Network-Security-Scanner/codes
در صورت نیاز، کتابخانه‌های مورد نیاز را نصب کنید:

pip install -r requirements.txt
برنامه را اجرا کنید:

bash
python main.py
English
Clone the repository:

bash
git clone https://github.com/PayamFekri/Network-Security-Scanner.git
cd Network-Security-Scanner/codes
Install dependencies:

bash
pip install -r requirements.txt
Run the program:

bash
python main.py
🗺️ نقشه راه برنامه | Menu Overview
<details> <summary><b>📌 13 گزینه اصلی | 13 Main Options (Click to expand)</b></summary>
#	نام (EN)	نام (FA)	توضیح مختصر
1	Single IP Scan	اسکن تک IP	بررسی کامل یک دستگاه خاص
2	Quick Network Scan	اسکن سریع شبکه	یافتن تمام دستگاه‌های متصل
3	Auto Scan	اسکن خودکار	اسکن دوره‌ای با تایمر
4	Threat History	تاریخچه تهدیدات	نمایش هشدارهای قبلی
5	Known Devices	دستگاه‌های شناخته شده	مدیریت دستگاه‌های مطمئن
6	Wi-Fi Scanner	اسکن وای‌فای	شناسایی شبکه‌های بی‌سیم
7	Traceroute	ردیابی مسیر	نمایش مسیر تا مقصد
8	Internet Monitor	مانیتور اینترنت	ثبت قطعی‌های اینترنت
9	Vulnerability Scan	اسکن آسیب‌پذیری	شناسایی پورت‌های خطرناک
10	Network Map	نقشه شبکه	نمایش گرافیکی شبکه
11	Bandwidth Monitor	مانیتور پهنای باند	سرعت لحظه‌ای آپلود/دانلود
12	Database Manager	مدیریت دیتابیس	ذخیره و مدیریت تاریخچه
13	Auto Mode	حالت خودکار	نظارت خودکار ۲۴ ساعته
</details>
🧠 نکات امنیتی | Security Tips
اولویت	توصیه (FA)	Recommendation (EN)
🔴	رمز پیش‌فرض مودم را تغییر دهید	Change your modem's default password
🟠	از WPA2/WPA3 استفاده کنید (نه WEP)	Use WPA2/WPA3 (not WEP)
🟡	پورت‌های غیرضروری (Telnet, FTP) را ببندید	Close unnecessary ports (Telnet, FTP)
🟢	ویندوز را به‌روز نگه دارید	Keep Windows updated
⚠️ تذکر مهم: این ابزار فقط برای تست روی تجهیزات خودتان یا با اجازه کتبی از صاحب شبکه طراحی شده است.

📁 فایل‌های خروجی | Output Files
نام فایل	توضیحات
scan_*.csv	نتایج اسکن شبکه
wifi_scan_*.csv	نتایج اسکن وای‌فای
threat_alerts.json	هشدارهای امنیتی
known_devices.json	لیست دستگاه‌های شناخته شده
internet_outages_*.json	گزارش قطعی‌های اینترنت
network_scanner.db	دیتابیس اصلی (SQLite)
👨‍💻 ارتباط با نویسنده | Contact
پدیدآورنده: Payam Fekri

گیت‌هاب: github.com/PayamFekri

پروژه: Network-Security-Scanner

<p align="center"> <b>© 2026 Payam Fekri - تمامی حقوق محفوست | All Rights Reserved</b><br> <i>استفاده مسئولانه از این ابزار توصیه می‌شود</i> </p> ```