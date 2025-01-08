import pydirectinput
import time

print("3 saniye bekliyor...")
time.sleep(3)
print("Çift tıklıyor...")
pydirectinput.doubleClick(39, 190)  # Ekranın sol üst köşesine yakın bir noktayı çift tıklar
print("Çift tıkladı")