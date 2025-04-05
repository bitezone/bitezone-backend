from rest_framework import serializers
from .models import MenuItems, MenuItemsAssociation, Menus

class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        fields = '__all__'


class MenuItemsAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemsAssociation
        fields = '__all__'


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = '__all__'
