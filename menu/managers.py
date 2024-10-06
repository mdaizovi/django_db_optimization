from django.db import models
from django.db.models import F
from .dtos import SetMenuDTO


class FoodManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class SetMenuManager(models.Manager):
    @staticmethod
    def _map_object(obj) -> SetMenuDTO:
        return SetMenuDTO(
            name=obj.name,
            vegan=obj.vegan,
            vegetarian=obj.vegetarian,
            glutenfree=obj.glutenfree,
            price_us=obj.price_us,
        )

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def low_price(self):
        return self.filter(price_us__lte=8).annotate(
            dto_name=F('name'),
            dto_price=F('price_us'),
            # Add other fields as needed
        ).values('dto_name', 'dto_price')


