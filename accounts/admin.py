from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'goal', 'diet_pref', 'weight_kg', 'height_cm', 'age']
    search_fields = ['user__username']
    list_filter   = ['goal', 'diet_pref', 'location']