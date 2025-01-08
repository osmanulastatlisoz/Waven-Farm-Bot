# memory_watcher.py

import time
import os
import psutil
import subprocess
import signal

MAX_RAM_USAGE_MB = 3072  # 3 GB
MAX_GPU_USAGE_PERCENT = 35  # %35
MAX_CPU_USAGE_PERCENT = 35  # %35
CHECK_INTERVAL = 10  # Kontrol aralığı (saniye)
WATCHER_SCRIPT = 'watcher.py'  # İzlenecek script
LOG_FILE = 'memory_watcher_log.txt'  # memory_watcher.py için log dosyası

def write_log(message):
    """Log dosyasına mesaj yazar."""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def kill_all_python_processes(exclude_pid=None):
    """Bütün Python süreçlerini kapatır, exclude_pid belirtilen süreç hariç."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python.exe' and (exclude_pid is None or proc.info['pid'] != exclude_pid):
            write_log(f"Killing process with PID: {proc.info['pid']}")
            os.kill(proc.info['pid'], signal.SIGTERM)

def start_watcher():
    """Watcher scriptini başlatır."""
    write_log(f"Starting {WATCHER_SCRIPT}...")
    subprocess.Popen(['python', WATCHER_SCRIPT])

def check_gpu_usage():
    """GPU kullanımını kontrol eder."""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        gpu_usage = int(result.stdout.strip())
        return gpu_usage
    except Exception as e:
        write_log(f"Error checking GPU usage: {e}")
        return 0

def main():
    """Ana izleme fonksiyonu."""
    # İlk başta watcher.py'yi başlat
    start_watcher()
    
    while True:
        # Toplam bellek kullanımını kontrol et
        total_memory = psutil.virtual_memory().used / (1024 * 1024)  # MB cinsinden
        write_log(f"Total memory usage: {total_memory:.2f} MB")

        # GPU kullanımını kontrol et
        gpu_usage = check_gpu_usage()
        write_log(f"GPU usage: {gpu_usage}%")

        # CPU kullanımını kontrol et
        cpu_usage = psutil.cpu_percent(interval=1)
        write_log(f"CPU usage: {cpu_usage}%")

        if total_memory > MAX_RAM_USAGE_MB or gpu_usage > MAX_GPU_USAGE_PERCENT or cpu_usage > MAX_CPU_USAGE_PERCENT:
            write_log("Resource usage exceeded limits. Restarting processes...")
            
            # Tüm Python süreçlerini kapat
            kill_all_python_processes()
            time.sleep(2)  # Kapanmalarının bitmesi için bekle

            # watcher.py'yi yeniden başlat
            start_watcher()

        # Bellek ve işlemci kullanımını belirli aralıklarla kontrol et
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
