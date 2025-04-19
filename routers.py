from rest_framework import routers

from menu.viewsets import MenuViewSet, MenuItemViewSet


router = routers.SimpleRouter()

router.register(r"menu", MenuViewSet, basename="menu")
router.register(r"menu-item", MenuItemViewSet, basename="menu-item")
urlpatterns = router.urls
