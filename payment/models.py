from django.db import models
from cart.models import Cart
from django.conf import settings


STATUS = [
    ("PENDING", "PENDING"),
    ("COMPLETE", "COMPLETE"),
    ("CANCELLED", "CANCELLED"),
    ("FAILED", "FAILED"),
]

PURPOSE = [
    ("CHECKOUT", "CHECKOUT"),

]


class DatingModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class Transaction(DatingModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='usertransactions')
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0.0)
    mobile = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=STATUS, default="PENDING")
    reference = models.CharField(max_length=100, blank=True, null=True)
    receiptnumber = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    checkoutid = models.CharField(max_length=255,  blank=True, null=True)
    timestamp = models.CharField(max_length=255, default="0000000000",  blank=True, null=True)
    purpose = models.CharField(max_length=255,  choices=PURPOSE, default="CHECKOUT")
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name="carttransactions")

    class Meta:
        ordering = ["-date_created"]
        app_label = "payment"

    def __str__(self):
        return f"{self.mobile} has sent {self.amount} >> {self.receiptnumber} for cart #{self.cart.id}"