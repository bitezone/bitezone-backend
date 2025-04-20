from django.db import models
from django.contrib.auth import get_user_model
from menu.models import MenuItems

User = get_user_model()

class MealSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_sessions")
    date = models.DateTimeField()
    meal_time = models.CharField(max_length=100)
    meal_location = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_calories = models.PositiveIntegerField(default=0) 
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table="user_meal_session"

class MealItemEntry(models.Model):
    session = models.ForeignKey(MealSession, on_delete=models.CASCADE, related_name="meal_items")
    menu_item = models.ForeignKey("menu.MenuItems", on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table="user_meal_items_entries"
