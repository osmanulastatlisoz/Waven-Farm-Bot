import pyautogui
import cv2
import numpy as np
import time
import pydirectinput
import subprocess  # Sürükleme dosyasını çalıştırmak için

def search_and_click(template_paths, region=None):
    templates = [cv2.imread(path, 0) for path in template_paths]
    template_sizes = [(template.shape[::-1]) for template in templates]

    print("Starting to search for the images.")
    
    for i in range(15):  # 15 kere tarama yap
        start_time = time.time()
        print(f"Searching... attempt {i+1}/15")

        # Belirli bir bölgenin ekran görüntüsünü al
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        for idx, template in enumerate(templates):
            template_w, template_h = template_sizes[idx]

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
                print(f"Found image {idx+1} at coordinates: ({center_x}, {center_y})")
                print("Moving to the coordinates and waiting for 0.2 seconds...")
                pydirectinput.moveTo(center_x, center_y)
                time.sleep(0.2)

                # 3 kere tıklama işlemi
                for _ in range(3):
                    print("Pressing F7 to hold down left click for 0.2 seconds...")
                    pydirectinput.keyDown('f7')
                    time.sleep(0.2)
                    pydirectinput.keyUp('f7')
                    print(f"Clicked at coordinates: ({center_x}, {center_y})")
                    time.sleep(0.35)  # 0.35 saniye bekle

                # Sürükleme dosyasını çalıştır
                subprocess.run(['python', 'surukleme.py'])
                return  # Bulduğunda tıklayıp çıkmak için

        # Her tarama arasında 0.3 saniye bekle
        time_elapsed = time.time() - start_time
        time.sleep(max(0, 0.3 - time_elapsed))

    print("Images not found in 15 attempts.")
    # Eğer resim bulunamazsa cikis.py dosyasını çalıştır
    subprocess.run(['python', 'cikis.py'])

def main():
    # Başlamadan önce 1 saniye bekle
    time.sleep(0.5)

    # play3.png, play2.png ve play.png dosyalarını ara
    template_paths = ['play3.png', 'play2.png', 'play.png']
    search_and_click(template_paths)

if __name__ == "__main__":
    main()
