from django.db import models
from generics.models import Timestamp
from cloudinary.models import CloudinaryField
from django.conf import settings
from cloudinary import CloudinaryImage

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
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    image = CloudinaryField('image')
    webp_image = models.URLField(blank=True, null=True)  # Change to URLField to store the URL
    price = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} @ KES {self.price}"

    def save(self, *args, **kwargs):
        # Convert the original image to WebP format and save the URL
        if self.image and not self.webp_image:
            image = CloudinaryImage(self.image)
            webp_version = image.image(transformation={'format': 'webp', 'quality': 'auto'})
            self.webp_image = webp_version.get('url')

        super().save(*args, **kwargs)