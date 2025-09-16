from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render

# Profile model with user OneToOne relation, profile picture, department, semester, and many-to-many clubs
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png')
    department = models.CharField(
        max_length=50,
        choices=[
            ('CSE', 'CSE'),
            ('EEE', 'EEE'),
            ('Civil', 'Civil'),
            ('Pharmacy', 'Pharmacy'),
            ('ENG', 'ENG'),
            ('Archi', 'Archi'),
            ('BBA', 'BBA'),
        ]
    )
    semester = models.CharField(
        max_length=10,
        choices=[
            ('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'),
            ('4th', '4th'), ('5th', '5th'), ('6th', '6th'),
            ('7th', '7th'), ('8th', '8th'),
        ]
    )
    clubs = models.ManyToManyField("Club", blank=True)

    def __str__(self):
        return self.user.username


# Club model to store clubs
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Home view rendering a template with a sample image url (update as needed)
def home(request):
    return render(request, 'home.html', {
        'image_url': settings.MEDIA_URL + '0bd7856b-f5ed-46f9-bf12-82f4d84246ea.jpg'
    })

