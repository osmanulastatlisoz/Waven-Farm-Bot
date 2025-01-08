import pydirectinput
import time
import subprocess
import keyboard

def main():
    # Başlamadan önce 2 saniye bekleme
    time.sleep(2)
    
    # ESC simülasyonu
    for _ in range(8):
        pydirectinput.press('esc')
        time.sleep(0.5)

    # Kullanıcıdan girdi alma
    print("Döngüyü durdurmak için '+' tuşuna basın, devam etmek için başka bir tuşa basın:")
    
    # 10 saniye boyunca '+' tuşuna basılıp basılmadığını kontrol et
    start_time = time.time()
    while time.time() - start_time < 1:
        if keyboard.is_pressed('+'):
            print("Program durduruluyor...")
            return

    print("5 saniye geçti, otomatik olarak devam ediyor...")

    # give-up.py dosyasını çalıştır
    subprocess.run(['python', 'give-up.py'])

if __name__ == "__main__":
    main()
