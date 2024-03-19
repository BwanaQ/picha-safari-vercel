import cloudinary
import cloudinary.uploader
import cloudinary.api
import zipfile
import os
from django.core.mail import EmailMessage
from django.conf import settings

class CartService:
    @staticmethod
    def process_cart_and_send_email(cart_items, buyer_email):
        pass
    

    @staticmethod
    def get_cloudinary_photo_id(photo_url):
        pass


    @staticmethod
    def download_photo(photo_id):
        pass


    @staticmethod
    def create_zip_file():
        pass

    @staticmethod
    def send_email_with_attachment(buyer_email, attachment_path):
        pass
