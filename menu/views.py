from django.shortcuts import render
from .models import SetMenu
from django.db.models import Case, When, Value, BooleanField
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.conf import settings

APP_NAME = "menu"

def all_items(request):
    # Query 1: Fetch all items with an additional 'is_low_price' field
    all_items = SetMenu.objects.annotate(
        is_low_price=Case(
            When(price_us__lte=8, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).values('name', 'price_us', 'is_low_price')
    
    # Pagination
    paginator = Paginator(all_items, 20)  # Show 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Query 2: Count total items (needed for pagination)
    total_items = all_items.count()
    
    context = {
        "low_price": [item for item in page_obj if item['is_low_price']],
        "all": page_obj,
        "total_items": total_items
    }
    return render(request, f"{APP_NAME}/list.html", context)

# Apply cache only if not in testing mode
if not settings.TESTING:
    all_items = cache_page(60 * 15)(all_items)
