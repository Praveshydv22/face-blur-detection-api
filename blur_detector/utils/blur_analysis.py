import cv2
import numpy as np

def variance_of_laplacian(gray_face):
    return cv2.Laplacian(gray_face, cv2.CV_64F).var()

def is_face_blurry(face_bgr, threshold=100.0):
    gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    return fm < threshold, float(fm)
