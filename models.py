# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MenuItems(models.Model):
    name = models.CharField()
    category = models.CharField()

    class Meta:
        managed = False
        db_table = 'menu_items'


class MenuItemsAssociation(models.Model):
    pk = models.CompositePrimaryKey('menu_id', 'menu_item_id')
    menu = models.ForeignKey('Menus', models.DO_NOTHING)
    menu_item = models.ForeignKey(MenuItems, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'menu_items_association'
        unique_together = (('menu', 'menu_item'),)


class Menus(models.Model):
    date = models.DateTimeField()
    meal_time = models.CharField()
    meal_location = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'menus'
