import cv2
import numpy as np

def unsharp_mask(image_bgr, kernel_size=(0,0), sigma=1.0, amount=1.5, threshold=0):
    blurred = cv2.GaussianBlur(image_bgr, kernel_size if kernel_size!=(0,0) else (0,0), sigma)
    sharpened = cv2.addWeighted(image_bgr, 1+amount, blurred, -amount, 0)
    if threshold > 0:
        low_contrast_mask = np.abs(image_bgr - blurred) < threshold
        np.copyto(sharpened, image_bgr, where=low_contrast_mask)
    return sharpened
