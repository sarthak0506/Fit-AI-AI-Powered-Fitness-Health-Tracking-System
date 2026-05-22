# tracker/models.py
from django.db import models
from django.contrib.auth.models import User
import json

class FoodLog(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_logs')
    image       = models.ImageField(upload_to='food_logs/')
    detected    = models.TextField(default='[]')   # JSON list of detected foods
    total_kcal  = models.IntegerField(default=0)
    total_protein = models.IntegerField(default=0)
    meal_type   = models.CharField(max_length=20, default='meal',
                    choices=[('breakfast','Breakfast'),('lunch','Lunch'),
                             ('snack','Snack'),('dinner','Dinner'),('meal','Meal')])
    logged_at   = models.DateTimeField(auto_now_add=True)

    def get_detected(self):
        return json.loads(self.detected)

    def __str__(self):
        return f"{self.user.username} — {self.total_kcal} kcal — {self.logged_at.date()}"


class DietPlan(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_plans')
    plan_data      = models.TextField()   # JSON
    calorie_target = models.IntegerField(default=2000)
    generated_at   = models.DateTimeField(auto_now_add=True)
    is_active      = models.BooleanField(default=True)

    def get_plan(self):
        return json.loads(self.plan_data)


class WorkoutPlan(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    plan_data    = models.TextField()   # JSON
    generated_at = models.DateTimeField(auto_now_add=True)
    is_active    = models.BooleanField(default=True)

    def get_plan(self):
        return json.loads(self.plan_data)


class ChatMessage(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    role       = models.CharField(max_length=10)   # 'user' or 'assistant'
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']