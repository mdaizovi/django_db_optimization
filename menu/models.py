from typing import Literal
from django.db import models
from .managers import FoodManager, SetMenuManager


class FoodItem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    vegan = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    glutenfree = models.BooleanField(default=False)

    objects = FoodManager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>: {self.name}"

    def natural_key(self) -> str:
        return self.name


class Condiment(FoodItem):
    pass

    class Meta:
        ordering = ("name",)


class Topping(FoodItem):
    pass

    class Meta:
        ordering = ("name",)


class Bun(FoodItem):
    pass

    class Meta:
        ordering = ("name",)


class Hotdog(FoodItem):
    length_cm = models.FloatField(default=15.24)

    class Meta:
        ordering = ("name",)


class SetMenu(models.Model):
    name = models.CharField(max_length=200)
    hotdog = models.ForeignKey(Hotdog, on_delete=models.CASCADE)
    condiments = models.ManyToManyField(Condiment, blank=True)
    toppings = models.ManyToManyField(Topping, blank=True)
    bun = models.ForeignKey(Bun, on_delete=models.CASCADE)
    price_us = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)

    objects = SetMenuManager()

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>: {self.name}"

    def _dietary_restriction_passes(
        self, restriction: Literal["vegan", "vegetarian", "glutenfree"]
    ) -> bool:
        return all(
            getattr(item, restriction)
            for item in [self.bun, self.hotdog] + list(self.condiments.all()) + list(self.toppings.all())
        )

    @property
    def vegan(self) -> bool:
        return self._dietary_restriction_passes(restriction="vegan")

    @property
    def vegetarian(self) -> bool:
        return self._dietary_restriction_passes(restriction="vegetarian")

    @property
    def glutenfree(self) -> bool:
        return self._dietary_restriction_passes(restriction="glutenfree")
