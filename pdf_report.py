# pdf_report_fixed.py - نسخه نهایی با جدول‌های مرتب

import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rich.console import Console
from utils import clear_screen, print_header, load_json_file
from config import GREEN, RED, YELLOW, CYAN, RESET

console = Console()

# ثبت فونت
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    FONT_NAME = 'DejaVu'
except:
    FONT_NAME = 'Helvetica'

def create_pdf_report():
    """تولید PDF با جدول‌های مرتب"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"security_report_{timestamp}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            leftMargin=50, rightMargin=50,
                            topMargin=50, bottomMargin=50)
    story = []
    
    # استایل‌ها
    styles = getSampleStyleSheet()
    
    # استایل عنوان با اسم جدید
    styles.add(ParagraphStyle(
        name='MyTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2E7D32'),
        alignment=TA_CENTER,
        spaceAfter=30
    ))
    
    # استایل هدر با اسم جدید
    styles.add(ParagraphStyle(
        name='MyHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1565C0'),
        spaceBefore=20,
        spaceAfter=10
    ))
    
    # استایل متن معمولی
    styles.add(ParagraphStyle(
        name='MyNormal',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=6
    ))
    
    # عنوان
    story.append(Paragraph("Network Security Report", styles['MyTitle']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['MyNormal']))
    story.append(Spacer(1, 20))
    
    # ========== سیستم ==========
    story.append(Paragraph("System Information", styles['MyHeading']))
    
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    sys_data = [
        ['Hostname', hostname],
        ['Local IP', local_ip],
        ['Report Time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    ]
    sys_table = Table(sys_data, colWidths=[80, 120])
    sys_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(sys_table)
    story.append(Spacer(1, 15))
    
    # ========== دستگاه‌ها ==========
    story.append(Paragraph("Network Devices", styles['MyHeading']))
    
    network_map = load_json_file("network_map.json", {})
    devices = network_map.get("devices", {})
    
    if devices:
        dev_data = [['IP', 'OS', 'Type', 'Ports']]
        for ip, device in devices.items():
            dev_data.append([
                ip,
                device.get("os_type", "Unknown")[:30],
                device.get("device_type", "-"),
                ','.join(map(str, device.get("ports", []))) or '-'
            ])
        
        dev_table = Table(dev_data, colWidths=[50, 90, 40, 60])
        dev_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), (colors.white, colors.HexColor('#F5F5F5'))),
        ]))
        story.append(dev_table)
    else:
        story.append(Paragraph("No devices found.", styles['MyNormal']))
    story.append(Spacer(1, 15))
    
    # ========== وای‌فای ==========
    story.append(Paragraph("Wi-Fi Networks", styles['MyHeading']))
    
    import glob
    wifi_data = [['SSID', 'Signal', 'Security']]
    for f in glob.glob("wifi_scan_*.csv"):
        try:
            with open(f, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:11]
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        ssid = parts[0][:25] if parts[0] else "Hidden"
                        signal = parts[2]
                        auth = parts[5] if len(parts) > 5 else "Unknown"
                        wifi_data.append([ssid, f"{signal}%", auth])
        except:
            pass
    
    if len(wifi_data) > 1:
        wifi_table = Table(wifi_data, colWidths=[100, 50, 80])
        wifi_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), (colors.white, colors.HexColor('#F5F5F5'))),
        ]))
        story.append(wifi_table)
    else:
        story.append(Paragraph("No Wi-Fi networks found.", styles['MyNormal']))
    story.append(Spacer(1, 15))
    
    # ========== تهدیدات ==========
    story.append(Paragraph("Security Threats", styles['MyHeading']))
    
    threats = load_json_file("threat_alerts.json", [])
    if threats:
        threat_data = [['IP', 'Risk', 'Details']]
        for t in threats[-10:]:
            threat_data.append([
                t.get("ip", "?"),
                t.get("risk_level", "unknown").upper(),
                str(len(t.get("threats", []))) + " threat(s)"
            ])
        
        threat_table = Table(threat_data, colWidths=[60, 50, 100])
        threat_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(threat_table)
    else:
        story.append(Paragraph("No threats detected.", styles['MyNormal']))
    
    
    story.append(Spacer(1, 30))
    footer = Paragraph(f"Report generated by Network Security Scanner | Created by Payam Fekri", styles['MyNormal'])
    story.append(footer)
    # ذخیره
    doc.build(story)
    console.print(f"{GREEN}✅ PDF saved to {filename}{RESET}")
    return filename

def pdf_report_menu():
    """منوی گزارش PDF"""
    while True:
        clear_screen()
        print_header("PDF REPORT GENERATOR")
        
        console.print("\n[bold cyan]📄 Simple PDF Report (Clean tables)[/bold cyan]\n")
        
        console.print("[1] Generate PDF Report")
        console.print("[2] View saved reports")
        console.print("[b] Back to main menu")
        
        choice = input(f"\n{YELLOW}👉 Choose: {RESET}").strip().lower()
        
        if choice == 'b':
            break
        
        elif choice == '1':
            console.print(f"\n{YELLOW}Generating PDF report...{RESET}")
            create_pdf_report()
            input(f"\nPress Enter...")
        
        elif choice == '2':
            import glob
            reports = glob.glob("security_report_*.pdf")
            if reports:
                console.print(f"\n{CYAN}Saved reports ({len(reports)}):{RESET}")
                for r in sorted(reports)[-10:]:
                    size = os.path.getsize(r) / 1024
                    console.print(f"  - {r} ({size:.1f} KB)")
            else:
                console.print(f"\n{YELLOW}No reports found{RESET}")
            input(f"\nPress Enter...")
        
        else:
            console.print(f"{RED}Invalid choice{RESET}")
            input(f"\nPress Enter...")