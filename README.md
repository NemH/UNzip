# 🚀 UNzip

A lightweight, background-running archive extraction utility for Windows that lives in the system tray and displays extraction progress in real-time.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

---

## ✨ Features

- **System Tray Integration:** Runs silently in the background without opening distracting console windows.
- **Live Progress Indicator:** Dynamically renders the current extraction percentage directly onto the tray icon image in real-time.
- **Clean & Autonomous:** Automatically creates a destination folder next to the original archive and extracts the contents without popping up unwanted File Explorer windows.
- **Native Support:** Handles `.zip`, `.tar`, `.gz`, and `.bz2` formats efficiently.
- **Crisp High-DPI Icon:** Supports multi-resolution `.ico` assets for clean visual presentation across all Windows scaling modes.

---

## 📦 Installation & Setup

1. Download the latest `UNzip.exe` release from the [Releases](../../releases) tab.
2. Move `UNzip.exe` to a permanent folder on your PC (e.g., `C:\Program Files\UNzip\`) or any else.
3. Right-click any `.zip` or `.tar` file in Windows.
4. Select **Open with** $\rightarrow$ **Choose another app**.
5. Scroll down, click **Choose an app on your PC**, browse to `UNzip.exe`, and check **Always use this app**.

---

## 🛠️ Building from Source

### Prerequisites

Ensure you have Python 3.10+ installed along with the required dependencies:

```bash
pip install pystray Pillow pyinstaller
```

### Build Instructions

1. *(Optional)* Convert your `icon.png` into a multi-resolution `icon.ico`:
   ```bash
   python -c "from PIL import Image; img = Image.open('icon.png').convert('RGBA'); img.save('icon.ico', format='ICO', sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])"
   ```

2. Compile the project using PyInstaller:
   ```bash
   pyinstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." --name "UNzip" UNzip.py
   ```

3. Your standalone executable will be ready in the `dist/UNzip.exe` directory.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
