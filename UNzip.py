import sys
import os
import zipfile
import tarfile
import threading
import time
import tkinter as tk
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageFont

# Try import RAR
try:
    import rarfile
    HAS_RAR = True
except ImportError:
    HAS_RAR = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_base_icon():
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        try:
            return Image.open(icon_path).convert("RGBA").resize((64, 64))
        except:
            pass
    return Image.new('RGBA', (64, 64), color=(15, 76, 129, 255))

def create_progress_icon(base_image, percent):
    img = base_image.copy()
    draw = ImageDraw.Draw(img)
    draw.rectangle([2, 36, 62, 62], fill=(0, 0, 0, 180))
    
    try:
        font = ImageFont.truetype("arial.bold.ttf", 22)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 22)
        except:
            font = ImageFont.load_default()

    text = f"{percent}%"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (64 - w) / 2
    y = 36 + (26 - h) / 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    return img

class TrayUnarchiver:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.icon = None
        self.base_image = get_base_icon()
        
        self.root = tk.Tk()
        self.root.withdraw()
        
        menu = (item('Exit', self.exit_app),)
        initial_icon = create_progress_icon(self.base_image, 0)
        self.icon = pystray.Icon("unarchiver", initial_icon, "Unpack: 0%", menu)
        
        threading.Thread(target=self.icon.run, daemon=True).start()
        threading.Thread(target=self.extract_archive, daemon=True).start()
        
        self.root.mainloop()

    def update_progress(self, percent, archive_name=""):
        if self.icon:
            self.icon.icon = create_progress_icon(self.base_image, percent)
            self.icon.title = f"Unpack: {percent}% ({archive_name})"

    def extract_archive(self):
        try:
            if not os.path.exists(self.archive_path):
                if self.icon:
                    self.icon.title = "File don`t found"
                time.sleep(2)
                self.exit_app()
                return

            base_dir = os.path.dirname(self.archive_path)
            archive_name = os.path.basename(self.archive_path)
            folder_name, _ = os.path.splitext(archive_name)
            extract_to = os.path.join(base_dir, folder_name)

            os.makedirs(extract_to, exist_ok=True)
            self.update_progress(0, archive_name)

            # 1. Support ZIP
            if zipfile.is_zipfile(self.archive_path):
                with zipfile.ZipFile(self.archive_path, 'r') as zf:
                    members = zf.infolist()
                    total_files = len(members)
                    for i, member in enumerate(members, 1):
                        zf.extract(member, extract_to)
                        if total_files > 0:
                            percent = int((i / total_files) * 100)
                            self.update_progress(percent, archive_name)

            # 2. Support TAR / GZ / BZ2
            elif tarfile.is_tarfile(self.archive_path):
                with tarfile.open(self.archive_path, 'r:*') as tf:
                    members = tf.getmembers()
                    total_files = len(members)
                    for i, member in enumerate(members, 1):
                        tf.extract(member, extract_to)
                        if total_files > 0:
                            percent = int((i / total_files) * 100)
                            self.update_progress(percent, archive_name)

            # 3. Support RAR
            elif HAS_RAR:
                try:
                    if rarfile.is_rarfile(self.archive_path):
                        with rarfile.RarFile(self.archive_path, 'r') as rf:
                            members = rf.infolist()
                            total_files = len(members)
                            for i, member in enumerate(members, 1):
                                rf.extract(member, extract_to )
                                if total_files > 0:
                                    percent = int((i / total_files) * 100)
                                    self.update_progress(percent, archive_name)
                    else:
                        raise ValueError("Don`t support file format")
                except rarfile.UnrarNotFound:
                    if self.icon:
                        self.icon.title = "Error: missing unrar.exe"
                    time.sleep(4)
                    self.exit_app()
                    return
            else:
                if self.icon:
                    self.icon.title = "Don`t support format"
                time.sleep(3)
                self.exit_app()
                return

            if self.icon:
                self.icon.icon = self.base_image
                self.icon.title = "Unpack Successful!"
            
        except Exception as e:
            if self.icon:
                self.icon.title = f"Error: {str(e)[:30]}"
            time.sleep(4)

        time.sleep(2)
        self.exit_app()

    def exit_app(self, icon=None, item=None):
        if self.icon:
            self.icon.stop()
        self.root.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TrayUnarchiver(sys.argv[1])
    else:
        sys.exit(0)