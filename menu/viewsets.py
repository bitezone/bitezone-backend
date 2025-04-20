from rest_framework import viewsets
from .models import MenuItems, Menus, Allergies
from .serializers import (
    MenuItemNutritionSerializer,
    MenuSerializer,
    MenuBasicSerializer,
    AllergySerializer
)
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.dateparse import parse_datetime


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving menus with their associated menu items.
    """

    permission_classes = [AllowAny]

    queryset = Menus.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = Menus.objects.all()
        date_str = self.request.query_params.get("date", None)
        meal_time = self.request.query_params.get("meal_time", None)
        meal_location = self.request.query_params.get("meal_location", None)

        if date_str:
            parsed_date = parse_datetime(date_str)
            if not parsed_date:
                raise ValidationError(
                    {
                        "error": "Invalid date format. Use ISO 8601 format: 'YYYY-MM-DDTHH:MM:SSZ'"
                    }
                )
            queryset = queryset.filter(date=parsed_date.date())

        if meal_time:
            valid_menu_times = (
                Menus.objects.order_by("meal_time")
                .values_list("meal_time", flat=True)
                .distinct()
            )
            if meal_time.lower() not in [val.lower() for val in valid_menu_times]:
                raise ValidationError(
                    {
                        "error",
                        "Invalid menu time. Please select only from the following-"
                        + ", ".join(valid_menu_times),
                    }
                )
            queryset = queryset.filter(meal_time__iexact=meal_time)

        if meal_location:
            valid_meal_locations = (
                Menus.objects.order_by("meal_location")
                .values_list("meal_location", flat=True)
                .distinct()
            )

            found_location = None
            for location in valid_meal_locations:
                if meal_location.lower() == location.lower():
                    found_location = location
                    break

            if not found_location:
                raise ValidationError(
                    {
                        "error",
                        "Invalid menu location. Please select only from the following-"
                        + ", ".join(valid_meal_locations),
                    }
                )
            queryset = queryset.filter(meal_location=found_location)

        return queryset

    @action(detail=False, methods=["get"])
    def get_menu_times(self, request):
        date_str = request.query_params.get("date", None)
        meal_location = self.request.query_params.get("meal_location", None)
        menus = Menus.objects.all()
        if not date_str:
            return Response({"error": "Date parameter is required"}, status=400)

        parsed_date = parse_datetime(date_str)
        if not parsed_date:
            return Response(
                {
                    "error": "Invalid date format. Use ISO 8601 format: 'YYYY-MM-DDTHH:MM:SSZ'"
                },
                status=400,
            )

        # Filter menus by the parsed date
        menus = menus.filter(date__date=parsed_date.date())

        if not meal_location:
            return Response(
                {"error": "Meal Location parameter is required"}, status=400
            )

        valid_meal_locations = (
            Menus.objects.order_by("meal_location")
            .values_list("meal_location", flat=True)
            .distinct()
        )

        found_location = None
        for location in valid_meal_locations:
            if meal_location.lower() == location.lower():
                found_location = location
                break

        menus = menus.filter(meal_location=found_location)

        serializer = MenuBasicSerializer(menus, many=True)

        return Response(serializer.data)


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows menu items to be viewed.
    """

    permission_classes = [AllowAny]
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemNutritionSerializer

class AllergyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Allergies.objects.all()
    serializer_class = AllergySerializer