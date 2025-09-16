from django.db import models

# Create your models here.
from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {
        'image_url': settings.MEDIA_URL + '0bd7856b-f5ed-46f9-bf12-82f4d84246ea.jpg'
    })

