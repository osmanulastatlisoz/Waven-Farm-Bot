import pyautogui
import cv2  # cv2 kütüphanesini import ediyoruz
import numpy as np
import time
import pydirectinput
import subprocess

def click_at_coordinates(x, y):
    pydirectinput.moveTo(x, y)
    time.sleep(0.2)
    pydirectinput.keyDown('f7')
    time.sleep(0.2)
    pydirectinput.keyUp('f7')
    print(f"Clicked at coordinates: ({x}, {y})")

def drag_and_wait(start_x, start_y, end_x, end_y):
    pydirectinput.moveTo(start_x, start_y)
    time.sleep(0.2)
    pydirectinput.keyDown('f7')
    time.sleep(0.2)
    pydirectinput.moveTo(end_x, end_y, duration=0.5)
    pydirectinput.keyUp('f7')
    print(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    time.sleep(1)

def search_image(template_path, region=None):
    template = cv2.imread(template_path, 0)
    template_w, template_h = template.shape[::-1]

    for i in range(3):  # 4 kere tarama yap
        start_time = time.time()
        print(f"Searching for image {template_path}... attempt {i+1}/4")

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
            return (center_x, center_y)  # Görseli bulduğunda koordinatları döndür

        # Her tarama arasında 0.1 saniye bekle
        time_elapsed = time.time() - start_time
        time.sleep(max(0, 0.1 - time_elapsed))

    print(f"Image {template_path} not found in 4 attempts.")
    return None

def search_and_click(template_path, region=None):
    coordinates = search_image(template_path, region)
    if coordinates:
        click_at_coordinates(*coordinates)
        return True
    return False

def main():
    time.sleep(4)  # Başlangıçta 1 saniye bekle

    # İlk sürükleme işlemi
    drag_and_wait(768, 659, 960, 568)
    
    # arti-bir.png'ye tıklama ve bekleme
    if search_and_click('arti-bir.png'):
        time.sleep(0.5)

    # pasif-iksir.png'ye tıklama ve 960, 568 koordinatına tıklama
    if search_and_click('pasif-iksir.png'):
        click_at_coordinates(960, 568)
        time.sleep(1)

    # İkinci sürükleme işlemi
    drag_and_wait(960, 568, 1152, 472)

    # cikis.py dosyasını çalıştırma
    subprocess.run(['python', 'cikis.py'])

if __name__ == "__main__":
    main()
