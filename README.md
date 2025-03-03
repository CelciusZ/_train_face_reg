- **Amaç**: Modelin tanıyacağı kişilere ait yüz verilerini organize etmek.
- **Veri Alma**: Kameradan veri toplamak için `capture_images.py` kullanılır.

### Kameradan Veri Nasıl Alınır?
`capture_images.py` dosyası, kameradan görüntü alarak `dataset` klasörüne resimleri kaydeder:
1. Kullanıcı adını kodda belirtin: `name = "me"`.
2. Terminalde çalıştırın: `python capture_images.py`.
3. Kamera açılır, "Space" tuşuna her bastığınızda `dataset/me/image_X.jpg` şeklinde bir resim kaydedilir.
4. "ESC" tuşuyla çıkılır.
- **Not**: Kamera çalışmazsa, `cv2.VideoCapture(0)` yerine `1` veya `2` gibi farklı bir indeks deneyin.

## Eğitim Süreci: `train_model.py`
Bu dosya, `dataset` klasöründeki resimleri okuyarak bir yüz tanıma modeli oluşturur ve sonuçları `encodings.pickle` dosyasına kaydeder.
- **Nasıl Çalışır?**
  1. `dataset` klasöründeki tüm resimleri tarar.
  2. Her resimdeki yüzlerin koordinatlarını `face_recognition.face_locations` ile bulur (`hog` modeli kullanılır).
  3. Yüzlerin özellik vektörlerini (embeddings) `face_recognition.face_encodings` ile çıkarır.
  4. Bu vektörleri ve kişi isimlerini bir sözlükte toplar, ardından `pickle` ile diske kaydeder.
- **Çalıştırma**: `python train_model.py`
- **Çıktı**: `encodings.pickle` dosyası oluşur.

### Haar Cascade Nedir?
Haar Cascade, OpenCV’nin sunduğu bir yüz algılama yöntemidir ve makine öğrenimi tabanlıdır. Ancak bu projede Haar Cascade yerine `face_recognition` kütüphanesinin `hog` modeli tercih edilmiştir. Farklar:
- **Haar Cascade**: Daha hızlı ama daha az hassas, genellikle basit yüz algılama için kullanılır.
- **HOG (Histogram of Oriented Gradients)**: Daha doğru yüz algılama yapar ve `face_recognition` ile özellik vektörü çıkarma için optimize edilmiştir.

## Offline Detection: `recognize_from_image.py`
Bu dosya, tek bir resim üzerinden yüz tanıma yapar.
- **Nasıl Çalışır?**
  1. `test_resmi.jpg` gibi bir resmi okur.
  2. `encodings.pickle` dosyasındaki verilerle yüzleri karşılaştırır.
  3. Tanınan yüzlerin etrafına dikdörtgen çizer ve isimlerini yazar.
  4. Sonucu `output.jpg` olarak kaydeder ve ekranda gösterir.
- **Çalıştırma**: `python recognize_from_image.py`
- **Örnek**:
  - **Giriş Resmi**: [test_resmi.jpg](https://github.com/kullanici_adin/repo_adin/blob/main/test_resmi.jpg)
  - **Çıktı Resmi**: [output.jpg](https://github.com/kullanici_adin/repo_adin/blob/main/output.jpg)

## Online Detection: `recognize_from_camera.py`
Bu dosya, kameradan gerçek zamanlı yüz tanıma yapar.
- **Nasıl Çalışır?**
  1. Kamerayı başlatır ve her kareyi okur.
  2. `encodings.pickle` dosyasındaki verilerle yüzleri karşılaştırır.
  3. Tanınan yüzlerin etrafına dikdörtgen çizer ve isimlerini yazar.
  4. Görüntüyü ekranda gösterir, "q" tuşuyla çıkılır.
- **Çalıştırma**: `python recognize_from_camera.py`
- **Not**: Kamera çalışmazsa, `VideoStream(src=0)` yerine `src=1` veya `src=2` deneyin.

## Kurulum
1. Gerekli kütüphaneleri yükleyin:
