from rest_framework import serializers
from .models import (
    MenuItems,
    MenuItemsAllergiesAssociation,
    Menus,
    MenuItemsAssociation,
    Ingredients,
    Allergies,
)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ["id", "ingredient"]


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = ["id", "allergy_type"]


class MenuItemNutritionSerializer(serializers.ModelSerializer):
    ingredients = serializers.StringRelatedField(many=True, read_only=True)
    allergies = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = MenuItems
        fields = [
            "id",
            "name",
            "category",
            "serving_size",
            "calories_per_serving",
            "ingredients",
            "allergies",
        ]


class MenuItemInMenuSerializer(serializers.ModelSerializer):
    # Get the item details from the menu_item foreign key
    name = serializers.CharField(source="menu_item.name")
    category = serializers.CharField(source="menu_item.category")
    item_id = serializers.IntegerField(source="menu_item.id")

    class Meta:
        model = MenuItemsAssociation
        fields = ["item_id", "name", "category"]


class MenuSerializer(serializers.ModelSerializer):
    menu_items = serializers.SerializerMethodField()

    class Meta:
        model = Menus
        fields = ["id", "date", "meal_time", "meal_location", "menu_items"]

    def get_menu_items(self, menu):
        request = self.context.get("request")
        exclude_allergy_id = (
            request.query_params.get("exclude_allergy") if request else None
        )

        all_associations = MenuItemsAssociation.objects.filter(menu=menu)

        if exclude_allergy_id:
            menu_item_ids_with_allergy = MenuItemsAllergiesAssociation.objects.filter(
                allergy_id=exclude_allergy_id
            ).values_list("menu_item_id", flat=True)

            filtered_associations = all_associations.exclude(
                menu_item_id__in=menu_item_ids_with_allergy
            )
            associations = filtered_associations
        else:
            associations = all_associations

        return MenuItemInMenuSerializer(associations, many=True).data


class MenuBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = ["id", "date", "meal_time", "meal_location"]
