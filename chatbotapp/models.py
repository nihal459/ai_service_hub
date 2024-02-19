from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    is_user = models.BooleanField(default=False, verbose_name='Is User')
    is_service = models.BooleanField(default=False, verbose_name='Is Service Center')
    name = models.CharField(max_length=100, default='User')
    mobile_number = models.CharField(max_length=20, default='Nil')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    location = models.CharField(max_length=300, default='Nil')
    address = models.TextField(max_length=1000, default='Nil')
    district = models.CharField(max_length=150, default='Nil')
    state = models.CharField(max_length=150, default='Nil')
    verified = models.BooleanField(default=False, verbose_name='Is Verified')
    description = models.TextField(max_length=1000, default='Nil')  # Add description field
    website = models.URLField(max_length=200, blank=True, null=True)  # Add website field

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return  url
    

    def __str__(self):
        return self.username
    

from django.db import models
from django.contrib.auth.models import AbstractUser

class Book(models.Model):
    service_center = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_center_books')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    user_date = models.DateField()
    confirm_date = models.DateField(null=True, blank=True)
    user_booking_status = models.CharField(max_length=20, default='Pending')
    service_center_booking_status = models.CharField(max_length=20, default='Pending')
    message = models.TextField(max_length=1000, default='Nil')

    def __str__(self):
        return self.service_center.name
    

    