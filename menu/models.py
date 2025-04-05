# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MenuItems(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'menu_items'


class MenuItemsAssociation(models.Model):
    id = models.AutoField(primary_key=True) 
    menu = models.ForeignKey('Menus', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'menu_items_association'
        constraints = [
            models.UniqueConstraint(
                fields=['menu','menu_item'], name='unique_menu_item_association'
            )
        ]
        



class Menus(models.Model):
    date = models.DateTimeField()
    meal_time = models.CharField()
    meal_location = models.TextField()

    class Meta:
        managed = False
        db_table = 'menus'
