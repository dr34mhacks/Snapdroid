# SnapDroid

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android-brightgreen" alt="Platform: Android">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License: MIT">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange" alt="Version: 1.0.0">
</p>

A powerful command-line tool for capturing Android screenshots and screen recordings directly to your local machine without third-party apps or manual transfers.

```
   _____                   ____             _     __   
  / ___/____  ____ _____  / __ \_________  (_)___/ /   Android
  \__ \/ __ \/ __ `/ __ \/ / / / ___/ __ \/ / __  /    Screenshot
 ___/ / / / / /_/ / /_/ / /_/ / /  / /_/ / / /_/ /     & Recording
/____/_/ /_/\__,_/ .___/_____/_/   \____/_/\__,_/      
                /_/                                     
```

## 🚀 Features

- **Instant Screenshots**: Capture Android device screens with a single command
- **Screen Recording**: Record device activity for specified durations
- **App Targeting**: Launch and capture specific apps by package name
- **Background Blur Testing**: Special mode for security testing of app preview blurring
- **No Root Required**: Works with standard ADB debugging connection
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
- **Background Blur Testing**: Test if sensitive apps properly blur content in the app switcher view
- **Evidence Collection**: Capture proof of security findings
- **Automation Friendly**: Integrate into testing scripts
- **Works on Emulators**: Test on platforms where manual screenshots are difficult (like Corellium)

## 📋 Requirements

- Python 3.6+
- Android Debug Bridge (ADB) installed and in your PATH
- USB debugging enabled on your Android device
- Connected Android device or emulator

## 🔧 Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install snapdroid
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

**Take a screenshot:**
```bash
snapdroid -ss
```

**Record the screen for 10 seconds:**
```bash
snapdroid -sr 10
```

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

**Record a specific app for 5 seconds:**
```bash
snapdroid -sr 5 --package com.example.banking.app
```

**Show all examples:**
```bash
snapdroid --examples
```

**Show version information:**
```bash
snapdroid --version
```

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

Created by [@yourusername](https://github.com/yourusername) - feel free to contact me!