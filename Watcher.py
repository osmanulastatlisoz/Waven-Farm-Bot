import subprocess
import threading
import time
import os
import signal
import psutil

# Timeout süresi (saniye olarak)
TIMEOUT = 30  # 30 saniye (test amaçlı)
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB (örnek boyut)

def run_script(script_name):
    """Belirtilen scripti çalıştırır."""
    print(f"Running: {script_name}")
    with open('log.txt', 'a') as log_file:
        log_file.write(f"Running: {script_name}\n")
    subprocess.run(['python', script_name])

def kill_all_scripts(exclude_current_pid):
    """Diğer çalışan tüm Python scriptlerini kapatır."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python.exe' and proc.info['pid'] != exclude_current_pid:
            os.kill(proc.info['pid'], signal.SIGTERM)

def clear_log():
    """Log dosyasını temizler."""
    with open('log.txt', 'w') as log_file:
        log_file.write("Log file cleared.\n")

def timeout_handler():
    """Zaman aşımı gerçekleştiğinde cikis.py'yi çalıştırır."""
    print("Timeout occurred. Running cikis.py...")
    with open('log.txt', 'a') as log_file:
        log_file.write("Timeout occurred. Running cikis.py...\n")

    # Diğer scriptleri öldür
    kill_all_scripts(os.getpid())

    # Log dosyasını temizle
    clear_log()

    # cikis.py'yi çalıştır
    subprocess.run(['python', 'cikis.py'])

    # Timer'ı resetleyerek tekrar çalıştır
    global timer
    timer = threading.Timer(TIMEOUT, timeout_handler)
    timer.start()
    with open('log.txt', 'a') as log_file:
        log_file.write("Timer reset after running cikis.py.\n")

def reset_timer():
    """Zamanlayıcıyı sıfırlar."""
    global timer
    if timer:
        timer.cancel()
    timer = threading.Timer(TIMEOUT, timeout_handler)
    timer.start()
    with open('log.txt', 'a') as log_file:
        log_file.write("Timer reset.\n")

def check_log_size():
    """Log dosyasının boyutunu kontrol eder ve belirli bir boyutu aşıyorsa temizler."""
    if os.path.exists('log.txt') and os.path.getsize('log.txt') > MAX_LOG_SIZE:
        with open('log.txt', 'w') as log_file:
            log_file.write("Log file cleared due to size limit.\n")

def main():
    """Ana izleme fonksiyonu."""
    global timer
    # İlk script
    initial_script = 'adamin-bacagina-tiklama.py'
    
    # İlk script'i çalıştır
    run_script(initial_script)
    
    # İlk zamanlayıcıyı başlat
    timer = threading.Timer(TIMEOUT, timeout_handler)
    timer.start()
    
    try:
        while True:
            check_log_size()  # Log dosyasının boyutunu kontrol et
            
            # status.txt dosyasını kontrol et
            with open('status.txt', 'r') as file:
                status = file.read().strip()
                if status == 'adamin-bacagina-tiklama.py calistirildi.':
                    print("Status.txt read and script started.")
                    with open('log.txt', 'a') as log_file:
                        log_file.write("Status.txt read and script started.\n")
                    reset_timer()
                    run_script(initial_script)
                    # status.txt'yi temizle
                    open('status.txt', 'w').close()
                else:
                    with open('log.txt', 'a') as log_file:
                        log_file.write(f"Unexpected content in status.txt: {status}\n")
            
            # Zamanlayıcıyı kontrol etmek için bekle
            while timer.is_alive():
                time.sleep(1)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        with open('log.txt', 'a') as log_file:
            log_file.write(f"An error occurred: {e}\n")
        if timer:
            timer.cancel()

if __name__ == "__main__":
    main()
