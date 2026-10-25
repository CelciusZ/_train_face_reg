# Face Detection & Recognition

**English** | [Türkçe](README.tr.md)

Face detection and recognition in Python, built with `face_recognition` (dlib) and OpenCV. It covers enrolment, recognition from an image and from a live camera, and face redaction.

## Project structure
- `dataset/`: enrolment images, one subfolder per person (for example `dataset/me/image_0.jpg`). The folder name is the label.
- `capture_images.py`: captures webcam images into `dataset/<name>/`.
- `train_model.py`: encodes the faces in `dataset/` and saves them to `encodings.pickle`.
- `recognize_from_image.py`: recognises faces in `test_resmi.jpg` and writes `output.jpg`.
- `recognize_from_camera.py`: real-time recognition from the webcam.
- `redact_image.py`: blurs every detected face and measures the result.
- `haarcascade_frontalface_default.xml`: OpenCV Haar cascade used by `redact_image.py`.
- `test_resmi.jpg`, `output.jpg`, `redacted.jpg`: test image, recognition output and redaction output.
- `encodings.pickle`: the enrolled face encodings.

## Requirements
```
pip install face_recognition opencv-python imutils numpy
```
`face_recognition` depends on dlib, which needs CMake and a C++ compiler on Windows.

## Collecting enrolment images: `capture_images.py`
Opens the webcam. Space saves a frame as `dataset/<name>/image_X.jpg` and Esc quits.
```
python capture_images.py
```

## Encoding: `train_model.py`
Walks `dataset/`, finds faces with the HOG detector, computes a 128-d encoding for each face and writes them to `encodings.pickle`. Images that can't be read, contain no face or fail to encode are skipped with a warning.
```
python train_model.py
```

## Recognition from an image: `recognize_from_image.py`
Reads `test_resmi.jpg`, compares each face with `encodings.pickle`, draws a yellow box with the recognised name and saves `output.jpg`.
```
python recognize_from_image.py
```

| Input | Output |
|---|---|
| ![Input](test_resmi.jpg) | ![Output](output.jpg) |

## Live recognition: `recognize_from_camera.py`
Opens the webcam and recognises faces in every frame. `q` quits.
```
python recognize_from_camera.py
```

## Face redaction: `redact_image.py`
Detects faces with the Haar cascade, pads each box by 10%, reduces it to 8x8 blocks and blurs it. Pixels outside the boxes are not touched. The script measures its own output:

```
python redact_image.py test_resmi.jpg redacted.jpg
faces detected in input:    1
faces detected after redact: 0
max pixel change outside mask before encoding: 0
PSNR outside mask after JPEG encoding: 56.3 dB
redacted area: 18.6% of frame
```

![Redacted output](redacted.jpg)
