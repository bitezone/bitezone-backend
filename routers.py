from rest_framework import routers

from menu.viewsets import MenusViewSet, MenuItemsViewSet, MenuItemsAssociationViewSet


router = routers.SimpleRouter()

router.register(r"menu", MenusViewSet, basename="menu")
router.register(r"menu-items", MenuItemsViewSet, basename="menu-items")
router.register(r"associations", MenuItemsAssociationViewSet, basename="menu-association")

urlpatterns = router.urls
