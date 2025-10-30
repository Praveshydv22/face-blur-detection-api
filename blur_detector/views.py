from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ImageUploadSerializer
from .models import ImageUpload
from django.core.files.base import ContentFile
import cv2, numpy as np
from .utils.face_detect import detect_faces_opencv
from .utils.blur_analysis import is_face_blurry
from .utils.deblur import unsharp_mask
from PIL import Image
import io

def pil_from_cv2(cv2_img_bgr):
    cv2_img_rgb = cv2.cvtColor(cv2_img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv2_img_rgb)

def cv2_from_file(file):
    arr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

class ImageUploadView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'detail': "No image provided (field 'image')."}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['image']
        inst = ImageUpload(original=file)
        inst.save()

        file.seek(0)
        img = cv2_from_file(file)
        if img is None:
            return Response({'detail': 'Invalid image.'}, status=status.HTTP_400_BAD_REQUEST)

        faces = detect_faces_opencv(img)
        results = []
        processed_img = img.copy()

        for idx, (x,y,w,h) in enumerate(faces):
            x1,y1,x2,y2 = int(x), int(y), int(x+w), int(y+h)
            face_crop = img[y1:y2, x1:x2]
            blurry, fm = is_face_blurry(face_crop, threshold=100.0)
            face_result = {
                'face_id': idx,
                'bbox': [x1,y1,x2,y2],
                'blur_detected': blurry,
                'focus_measure': fm
            }
            if blurry:
                sharpened = unsharp_mask(face_crop, kernel_size=(0,0), sigma=1.0, amount=1.5)
                processed_img[y1:y2, x1:x2] = sharpened
                face_result['correction'] = 'unsharp_mask_applied'
            else:
                face_result['correction'] = 'none_needed'
            results.append(face_result)

        pil = pil_from_cv2(processed_img)
        buf = io.BytesIO()
        pil.save(buf, format='JPEG')
        buf.seek(0)
        inst.processed.save(f'processed_{inst.id}.jpg', ContentFile(buf.read()))
        inst.save()

        response = {
            'id': inst.id,
            'original_url': request.build_absolute_uri(inst.original.url) if hasattr(request, 'build_absolute_uri') else inst.original.url,
            'processed_url': request.build_absolute_uri(inst.processed.url) if hasattr(request, 'build_absolute_uri') else inst.processed.url,
            'faces': results
        }
        return Response(response, status=status.HTTP_201_CREATED)
