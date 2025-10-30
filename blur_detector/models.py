from django.db import models

class ImageUpload(models.Model):
    original = models.ImageField(upload_to='uploads/originals/')
    processed = models.ImageField(upload_to='uploads/processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ImageUpload {self.id}"
