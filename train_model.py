#! /usr/bin/python

# Gerekli paketleri import et
from imutils import paths
import face_recognition
import pickle
import cv2
import os

# Veri setinin bulunduğu ana klasörü belirt
print("[INFO] start processing faces...")
dataset_folder = "dataset"  # Ana klasör adı
imagePaths = list(paths.list_images(dataset_folder))  # "dataset" içindeki tüm resimleri tara

# Bilinen yüz özelliklerini ve isimleri saklamak için listeler
knownEncodings = []
knownNames = []

# Resim yollarını döngüyle tara
for (i, imagePath) in enumerate(imagePaths):
    # Resim yolundan kişi adını çıkar (alt klasör adı)
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]  # Alt klasör adını al (me, sero, yildirim vb.)

    # Resmi yükle ve BGR’den RGB’ye çevir
    image = cv2.imread(imagePath)
    if image is None:
        print(f"[ERROR] Resim yüklenemedi: {imagePath}")
        continue
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Yüzlerin koordinatlarını bul
    boxes = face_recognition.face_locations(rgb, model="hog")
    if not boxes:
        print(f"[WARNING] Yüz bulunamadı: {imagePath}")
        continue

    # Yüzlerin özellik vektörlerini hesapla
    encodings = face_recognition.face_encodings(rgb, boxes)
    if not encodings:
        print(f"[WARNING] Özellik vektörü çıkarılamadı: {imagePath}")
        continue

    # Her özellik vektörünü ve ismi listeye ekle
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

# Yüz özelliklerini ve isimleri diske kaydet
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
with open("encodings.pickle", "wb") as f:
    f.write(pickle.dumps(data))

print("[INFO] Model başarıyla eğitildi ve encodings.pickle dosyasına kaydedildi.")