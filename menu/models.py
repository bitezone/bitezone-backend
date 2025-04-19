from django.db import models


class MenuItems(models.Model):
    name = models.CharField()
    category = models.CharField()
    serving_size = models.CharField()
    calories_per_serving = models.IntegerField()

    ingredients = models.ManyToManyField(
        "ingredients",
        through="MenuItemsIngredientsAssociation",
        related_name="menu_items",
    )

    allergies = models.ManyToManyField(
        "allergies", through="MenuItemsAllergiesAssociation", related_name="menu_items"
    )

    class Meta:
        managed = False
        db_table = "menu_items"


class Menus(models.Model):
    date = models.DateTimeField()
    meal_time = models.CharField(max_length=100)
    meal_location = models.TextField()

    class Meta:
        managed = False
        db_table = "menus"


class MenuItemsAssociation(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = "menu_items_association"
        constraints = [
            models.UniqueConstraint(
                fields=["menu", "menu_item"], name="unique_menu_item_association"
            )
        ]


class Ingredients(models.Model):
    ingredient = models.CharField()

    def __str__(self):
        return self.ingredient

    class Meta:
        managed = False
        db_table = "ingredients"


class Allergies(models.Model):
    allergy_type = models.CharField()

    def __str__(self):
        return self.allergy_type

    class Meta:
        managed = False
        db_table = "allergies"


class MenuItemsIngredientsAssociation(models.Model):
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "menu_items_ingredients_association"


class MenuItemsAllergiesAssociation(models.Model):
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergies, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "menu_items_allergies_association"
