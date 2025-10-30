# Face Blur Detection & Correction API

A Django REST API that detects faces, identifies blurred faces (variance of Laplacian), and corrects them using unsharp masking.

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

POST an image to:
`POST /api/blur/upload/` (form-data key: `image`)

See sample images in `/samples/`.

## Author
Auto-generated
