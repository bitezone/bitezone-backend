from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Menus, MenuItems, MenuItemsAssociation
from .serializers import MenusSerializer, MenuItemsSerializer, MenuItemsAssociationSerializer


class MenusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving Menus.
    Includes a custom action 'items' to get associated MenuItems via MenuItemsAssociation.
    """
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """
        Returns all MenuItems for the given Menu.
        It does so by finding all MenuItemsAssociation entries for the menu,
        and then extracting the corresponding MenuItems.
        """
        menu = self.get_object()
        associations = MenuItemsAssociation.objects.filter(menu=menu)
        menu_items = [assoc.menu_item for assoc in associations]
        serializer = MenuItemsSerializer(menu_items, many=True)
        return Response(serializer.data)


class MenuItemsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving all MenuItems.
    """
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializer


class MenuItemsAssociationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving MenuItemsAssociation entries.
    """
    
    queryset = MenuItemsAssociation.objects.raw("SELECT * FROM menu_items_association")
    serializer_class = MenuItemsAssociationSerializer
