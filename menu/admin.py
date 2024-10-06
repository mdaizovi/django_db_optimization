from django.contrib import admin

from .models import Condiment, Topping, Bun, Hotdog, SetMenu

admin.site.register(Condiment)
admin.site.register(Topping)
admin.site.register(Bun)
admin.site.register(Hotdog)
admin.site.register(SetMenu)
