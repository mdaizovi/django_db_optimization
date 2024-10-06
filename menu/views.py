from django.http import HttpResponse
from django.template import loader
from .models import SetMenu

APP_NAME = "menu"


def all_items(request):
    template = loader.get_template(f"{APP_NAME}/list.html")
    all_items = SetMenu.objects.all()
    low_price_items = SetMenu.objects.low_price()
    context = {"low_price": low_price_items, "all": all_items}
    return HttpResponse(template.render(context, request))
