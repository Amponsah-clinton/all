from django.db import models

class FileUpload(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
    converted_file = models.FileField(upload_to='converted/', blank=True, null=True)
    original_format = models.CharField(max_length=10)
    target_format = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uploaded_file.name} to {self.target_format}"
