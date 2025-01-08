import pyautogui
import cv2
import numpy as np
import time
import pydirectinput
import subprocess

def search_image(template_path, region=None):
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    for i in range(3):  # 10 kere tarama yap
        start_time = time.time()
        print(f"Searching for image... attempt {i+1}/10")

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
            return (center_x, center_y)  # Görseli bulduğunda koordinatları döndür

        # Her tarama arasında 0.1 saniye bekle
        time_elapsed = time.time() - start_time
        time.sleep(max(0, 0.1 - time_elapsed))

    print("Image not found in 10 attempts.")
    return None

def drag_between_coordinates(coordinates):
    # İlk koordinata git ve tıklayıp basılı tut
    x_start, y_start = coordinates[0]
    pydirectinput.moveTo(x_start, y_start)
    time.sleep(0.2)
    pydirectinput.keyDown('f7')  # Sol tıkı basılı tut
    time.sleep(0.2)  # Kısa bir bekleme

    # Koordinatlar arasında sürükleme yap
    for x, y in coordinates[1:]:
        pydirectinput.moveTo(x, y, duration=0.5)  # Koordinatlar arasında hareket etme
        time.sleep(0.2)  # Her adımda kısa bir bekleme

    pydirectinput.keyUp('f7')  # Sol tıkı bırak

# 2 saniye bekleme
time.sleep(2)

# uc-cizgi.png dosyasını arama
template_path = 'uc-cizgi.png'
coordinates = search_image(template_path)

if coordinates:
    # 1 saniye bekleme
    time.sleep(4)

    # Koordinat listesi
    coordinates = [(832, 628), (900, 662), (831, 694), (766, 665)]
    drag_between_coordinates(coordinates)

    # 1 saniye bekleme ve skill-mavi.py dosyasını çalıştırma
    time.sleep(1)
    subprocess.run(['python', 'skill-mavi.py'])
else:
    print("uc-cizgi.png not found. Exiting script.")
