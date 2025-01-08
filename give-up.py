import pyautogui
import cv2
import numpy as np
import time
import pydirectinput
import subprocess

def search_and_click(template_path, region=None):
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    for i in range(3):  # 5 kere tarama yap
        start_time = time.time()
        print(f"Searching for image {template_path}... attempt {i+1}/5")

        # Belirli bir bölgenin ekran görüntüsünü al
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Görselin ekran görüntüsünde aranması
        result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)

        for point in zip(*locations[::-1]):
            center_x = point[0] + template_w // 2
            center_y = point[1] + template_h // 2
            if region:
                # Bölgeye göre koordinatları ayarla
                center_x += region[0]
                center_y += region[1]
            print(f"Found image {template_path} at coordinates: ({center_x}, {center_y})")
            
            # Eğer `give-up.png` ise X ekseninde +20 kaydırma yap
            if template_path == 'give-up.png':
                center_x += 20
            
            print("Moving to the coordinates and waiting for 0.5 seconds...")
            pydirectinput.moveTo(center_x, center_y)
            time.sleep(0.5)  # 0.5 saniye bekle
            print("Pressing F7 to hold down left click for 0.2 seconds...")
            pydirectinput.keyDown('f7')
            time.sleep(0.2)  # 0.2 saniye bekle
            pydirectinput.keyUp('f7')
            print(f"Clicked at coordinates: ({center_x}, {center_y})")
            return True  # Bulduğunda tıklayıp çıkmak için

        # Her tarama arasında 0.1 saniye bekle
        time_elapsed = time.time() - start_time
        time.sleep(max(0, 0.1 - time_elapsed))

    print(f"Image {template_path} not found in 5 attempts.")
    return False

# Başlangıçta 0.5 saniye bekleme
time.sleep(0.5)

# uc-cizgi.png dosyasını arama
found1 = search_and_click('uc-cizgi.png')

# Eğer uc-cizgi.png bulunamazsa adamin-bacagina-tiklama.py dosyasını çalıştır
if not found1:
    subprocess.run(['python', 'adamin-bacagina-tiklama.py'])
else:
    # Arama ve tıklama işlemleri
    found2 = search_and_click('give-up.png')
    found3 = search_and_click('yes.png')

    # Eğer yes.png bulunursa adamin-bacagina-tiklama.py dosyasını çalıştırmadan önce 3 saniye bekle
    if found3:
        time.sleep(3)
        subprocess.run(['python', 'adamin-bacagina-tiklama.py'])
    else:
        # Eğer yes.png bulunamazsa adamin-bacagina-tiklama.py dosyasını çalıştır
        subprocess.run(['python', 'adamin-bacagina-tiklama.py'])
