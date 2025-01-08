import pyautogui
import cv2
import numpy as np
import time
import pydirectinput
import subprocess  # Play dosyasını çalıştırmak için

def search_and_click(template_path, region=None):
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    print("Starting bot... waiting for 0.5 seconds to switch to the game window.")
    # 0.5 saniye bekle
    time.sleep(0.5)
    print("0.5 seconds passed. Starting to search for the image.")

    for i in range(10):  # 10 kere tarama yap
        start_time = time.time()
        print(f"Searching... attempt {i+1}/10")

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
            print(f"Found image at coordinates: ({center_x}, {center_y})")
            print("Moving to the coordinates and waiting for 0.2 seconds...")
            pydirectinput.moveTo(center_x, center_y)
            time.sleep(0.2)
            print("Pressing F7 to hold down left click for 0.2 seconds...")
            pydirectinput.keyDown('f7')
            time.sleep(0.2)  # 0.2 saniye bekle
            pydirectinput.keyUp('f7')
            print(f"Clicked at coordinates: ({center_x}, {center_y})")

            # Play dosyasını çalıştır
            subprocess.run(['python', 'play.py'])
            return  # Bulduğunda tıklayıp çıkmak için

        # Her tarama arasında 0.18 saniye bekle
        time_elapsed = time.time() - start_time
        time.sleep(max(0, 0.18 - time_elapsed))

    print("Image not found in 10 attempts.")
    # Eğer resim bulunamazsa cikis.py dosyasını çalıştır
    subprocess.run(['python', 'cikis.py'])

# Örnek kullanım
template_path = 'kilic.png'
search_and_click(template_path)
