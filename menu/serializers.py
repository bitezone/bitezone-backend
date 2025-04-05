
from rest_framework import serializers
from .models import MenuItems, Menus, MenuItemsAssociation

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        fields = ['id', 'name', 'category']

class MenuItemInMenuSerializer(serializers.ModelSerializer):
    # Get the item details from the menu_item foreign key
    name = serializers.CharField(source='menu_item.name')
    category = serializers.CharField(source='menu_item.category')
    item_id = serializers.IntegerField(source='menu_item.id')
    
    class Meta:
        model = MenuItemsAssociation
        fields = ['item_id', 'name', 'category']

class MenuSerializer(serializers.ModelSerializer):
    menu_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Menus
        fields = ['id', 'date', 'meal_time', 'meal_location', 'menu_items']
    
    def get_menu_items(self, menu):
        # Get all associations for this menu
        associations = MenuItemsAssociation.objects.filter(menu=menu)
        # Use the serializer that includes item details
        return MenuItemInMenuSerializer(associations, many=True).data