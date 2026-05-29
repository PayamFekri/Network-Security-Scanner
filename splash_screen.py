# splash_screen.py - صفحه خوش‌آمدگویی با نوار پیشرفت

import time
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.text import Text

console = Console()

def show_splash_screen():
    """نمایش صفحه خوش‌آمدگویی با نوار پیشرفت"""
    
    # بنر اولیه
    banner = Text()
    banner.append("╔══════════════════════════════════════════════════════════════╗\n", style="cyan")
    banner.append("║", style="cyan")
    banner.append("     🔒 Network Security Scanner v5.0                          ", style="bold green")
    banner.append("║\n", style="cyan")
    banner.append("║", style="cyan")
    banner.append("     👨‍💻 Created by: Payam Fekri                               ", style="yellow")
    banner.append("║\n", style="cyan")
    banner.append("║", style="cyan")
    banner.append("     🛡️ For authorized security testing only                  ", style="dim")
    banner.append("║\n", style="cyan")
    banner.append("╚══════════════════════════════════════════════════════════════╝", style="cyan")
    
    console.print(Panel(banner, border_style="cyan", padding=(1, 2)))
    
    # نوار پیشرفت
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=False
    ) as progress:
        
        task = progress.add_task("[cyan]Initializing Network Scanner...", total=100)
        
        # مراحل بارگذاری
        stages = [
            (10, "Loading core modules..."),
            (25, "Checking network interfaces..."),
            (40, "Initializing database..."),
            (55, "Loading Wi-Fi scanner..."),
            (70, "Preparing security modules..."),
            (85, "Starting threat detector..."),
            (95, "Finalizing setup..."),
            (100, "Ready!")
        ]
        
        for percent, stage in stages:
            progress.update(task, description=f"[cyan]{stage}", completed=percent)
            time.sleep(0.3)
    
    console.print("\n[green]✅ System ready![/green]")
    console.print("[dim]Press Enter to continue...[/dim]")
    input()

def show_simple_splash():
    """نمایش صفحه ساده بدون نیاز به Enter"""
    
    # پاک کردن صفحه
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # بنر
    banner =  """
    ╔══════════════════════════════════════════════════════════════╗
    ║     🔒 Network Security Scanner v1.0                        
    ║     👨‍💻 Created by: Payam Fekri                              
    ║     📅 2026                                                 
    ║     🛡️ For authorized security testing only                 
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner)
    
    print()
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=50),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=False
    ) as progress:
        task = progress.add_task("[cyan]Loading...", total=100)
        
        for i in range(0, 101, 2):
            progress.update(task, completed=i)
            time.sleep(0.23)
    
    console.print("\n[green]✅ Ready![/green]")
    time.sleep(0.7)

def show_ascii_splash():
    """نمایش صفحه با کاراکترهای ASCII ساده (بدون rich)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🔒 Network Security Scanner v1.0                        ║
    ║     👨‍💻 Created by: Payam Fekri                              ║
    ║     🛡️ For authorized security testing only                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # نوار پیشرفت ASCII
    print("Loading", end="")
    for i in range(20):
        print(".", end="", flush=True)
        time.sleep(0.1)
    print(" [OK]\n")
    
    time.sleep(0.5)

#خب ببین میخوام اینو تبدیل به فایل exe کنم . به طوری که اسمشو بزارم Network Security Scanner و ایکونش رو هم خودم انتخاب کنم . دیگه چی باید باشه ؟
#خیل خب توضیحات فارسی هم به طور کامل برام اماده کن