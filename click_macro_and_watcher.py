import subprocess
import os
import time

# Mevcut çalışma dizinini belirleyin
current_directory = os.path.dirname(os.path.abspath(__file__))

# click_macro.ahk dosyasının tam yolunu belirleyin
ahk_file = os.path.join(current_directory, "click_macro.ahk")

# click_macro.ahk dosyasını çalıştır
subprocess.run(["start", ahk_file], shell=True)

# 1 saniye bekle
time.sleep(1)

# Watcher.py dosyasının tam yolunu belirleyin
watcher_file = os.path.join(current_directory, "Watcher.py")

# Watcher.py dosyasını çalıştır
subprocess.run(["python", watcher_file])
