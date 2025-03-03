#! /usr/bin/python

# Gerekli paketleri import et
import face_recognition
import pickle
import cv2
import os

# Eğitilmiş modelin dosya yolunu belirt
encodingsP = "encodings.pickle"

# Tanıma yapmak istediğin resim dosyasını belirt
image_path = "test_resmi.jpg"  # Buraya tanıyacağın resmi koy, örneğin "C:/path/to/test_resmi.jpg"

# Eğitilmiş verileri yükle
print("[INFO] loading encodings...")
data = pickle.loads(open(encodingsP, "rb").read())

# Resmi oku
print("[INFO] processing image...")
if not os.path.exists(image_path):
    print(f"[ERROR] Resim dosyası bulunamadı: {image_path}")
    exit()

image = cv2.imread(image_path)
if image is None:
    print(f"[ERROR] Resim yüklenemedi: {image_path}")
    exit()

# OpenCV’nin BGR formatını RGB’ye çevir (face_recognition RGB bekler)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Yüzlerin koordinatlarını tespit et
boxes = face_recognition.face_locations(rgb, model="hog")

# Yüzlerin özellik vektörlerini (embeddings) hesapla
encodings = face_recognition.face_encodings(rgb, boxes)

# Tanınan isimleri saklamak için liste
names = []

# Her yüzün özellik vektörünü döngüyle kontrol et
for encoding in encodings:
    # Eğitilmiş verilerle eş化leştirme yap
    matches = face_recognition.compare_faces(data["encodings"], encoding)
    name = "Unknown"  # Eğer eşleşme yoksa "Unknown" yaz

    # Eşleşme varsa
    if True in matches:
        # Eşleşen yüzlerin indekslerini bul
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}

        # Her eşleşen yüz için oy sayımı yap
        for i in matchedIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1

        # En çok oy alan ismi seç
        name = max(counts, key=counts.get)
        print(f"[INFO] Tanımlanan kişi: {name}")

    # İsimleri listeye ekle
    names.append(name)

# Tanınan yüzleri resim üzerinde işaretle
for ((top, right, bottom, left), name) in zip(boxes, names):
    # Yüzün etrafına dikdörtgen çiz (BGR renk formatında: sarı)
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 225), 2)
    # İsim yazısı için pozisyon ayarla
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 255), 2)

# İşlenmiş resmi göster
cv2.imshow("Face Recognition Result", image)
cv2.waitKey(0)  # Bir tuşa basılana kadar bekle

# Pencereyi kapat ve temizlik yap
cv2.destroyAllWindows()

# İşlenmiş resmi kaydet (isteğe bağlı)
cv2.imwrite("output.jpg", image)
print("[INFO] İşlenmiş resim 'output.jpg' olarak kaydedildi.")