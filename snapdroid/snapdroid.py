import subprocess
import os
import sys
import time
import argparse
import re

COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
COLOR_RESET = "\033[0m"

# Colorized ASCII art
ASCII_ART = fr"""
{COLOR_GREEN}   _____                   ____             _     __   {COLOR_GREEN}
{COLOR_GREEN}  / ___/____  ____ _____  / __ \_________  (_)___/ /   {COLOR_GREEN}{COLOR_YELLOW}Android{COLOR_RESET}
{COLOR_GREEN}  \__ \/ __ \/ __ `/ __ \/ / / / ___/ __ \/ / __  /    {COLOR_GREEN}{COLOR_YELLOW}Screenshot{COLOR_RESET}
{COLOR_GREEN} ___/ / / / / /_/ / /_/ / /_/ / /  / /_/ / / /_/ /     {COLOR_GREEN}{COLOR_YELLOW}& Recording{COLOR_RESET}
{COLOR_GREEN}/____/_/ /_/\__,_/ .___/_____/_/   \____/_/\__,_/      {COLOR_GREEN}{COLOR_YELLOW}Tool v1.0.3{COLOR_RESET}
{COLOR_GREEN}                /_/                                     {COLOR_RESET}
{COLOR_GREEN}                          With <3 by Sid (github.com/dr34mhacks){COLOR_RESET}
"""



def print_formatted_message(message, details=None, is_error=False):
    color = COLOR_RED if is_error else COLOR_GREEN
    width = max(len(message), len(details) if details else 0, 50)
    
    print(f"{color}+{'-' * (width + 2)}+{COLOR_RESET}")
    print(f"{color}| {message.ljust(width)} |{COLOR_RESET}")
    if details:
        print(f"{color}| {details.ljust(width)} |{COLOR_RESET}")
    print(f"{color}+{'-' * (width + 2)}+{COLOR_RESET}")

def get_foreground_app_android():
    try:
        output = subprocess.check_output(['adb', 'shell', 'dumpsys window | grep mCurrentFocus'], stderr=subprocess.STDOUT).decode('utf-8')
        package = output.split()[-1].split('/')[0]
        if package and not package.startswith('com.android') and not package.endswith('}'):
            return package
        print(f"{COLOR_YELLOW}Warning: No foreground app detected. Current focus: {package}{COLOR_RESET}")
        return None
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        print_formatted_message("Error: Failed to detect foreground app", f"Details: {error_msg}", is_error=True)
        return None
    except Exception as e:
        print_formatted_message("Error: Failed to detect foreground app", f"Details: {str(e)}", is_error=True)
        return None

def get_launcher_activity(package):
    try:
        try:
            output = subprocess.check_output(
                ['adb', 'shell', 'dumpsys', 'package', package, '|', 'grep', '-A', '1', 'android.intent.category.LAUNCHER', '|', 'grep', 'Activity'], 
                stderr=subprocess.STDOUT, shell=True).decode('utf-8').strip()
            
            if output and '/' in output:
                activity_path = output.split()[-1]
                if package in activity_path and '/' in activity_path:
                    return activity_path.split('/')[-1]
        except:
            pass
            
        try:
            output = subprocess.check_output(
                f"adb shell 'cmd package resolve-activity --brief {package} | tail -n 1'", 
                stderr=subprocess.STDOUT, shell=True).decode('utf-8').strip()
            
            if output and '/' in output:
                return output.split('/')[-1]
        except:
            pass
            
        print(f"{COLOR_YELLOW}Could not determine main activity, will use monkey launcher instead{COLOR_RESET}")
        return None
    except Exception as e:
        print(f"{COLOR_YELLOW}Error finding launcher activity: {str(e)}, will use monkey launcher instead{COLOR_RESET}")
        return None

def launch_android_app(package):
    try:
        activity = get_launcher_activity(package)
        launch_success = False
        
        if activity:
            try:
                subprocess.check_call(['adb', 'shell', f'am start -n {package}/{activity}'])
                print(f"{COLOR_GREEN}Launched app with activity: {activity}{COLOR_RESET}")
                launch_success = True
            except subprocess.CalledProcessError:
                print(f"{COLOR_YELLOW}Failed to launch with activity name, trying alternative methods...{COLOR_RESET}")
        
        if not launch_success:
            try:
                subprocess.check_call(['adb', 'shell', f'monkey -p {package} -c android.intent.category.LAUNCHER 1'])
                launch_success = True
            except subprocess.CalledProcessError:
                print(f"{COLOR_YELLOW}Monkey launcher failed, trying generic intent...{COLOR_RESET}")
        
        if not launch_success:
            try:
                subprocess.check_call(['adb', 'shell', f'am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p {package}'])
                launch_success = True
            except subprocess.CalledProcessError:
                print(f"{COLOR_YELLOW}Generic intent failed, trying MainActivity as last resort...{COLOR_RESET}")
        
        if not launch_success:
            subprocess.check_call(['adb', 'shell', f'am start -n {package}/.MainActivity'])
        
        time.sleep(1)
        print_formatted_message("Application launched successfully", f"Package: {package}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        print_formatted_message("Error: Failed to launch application", f"Details: {error_msg}", is_error=True)
        print(f"{COLOR_YELLOW}Try launching the app manually before running this script.{COLOR_RESET}")
        raise

def switch_to_task_switcher_android(delay):
    try:
        subprocess.check_call(['adb', 'shell', 'input keyevent KEYCODE_APP_SWITCH'])
        print_formatted_message("Navigating to task switcher for blur test", f"Waiting for {delay} seconds")
        for i in range(delay - 1, -1, -1):
            print(f"{COLOR_YELLOW}Waiting: {i} seconds{COLOR_RESET}", end="\r")
            time.sleep(1)
        print(" " * 30, end="\r")
        print_formatted_message("Task switcher navigation complete", "Ready for capture")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        print_formatted_message("Error: Failed to navigate to task switcher", f"Details: {error_msg}", is_error=True)
        raise



def take_android_screenshot(output_path, task_switcher=False, package=None, delay=1):
    if package:
        launch_android_app(package)
        print_formatted_message("Launched specified app", f"Package: {package}")
        
        if task_switcher:
            switch_to_task_switcher_android(delay)
    elif task_switcher:
        package = get_foreground_app_android()
        if not package:
            print_formatted_message("Error: No foreground app detected", "Launch an app or specify --package", is_error=True)
            return
        print_formatted_message("Detected foreground app", f"Package: {package}")
        switch_to_task_switcher_android(delay)
    
    filename = f"screenshot_{int(time.time())}.png"
    output_file = os.path.join(output_path, filename)
    try:
        subprocess.check_call(['adb', 'shell', f'screencap /sdcard/{filename}'])
        subprocess.check_call(['adb', 'pull', f'/sdcard/{filename}', output_file])
        subprocess.check_call(['adb', 'shell', f'rm /sdcard/{filename}'])
        message = "Screenshot captured successfully!"
        details = f"Saved as: {output_file}"
        if task_switcher:
            message += " (App switcher test)"
            details += " | Check app preview for blur effect"
        print_formatted_message(message, details)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        print_formatted_message("Error: Failed to capture screenshot", f"Details: {error_msg}", is_error=True)
        print(f"{COLOR_YELLOW}Ensure ADB is installed and the device is connected (run 'adb devices').{COLOR_RESET}")
    except Exception as e:
        print_formatted_message("Error: Failed to capture screenshot", f"Details: {str(e)}", is_error=True)

def record_android_screen(duration, output_path, task_switcher=False, package=None, delay=1):
    if package:
        launch_android_app(package)
        print_formatted_message("Launched specified app", f"Package: {package}")
        
        if task_switcher:
            switch_to_task_switcher_android(delay)
    elif task_switcher:
        package = get_foreground_app_android()
        if not package:
            print_formatted_message("Error: No foreground app detected", "Launch an app or specify --package", is_error=True)
            return
        print_formatted_message("Detected foreground app", f"Package: {package}")
        switch_to_task_switcher_android(delay)
    
    filename = f"screenrecord_{int(time.time())}.mp4"
    output_file = os.path.join(output_path, filename)
    try:
        print_formatted_message(f"Screen recording started for {duration} seconds", "Platform: Android")
        subprocess.check_call(['adb', 'shell', f'screenrecord --time-limit {duration} /sdcard/{filename}'])
        for i in range(duration - 1, -1, -1):
            print(f"{COLOR_YELLOW}Remaining: {i} seconds{COLOR_RESET}", end="\r")
            time.sleep(1)
        print(" " * 30, end="\r")
        subprocess.check_call(['adb', 'pull', f'/sdcard/{filename}', output_file])
        subprocess.check_call(['adb', 'shell', f'rm /sdcard/{filename}'])
        message = "Screen recording completed!"
        details = f"Saved as: {output_file}"
        if task_switcher:
            message += " (App switcher test)"
            details += " | Check app preview for blur effect"
        print_formatted_message(message, details)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        print_formatted_message("Error: Failed to record screen", f"Details: {error_msg}", is_error=True)
        print(f"{COLOR_YELLOW}Ensure ADB is installed and the device is connected (run 'adb devices').{COLOR_RESET}")
    except Exception as e:
        print_formatted_message("Error: Failed to record screen", f"Details: {str(e)}", is_error=True)



def print_help_examples():
    print(f"\n{COLOR_GREEN}Usage Examples:{COLOR_RESET}")
    print(f"{COLOR_YELLOW}  Basic screenshot:{COLOR_RESET}")
    print(f"  snapdroid --screenshot")
    print(f"  snapdroid -ss")
    print(f"\n{COLOR_YELLOW}  Screenshot with specific app:{COLOR_RESET}")
    print(f"  snapdroid -ss --package com.example.app")
    print(f"\n{COLOR_YELLOW}  Screenshot in app switcher (blur test):{COLOR_RESET}")
    print(f"  snapdroid -ss --background")
    print(f"\n{COLOR_YELLOW}  Record screen for 10 seconds:{COLOR_RESET}")
    print(f"  snapdroid --screenrecord 10")
    print(f"  snapdroid -sr 10")
    print(f"\n{COLOR_YELLOW}  Record specific app for 5 seconds:{COLOR_RESET}")
    print(f"  snapdroid -sr 5 --package com.example.app")
    print(f"\n{COLOR_YELLOW}  Save output to specific directory:{COLOR_RESET}")
    print(f"  snapdroid -ss --out /path/to/save")
    print("")

def main():
    parser = argparse.ArgumentParser(description='SnapDroid - Android Screenshot and Screen Recording Tool')
    parser.add_argument('--screenshot', '-ss', action='store_true', help='Capture a screenshot')
    parser.add_argument('--screenrecord', '-sr', type=int, help='Record the screen for specified seconds')
    parser.add_argument('--out', default='.', help='Output directory for saved files (default: current directory)')
    parser.add_argument('--background', action='store_true', help='Navigate to app switcher before capturing (pentest app preview blur test)')
    parser.add_argument('--package', help='Specify the target app package name (optional override for foreground app detection)')
    parser.add_argument('--delay', type=int, default=1, help='Delay in seconds after navigating to app switcher (default: 1)')
    parser.add_argument('--examples', action='store_true', help='Show usage examples')
    parser.add_argument('--version', action='store_true', help='Show version information')
    args = parser.parse_args()
    
    print(ASCII_ART)
    
    if args.version:
        # Hardcoded version to match package version
        __version__ = '1.0.3'
        print(f"{COLOR_GREEN}SnapDroid version: {__version__}{COLOR_RESET}")
        return
    
    if args.examples:
        print_help_examples()
        return

    # Check if ADB is installed
    try:
        try:
            subprocess.check_output(['adb', 'version'], stderr=subprocess.STDOUT)
        except FileNotFoundError:
            print_formatted_message("Error: ADB not found", "Android Debug Bridge is required", is_error=True)
            print(f"{COLOR_YELLOW}Please install ADB:{COLOR_RESET}")
            print(f"{COLOR_YELLOW}- macOS: brew install android-platform-tools{COLOR_RESET}")
            print(f"{COLOR_YELLOW}- Linux: apt install adb{COLOR_RESET}")
            print(f"{COLOR_YELLOW}- Windows: Download from developer.android.com{COLOR_RESET}")
            return
            
        devices_output = subprocess.check_output(['adb', 'devices'], stderr=subprocess.STDOUT).decode('utf-8')
        if 'device' not in devices_output or devices_output.count('\n') <= 1:
            print_formatted_message("Error: No Android devices detected", "No devices found or device not authorized", is_error=True)
            print(f"{COLOR_YELLOW}Please ensure:{COLOR_RESET}")
            print(f"{COLOR_YELLOW}1. Android device is connected via USB{COLOR_RESET}")
            print(f"{COLOR_YELLOW}2. USB debugging is enabled on the device{COLOR_RESET}")
            print(f"{COLOR_YELLOW}3. Device is authorized (check for authorization dialog on device){COLOR_RESET}")
            print(f"{COLOR_YELLOW}4. Try running 'adb devices' to see connected devices{COLOR_RESET}")
            return
            
        try:
            subprocess.check_output(['adb', 'get-state'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print_formatted_message("Error: Device not responding", "Connected device is not responding to ADB commands", is_error=True)
            print(f"{COLOR_YELLOW}Try these steps:{COLOR_RESET}")
            print(f"{COLOR_YELLOW}1. Restart ADB with 'adb kill-server && adb start-server'{COLOR_RESET}")
            print(f"{COLOR_YELLOW}2. Reconnect your device{COLOR_RESET}")
            print(f"{COLOR_YELLOW}3. Check for permission prompts on your device{COLOR_RESET}")
            return
            
    except Exception as e:
        print_formatted_message("Error: ADB connection issue", f"Details: {str(e)}", is_error=True)
        return

    if args.delay <= 0:
        print_formatted_message("Error: Invalid delay", "Delay must be a positive integer", is_error=True)
        return

    if not args.out or not re.match(r'^[a-zA-Z0-9_\-./]+$', args.out):
        print_formatted_message("Error: Invalid output directory", "Directory path contains invalid characters", is_error=True)
        return
        
    output_dir = os.path.abspath(args.out)
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"{COLOR_YELLOW}Created output directory: {output_dir}{COLOR_RESET}")
        except Exception as e:
            print_formatted_message("Error: Failed to create output directory", f"Details: {str(e)}", is_error=True)
            return
    
    if not os.access(output_dir, os.W_OK):
        print_formatted_message("Error: Output directory not writable", f"Cannot write to: {output_dir}", is_error=True)
        return

    if not args.screenshot and not args.screenrecord:
        print_formatted_message("Error: No action specified", "Use --screenshot or --screenrecord <duration>", is_error=True)
        print_help_examples()
        return
        
    if args.screenshot and args.screenrecord:
        print_formatted_message("Error: Invalid action selection", "Cannot specify both --screenshot and --screenrecord", is_error=True)
        return

    if args.screenshot:
        take_android_screenshot(output_dir, args.background, args.package, args.delay)
    elif args.screenrecord:
        if args.screenrecord <= 0:
            print_formatted_message("Error: Invalid duration", "Screenrecord duration must be positive", is_error=True)
            return
        record_android_screen(args.screenrecord, output_dir, args.background, args.package, args.delay)

if __name__ == '__main__':
    main()