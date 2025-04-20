from rest_framework import serializers
from .models import MealSession, MealItemEntry
from menu.models import MenuItems  # your actual menu item model


class MenuItemBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        fields = ["id", "name", "category", "serving_size", "calories_per_serving"]


class MealItemEntrySerializer(serializers.ModelSerializer):
    # Read-only detailed info
    menu_item = MenuItemBriefSerializer(read_only=True)

    # Write-only ID for creation
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItems.objects.all(), source="menu_item", write_only=True
    )

    class Meta:
        model = MealItemEntry
        fields = ["menu_item", "menu_item_id", "quantity"]


class MealSessionSerializer(serializers.ModelSerializer):
    meal_items = MealItemEntrySerializer(many=True)

    class Meta:
        model = MealSession
        fields = [
            "id",
            "date",
            "meal_time",
            "meal_location",
            "meal_items",
            "total_calories",
        ]
        read_only_fields = ["total_calories"]  # So user can't manually POST it

    def create(self, validated_data):
        """Payload example
                {
          "date": "2025-04-20T12:00:00Z",
          "meal_time": "lunch",
          "meal_location": "Lakeside",
          "meal_items": [
            { "menu_item_id": 5, "quantity": 2 },
            { "menu_item_id": 7, "quantity": 1 }
          ]
        }"""
        meal_items_data = validated_data.pop("meal_items")

        total = 0
        for item in meal_items_data:
            menu_item = item["menu_item"]
            quantity = item["quantity"]
            total += menu_item.calories_per_serving * quantity

        session = MealSession.objects.create(total_calories=total, **validated_data)

        for item_data in meal_items_data:
            MealItemEntry.objects.create(session=session, **item_data)

        return session
