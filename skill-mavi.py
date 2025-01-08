import pyautogui
import cv2
import numpy as np
import time
import pydirectinput
import subprocess
import random

def search_and_click(template_path, region=None):
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
            print("Moving to the coordinates and waiting for 0.2 seconds...")
            pydirectinput.moveTo(center_x, center_y)
            time.sleep(0.2)
            print("Pressing F7 to hold down left click for 0.2 seconds...")
            pydirectinput.keyDown('f7')
            time.sleep(0.2)  # 0.2 saniye bekle
            pydirectinput.keyUp('f7')
            print(f"Clicked at coordinates: ({center_x}, {center_y})")
            return True  # Bulduğunda tıklayıp çıkmak için

        # Her tarama arasında 0.1 saniye bekle
        time_elapsed = time.time() - start_time
        time.sleep(max(0, 0.1 - time_elapsed))

    print(f"Image {template_path} not found in 4 attempts.")
    return False

def click_at_coordinates(x, y):
    pydirectinput.moveTo(x, y)
    time.sleep(0.2)
    pydirectinput.keyDown('f7')
    time.sleep(0.2)
    pydirectinput.keyUp('f7')
    print(f"Clicked at coordinates: ({x}, {y})")

def click_and_wait(image, coordinates):
    if search_and_click(image):
        click_at_coordinates(*coordinates)
        return True
    return False

def handle_end_turn():
    if search_and_click('end-turn.png'):
        search_and_click('yes.png')
        time.sleep(7)

def perform_drag(start_coords, end_coords):
    pydirectinput.moveTo(start_coords[0], start_coords[1])
    time.sleep(0.2)
    pydirectinput.keyDown('f7')
    time.sleep(0.2)
    pydirectinput.moveTo(end_coords[0], end_coords[1], duration=0.5)
    pydirectinput.keyUp('f7')
    print(f"Dragged from {start_coords} to {end_coords}")

def main():
    time.sleep(0.1)  # Başlangıçta 0.1 saniye bekle
    coordinates = (704, 567)
    skill_images = ['skill-yesil-parmak.png', 'skill-mor-iksir.png', 'skill-kirmizi-iksir.png', 'skill-yesil-iksir.png']
    
    for attempt in range(5):  # 5 döngü boyunca dene
        print(f"Attempt {attempt+1} of 5")
        
        if search_and_click('skill-mavi.png'):
            click_at_coordinates(*coordinates)
            # Sürükleme işlemleri
            perform_drag((958, 696), (840, 697))
            time.sleep(0.5)
            perform_drag((898, 662), (835, 695))
            time.sleep(0.5)

            random.shuffle(skill_images)
            for skill in skill_images:
                if click_and_wait(skill, coordinates):
                    break
            handle_end_turn()
            subprocess.run(['python', 'movement.py'])  # Movement.py'yi çalıştır
            return
        
        else:
            random.shuffle(skill_images)
            skill_clicks = 0  # Tıklanan skill sayısı
            for skill in skill_images:
                if click_and_wait(skill, coordinates):
                    skill_clicks += 1
                    if skill_clicks >= 2:
                        break  # İki tane tıklama yapıldıysa daha fazla arama
            handle_end_turn()

    # 5 döngüde de skill-mavi.png bulunamazsa give-up.py'yi çalıştır
    subprocess.run(['python', 'give-up.py'])

if __name__ == "__main__":
    main()
