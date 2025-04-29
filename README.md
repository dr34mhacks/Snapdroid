<div align=center>
<img src="https://github.com/user-attachments/assets/cee729da-42ca-4169-bf04-4757cb79bdc4">

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android-brightgreen" alt="Platform: Android">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT">
  <img src="https://img.shields.io/pypi/v/snapdroid.svg">
  <img src="https://img.shields.io/badge/screen-capture-orange" alt="screen record android">
</p>

- - - 


A powerful command-line tool for capturing Android screenshots and screen recordings directly to your local machine without third-party apps or manual transfers. 

## 🚀 Features

- **Instant Screenshots**: Capture Android device screens with a single command
- **Screen Recording**: Record device activity for specified durations
- **App Targeting**: Launch and capture specific apps by package name
- **Background Blur Testing**: Special mode for security testing of app preview blurring
- **No Third-Party Apps**: Uses built-in Android tools, no app installation needed
- **Local Storage**: Files saved directly to your computer, no cloud uploads
- **Emulator Support**: Works with Android emulators including Corellium devices

## 🔍 Why SnapDroid?

### For Developers
- **Streamlined Workflow**: Capture screenshots and recordings without interrupting your development flow
- **Documentation**: Easily create visual documentation for your apps
- **Bug Reporting**: Capture and share visual evidence of issues
- **Demo Creation**: Record app demos directly from your development environment

### For Security Testers
- **Automation Friendly**: Integrate into testing scripts easily 
- **Background Blur Testing**: Test if sensitive apps properly blur content in the app switcher view
- **POC Collection**: Capture proof of security findings actual pain point of mine for creating this tool
- **Works on Emulators**: Test on platforms where manual screenshots are difficult (like `Corellium`)

## 📋 Requirements

- Python 3.6+
- Android Debug Bridge (ADB) installed and set to your PATH
- USB debugging enabled on your Android device
- Connected Android device or emulator

## 🔧 Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip3 install snapdroid
```

### Option 2: Install from GitHub

1. Clone this repository:
   ```bash
   git clone https://github.com/dr34mhacks/snapdroid.git
   cd snapdroid
   ```

2. Install the package:
   ```bash
   # Method A: Using the installation script
   ./install.sh
   
   # Method B: Using pip directly
   pip install -e .
   ```

### Prerequisites

Make sure ADB is installed:
- **macOS**: `brew install android-platform-tools`
- **Linux**: `apt install adb`
- **Windows**: Download from [developer.android.com](https://developer.android.com/studio/releases/platform-tools)

Connect your Android device and enable USB debugging

## 📱 Usage

### Basic Commands

```
SnapDroid - Android Screenshot and Screen Recording Tool

options:
  -h, --help            show this help message and exit
  --screenshot, -ss     Capture a screenshot
  --screenrecord, -sr SCREENRECORD
                        Record the screen for specified seconds
  --out OUT             Output directory for saved files (default: current directory)
  --background          Navigate to app switcher before capturing (pentest app preview blur test)
  --package PACKAGE     Specify the target app package name (optional override for foreground app detection)
  --delay DELAY         Delay in seconds after navigating to app switcher (default: 1)
  --examples            Show usage examples
  --version             Show version information
```

**Take a screenshot:**
```bash
snapdroid -ss
```
<img width="1467" alt="snapdroid" src="https://github.com/user-attachments/assets/f80ec9cb-3872-463c-9df6-b3b372e8de05" />


**Record the screen for 10 seconds:**
```bash
snapdroid -sr 10
```

<img width="1469" alt="snapdroid" src="https://github.com/user-attachments/assets/c610e46e-2a28-4c81-8a89-36dbc3a344f9" />


**Save to a specific directory:**
```bash
snapdroid -ss --out ~/Screenshots
```

### Advanced Features

**Capture a specific app by package name:**
```bash
snapdroid -ss --package com.example.app
```

**Test background blur in app switcher:**
```bash
snapdroid -ss --background
```

<img width="1476" alt="snapdroid" src="https://github.com/user-attachments/assets/ec834227-1772-4052-8712-35b937f18ee2" />


**Record a specific app for 5 seconds:**
```bash
snapdroid -sr 5 --package com.example.banking.app
```

**Show all examples:**
```bash
snapdroid --examples
```
<img width="1126" alt="snapdroid" src="https://github.com/user-attachments/assets/1d106f93-755c-44ec-9b9a-e17cc5952a05" />

**Show version information:**
```bash
snapdroid --version
```

## Watch SnapDroid in Action:

SnapDroid Video Demonstration:


<p align="center">
  <a href="https://www.youtube.com/watch?v=1QIj4CdrTPM">
    <img width="1126" src="https://img.youtube.com/vi/1QIj4CdrTPM/1.jpg" alt="SnapDroid Android Capture">
  </a>
</p>


## 🔒 Security Testing Use Cases

### Background Blur Testing

Many apps containing sensitive information should implement proper blurring when shown in the app switcher (recent apps) view. SnapDroid makes it easy to test this security feature:

1. Launch the target app:
   ```bash
   snapdroid -ss --package com.example.banking.app --background
   ```

2. SnapDroid will:
   - Launch the specified app
   - Navigate to the app switcher
   - Capture a screenshot
   - Save it locally for analysis

3. Examine the screenshot to verify proper content blurring

This is particularly useful on emulators like older Corellium devices where taking screenshots of the app switcher can be challenging through normal means.

## 🛠️ Troubleshooting

**No device detected:**
- Ensure USB debugging is enabled on your device
- Check connection with `adb devices`
- Try restarting ADB with `adb kill-server && adb start-server`

**Permission denied errors:**
- Make sure your device has authorized the ADB connection
- Check for permission prompts on your device

**App won't launch:**
- Verify the package name is correct
- Try launching the app manually first

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📬 Contact

Created by [@dr34mhacks](https://github.com/dr34mhacks) - feel free to contact me!
