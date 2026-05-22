# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GOAL_CHOICES   = [('bulk','Bulk'),('cut','Cut'),('maintain','Maintain')]
    DIET_CHOICES   = [('veg','Vegetarian'),('non-veg','Non-Veg'),('vegan','Vegan')]
    GENDER_CHOICES = [('male','Male'),('female','Female')]
    LOCATION_CHOICES = [('gym','Gym'),('home','Home')]

    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age           = models.IntegerField(default=25)
    weight_kg     = models.FloatField(default=70)
    height_cm     = models.FloatField(default=170)
    gender        = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    activity_days = models.IntegerField(default=3)
    goal          = models.CharField(max_length=10, choices=GOAL_CHOICES, default='maintain')
    diet_pref     = models.CharField(max_length=10, choices=DIET_CHOICES, default='veg')
    supplements   = models.BooleanField(default=False)
    location      = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='gym')
    avatar        = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def bmi(self):
        return round(self.weight_kg / (self.height_cm / 100) ** 2, 1)

    def bmi_category(self):
        b = self.bmi()
        if b < 18.5: return 'Underweight'
        if b < 25:   return 'Normal'
        if b < 30:   return 'Overweight'
        return 'Obese'

    def __str__(self):
        return f"{self.user.username} profile"