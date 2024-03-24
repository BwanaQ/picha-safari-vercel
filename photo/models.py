from django.db import models
from generics.models import Timestamp
from cloudinary.models import CloudinaryField
from django.conf import settings
import cloudinary.uploader
import uuid


class Tag(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Photo(Timestamp):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    image = CloudinaryField('image')
    webp_image = models.URLField(blank=True)  # Field to store WebP image URL
    price = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} @ KES {self.price}"

    def save(self, *args, **kwargs):
        # Convert and save the image to WebP format
        if self.image:
            # Check if the image is already stored in Cloudinary
            if hasattr(self.image, 'url'):
                # If the image is already stored in Cloudinary, construct the WebP image URL
                original_image_url = self.image.url
                webp_image_url = f"{original_image_url}.webp"
                
                # Save the WebP image URL
                self.webp_image = webp_image_url
            else:
                # If the image is uploaded via a form, upload it to Cloudinary and convert it to WebP format
                upload_result = cloudinary.uploader.upload(self.image, format="webp")
                
                # Get the secure URL of the uploaded image in WebP format
                webp_image_url = upload_result['secure_url']
                
                # Save the WebP image URL
                self.webp_image = webp_image_url
        
        # Call the superclass's save method to save the object
        super().save(*args, **kwargs)