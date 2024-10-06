from django.shortcuts import render
from .models import SetMenu
from django.db.models import F
from django.utils.timeit import timeit
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

APP_NAME = "menu"

@timeit
@cache_page(60 * 15)  # Cache for 15 minutes
def all_items(request):
    all_items = SetMenu.objects.values('name', 'price_us')
    
    # Pagination
    paginator = Paginator(all_items, 20)  # Show 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "low_price": all_items.filter(price_us__lte=8),
        "all": page_obj
    }
    return render(request, f"{APP_NAME}/list.html", context)
