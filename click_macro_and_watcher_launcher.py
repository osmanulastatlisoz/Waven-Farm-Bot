import subprocess
import os
import signal
import psutil
import atexit
import time

# Sabit yolları belirleyin
click_macro_ahk_path = "C:\\Users\\ulast\\OneDrive\\Masaüstü\\bot-yapimi-waven\\click_macro.ahk"
watcher_py_path = "C:\\Users\\ulast\\OneDrive\\Masaüstü\\bot-yapimi-waven\\Watcher.py"

def kill_all_scripts(exclude_current_pid):
    """Diğer çalışan tüm Python scriptlerini kapatır."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python.exe' and proc.info['pid'] != exclude_current_pid:
            os.kill(proc.info['pid'], signal.SIGTERM)

def cleanup():
    """Çıkışta tüm Python scriptlerini kapatır."""
    print("Cleaning up...")
    kill_all_scripts(os.getpid())

def main():
    # click_macro.ahk dosyasını çalıştır
    subprocess.run(["start", click_macro_ahk_path], shell=True)
    time.sleep(1)  # 1 saniye bekle

    # Watcher.py dosyasını çalıştır
    subprocess.run(["python", watcher_py_path])

if __name__ == "__main__":
    atexit.register(cleanup)
    main()
