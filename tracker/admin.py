from django.contrib import admin
from .models import FoodLog, DietPlan, WorkoutPlan, ChatMessage

@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display  = ['user', 'meal_type', 'total_kcal', 'total_protein', 'logged_at']
    list_filter   = ['meal_type', 'logged_at']
    search_fields = ['user__username']

@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'calorie_target', 'generated_at', 'is_active']

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'generated_at', 'is_active']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display  = ['user', 'role', 'created_at']
    search_fields = ['user__username', 'content']