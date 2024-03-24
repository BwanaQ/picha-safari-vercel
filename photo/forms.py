from django import forms
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple

from .models import Photo, Tag, Category

class PhotoCreateForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ['owner','webp_image','approved','comments']

class TagCreateForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
