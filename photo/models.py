from django.db import models
from generics.models import Timestamp
from cloudinary.models import CloudinaryField
from django.conf import settings
import cloudinary.uploader
import uuid
import os

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
    webp_image = models.URLField(blank=True)  # Change to URLField to store the URL
    price = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} @ KES {self.price}"

class Photo(Timestamp):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    image = CloudinaryField('image')
    webp_image = models.URLField(blank=True)  # Change to URLField to store the URL
    price = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} @ KES {self.price}"

    def save(self, *args, **kwargs):
        # Convert the original image to WebP format and save the URL
        if self.image and not self.webp_image:
            # Upload the original image to Cloudinary
            upload_result = cloudinary.uploader.upload(self.image.file)
            original_url = upload_result['secure_url']

            # Generate a unique identifier for the WebP filename
            unique_identifier = uuid.uuid4().hex

            # Construct the filename for the WebP version of the image
            original_filename, original_extension = os.path.splitext(upload_result['public_id'])
            webp_filename = f"{original_filename}_webp_{unique_identifier}.webp"

            # Construct the URL for the WebP version of the image
            webp_url = f"{upload_result['secure_url'][:-4]}/{webp_filename}"

            # Save the WebP image URL
            self.webp_image = webp_url

            # Convert the original image to WebP format and upload to Cloudinary
            cloudinary.uploader.upload(self.image.file, public_id=webp_filename, format="webp")

        super().save(*args, **kwargs)

