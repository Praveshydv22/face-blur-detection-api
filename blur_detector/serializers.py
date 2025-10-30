from rest_framework import serializers
from .models import ImageUpload

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'original', 'processed', 'uploaded_at']
        read_only_fields = ['id', 'processed', 'uploaded_at']
