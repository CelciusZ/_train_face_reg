import sys
import cv2
import numpy as np

PAD = 0.10
BLOCKS = 8


def detect(gray, cascade):
    return cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))


def redact(img, boxes):
    out = img.copy()
    mask = np.zeros(img.shape[:2], np.uint8)
    h, w = img.shape[:2]
    for (x, y, bw, bh) in boxes:
        px, py = int(bw * PAD), int(bh * PAD)
        x0, y0 = max(0, x - px), max(0, y - py)
        x1, y1 = min(w, x + bw + px), min(h, y + bh + py)
        roi = out[y0:y1, x0:x1]
        small = cv2.resize(roi, (BLOCKS, BLOCKS), interpolation=cv2.INTER_AREA)
        blocks = cv2.resize(small, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST)
        k = max(3, ((x1 - x0) // 4) | 1)
        out[y0:y1, x0:x1] = cv2.GaussianBlur(blocks, (k, k), 0)
        mask[y0:y1, x0:x1] = 255
    return out, mask


def psnr(a, b):
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255.0 ** 2 / mse)


def main(src, dst):
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = cv2.imread(src)
    boxes = detect(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cascade)
    out, mask = redact(img, boxes)

    outside = mask == 0
    diff_before = int(np.abs(out.astype(int) - img.astype(int))[outside].max())
    cv2.imwrite(dst, out, [cv2.IMWRITE_JPEG_QUALITY, 95])
    saved = cv2.imread(dst)

    print(f"faces detected in input:    {len(boxes)}")
    print(f"faces detected after redact: {len(detect(cv2.cvtColor(saved, cv2.COLOR_BGR2GRAY), cascade))}")
    print(f"max pixel change outside mask before encoding: {diff_before}")
    print(f"PSNR outside mask after JPEG encoding: {psnr(saved[outside], img[outside]):.1f} dB")
    print(f"redacted area: {100 * (~outside).mean():.1f}% of frame")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "test_resmi.jpg",
         sys.argv[2] if len(sys.argv) > 2 else "redacted.jpg")
