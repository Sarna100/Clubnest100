from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from django.shortcuts import render
import uuid


# ==============================
# Club Model
# ==============================
class Club(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='club_image/', null=True, blank=True)
    caption = models.TextField(blank=True)
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    introduction = models.TextField(blank=True)
    our_goal = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ==============================
# Profile Model
# ==============================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png', blank=True, null=True)

    department = models.CharField(
        max_length=50,
        choices=[
            ('CSE', 'CSE'), ('EEE', 'EEE'), ('Civil', 'Civil'),
            ('Pharmacy', 'Pharmacy'), ('ENG', 'ENG'),
            ('Archi', 'Archi'), ('BBA', 'BBA'),
        ],
        blank=True,
        null=True
    )

    semester = models.CharField(
        max_length=10,
        choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'),
                 ('4th', '4th'), ('5th', '5th'), ('6th', '6th'),
                 ('7th', '7th'), ('8th', '8th')],
        blank=True,
        null=True
    )

    clubs = models.ManyToManyField('Club', through='Membership', blank=True)

    def __str__(self):
        return self.user.username


# ==============================
# Membership Model (Fixed)
# ==============================
class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # ✅ Added
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'club')

    def __str__(self):
        status = "Approved" if self.is_approved else "Pending"
        return f"{self.profile.user.username} - {self.club.name} ({status})"


# ==============================
# Event Model
# ==============================
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('sport', 'Sport'),
        ('cultural', 'Cultural'),
        ('math', 'Math'),
        ('drama', 'Drama'),
        ('cybersecurity', 'Cyber Security'),
        ('software-hardware', 'Software & Hardware'),
        ('english-learning', 'English Learning'),
        ('debating-speaking', 'Debating & Public Speaking'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    society = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    attendees = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    image = models.ImageField(upload_to='event_images/')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True, help_text="Event organizing club")

    def __str__(self):
        return self.title


# ==============================
# Participation Model
# ==============================
class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


# ==============================
# Certificate Model
# ==============================
class Certificate(models.Model):
    participation = models.OneToOneField(Participation, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=100, null=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"Certificate for {self.participation.user.username} - {self.participation.event.title}"


# ==============================
# Optional Home View
# ==============================
def home(request):
    return render(request, 'home.html', {
        'image_url': settings.MEDIA_URL + '0bd7856b-f5ed-46f9-bf12-82f4d84246ea.jpg'
  })
