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
    price_us = models.DecimalField(max_digits=5, decimal_places=2)

    objects = SetMenuManager()

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>: {self.name}"

    def _dietary_restriction_passes(
        self, restriction: Literal["vegan", "vegetarian", "glutenfree"]
    ) -> bool:
        for condiment in self.condiments.all():
            if getattr(condiment, restriction) is False:
                return False
        for topping in self.toppings.all():
            if getattr(topping, restriction) is False:
                return False
        if getattr(self.bun, restriction) is False:
            return False
        if getattr(self.hotdog, restriction) is False:
            return False
        return True

    @property
    def vegan(self) -> bool:
        return self._dietary_restriction_passes(restriction="vegan")

    @property
    def vegetarian(self) -> bool:
        return self._dietary_restriction_passes(restriction="vegetarian")

    @property
    def glutenfree(self) -> bool:
        return self._dietary_restriction_passes(restriction="glutenfree")
