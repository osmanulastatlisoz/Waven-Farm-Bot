import pyautogui
import keyboard

print("Press the 'Space' key to get the current mouse coordinates.")

# Space tuşuna basıldığında çalışacak fonksiyon
def get_mouse_position():
    for _ in range(4):
        keyboard.wait('space')
        x, y = pyautogui.position()
        print(f"Mouse coordinates: X: {x} Y: {y}")
    print("Program terminated.")
    return

get_mouse_position()
