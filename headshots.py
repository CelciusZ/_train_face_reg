#! /usr/bin/python

import cv2
import os

# Kullanıcı adını belirt
name = "miyav"  # Burayı kendi adınla değiştirebilirsin

# Dataset klasörünü ve alt klasörü kontrol et/oluştur
dataset_folder = "dataset"
user_folder = os.path.join(dataset_folder, name)
if not os.path.exists(user_folder):
    os.makedirs(user_folder)
    print(f"[INFO] Klasör oluşturuldu: {user_folder}")

# Kamerayı başlat
cam = cv2.VideoCapture(0)  # 0: dahili kamera, USB için 1 veya 2 deneyebilirsin
if not cam.isOpened():
    print("[ERROR] Kamera açılamadı!")
    exit()

# Çözünürlüğü ayarla
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 500)  # Genişlik
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)  # Yükseklik

# Pencereyi oluştur
cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)

# Resim sayacı
img_counter = 0

# Ana döngü
print("[INFO] Kamera başlatıldı. Space tuşuna basarak fotoğraf çekebilirsin, ESC ile çıkabilirsin.")
while True:
    ret, frame = cam.read()
    if not ret:
        print("[ERROR] Görüntü alınamadı!")
        break

    # Kameradan gelen görüntüyü göster
    cv2.imshow("press space to take a photo", frame)

    # Tuş girişini bekle
    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC tuşu
        print("[INFO] ESC tuşuna basıldı, kapatılıyor...")
        break
    elif k % 256 == 32:  # Space tuşu
        # Resmi kaydet
        img_name = os.path.join(user_folder, f"image_{img_counter}.jpg")
        cv2.imwrite(img_name, frame)
        print(f"[INFO] {img_name} kaydedildi!")
        img_counter += 1

# Kamerayı serbest bırak ve pencereleri kapat
cam.release()
cv2.destroyAllWindows()
print("[INFO] Kamera kapatıldı.")