#! /usr/bin/python

# Gerekli paketleri import et
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

# Eğitilmiş modelin dosya yolunu belirt
encodingsP = "encodings.pickle"

# Tanımlanan kişiyi takip etmek için değişken
currentname = "Unknown"

# Eğitilmiş verileri yükle
print("[INFO] loading encodings...")
data = pickle.loads(open(encodingsP, "rb").read())

# Video akışını başlat ve kameranın ısınması için bekle
print("[INFO] starting video stream...")
vs = VideoStream(src=0, framerate=10).start()  # src=0 dahili kamera, USB kamera için 1 veya 2 deneyebilirsin
time.sleep(2.0)  # Kameranın hazır olması için kısa bir bekleme

# FPS sayacını başlat
fps = FPS().start()

# Sürekli döngü ile kamera görüntüsünü işle
while True:
    # Kameradan bir kare al ve boyutunu küçült (hız için)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    # Yüzlerin koordinatlarını bul (RGB formatında)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog")

    # Yüzlerin özellik vektörlerini hesapla
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # Her yüzün özellik vektörünü kontrol et
    for encoding in encodings:
        # Eğitilmiş verilerle eşleştirme yap
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"  # Eşleşme yoksa "Unknown"

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

            # Yeni bir kişi tanınırsa konsola yaz
            if currentname != name:
                currentname = name
                print(f"[INFO] Tanımlanan kişi: {currentname}")

        # İsimleri listeye ekle
        names.append(name)

    # Tanınan yüzleri çerçevele ve isimlerini yaz
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # Yüzün etrafına dikdörtgen çiz (sarı renk)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        # İsim için pozisyon ayarla
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 2)

    # Görüntüyü ekranda göster
    cv2.imshow("Facial Recognition is Running", frame)

    # 'q' tuşuna basılırsa çık
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # FPS sayacını güncelle
    fps.update()

# FPS bilgisini göster ve temizlik yap
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()



import cv2

name = 'miyav' #replace with your name

cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("press space to take a photo", 500, 300)
cam.set(3, 500)
cam.set(4, 300)
img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
