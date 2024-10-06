from django.db import models
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
        return [
            self._map_object(x) for x in self.get_queryset().filter(price_us__lte=8)
        ]
