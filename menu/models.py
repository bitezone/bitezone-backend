
from django.db import models

class MenuItems(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'menu_items'

class Menus(models.Model):
    date = models.DateTimeField()
    meal_time = models.CharField(max_length=100)
    meal_location = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'menus'

class MenuItemsAssociation(models.Model):
    id = models.AutoField(primary_key=True) 
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.PROTECT)
    
    class Meta:
        managed = False
        db_table = 'menu_items_association'
        constraints = [
            models.UniqueConstraint(
                fields=['menu', 'menu_item'], name='unique_menu_item_association'
            )
        ]