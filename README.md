# Yüz Tanıma Projesi

Bu proje, Python ile yüz tanıma yapar. `face_recognition` ve OpenCV ile yazıldı. Eğitim, offline (resimden) ve online (kameradan) tanıma içerir.

## Projenin Yapısı
- `dataset/`: Yüz verilerinin durduğu klasör. İçinde alt klasörler (örneğin `miyav/`) ve resimler (örneğin `dataset/miyav/image_0.jpg`) var.
- `train_model.py`: `dataset`teki resimleri işleyip `encodings.pickle` dosyasına model kaydeder.
- `capture_images.py`: Kameradan resim çeker, `dataset/miyav/` gibi alt klasörlere kaydeder.
- `recognize_from_image.py`: `test_resmi.jpg`yi tanır, `output.jpg`ye yazar.
- `recognize_from_camera.py`: Kameradan gerçek zamanlı yüz tanır, ekranda gösterir.
- `test_resmi.jpg`: Test için resim. [Bak](https://github.com/kullanici_adin/repo_adin/blob/main/test_resmi.jpg)
- `output.jpg`: Tanıma sonrası işaretlenmiş resim. [Bak](https://github.com/kullanici_adin/repo_adin/blob/main/output.jpg)
- `encodings.pickle`: Eğitilmiş modelin dosyası.

## `dataset` Klasörü Ne İşe Yarar?
`dataset`, modelin tanıyacağı yüzlerin resimlerini saklar. Alt klasörler (mesela `miyav/`) o kişinin resimlerini içerir. Kameradan veri toplamak için `capture_images.py` kullanılır: kodu çalıştır, "Space"e bas, resimler kaydedilir.

## Eğitim: `train_model.py`
`dataset`teki resimleri tarar, `face_recognition` ile yüzleri bulur, `encodings.pickle`a yazar. Çalıştırmak için: `python train_model.py`.

## Kameradan Veri Toplama: `capture_images.py`
Kamerayı açar, "Space" ile `dataset/miyav/image_X.jpg` gibi resimler çeker, "ESC" ile çıkar. Çalıştırmak için: `python capture_images.py`.

## Offline Tanıma: `recognize_from_image.py`
`test_resmi.jpg`yi okur, `encodings.pickle` ile karşılaştırır, tanınan yüzleri işaretler, `output.jpg`ye kaydeder, ekranda gösterir. Çalıştırmak için: `python recognize_from_image.py`.

## Online Tanıma: `recognize_from_camera.py`
Kamerayı açar, her karede yüzleri tanır, `encodings.pickle` ile eşleştirir, tanınanları ekranda gösterir, "q" ile kapanır. Çalıştırmak için: `python recognize_from_camera.py`.
