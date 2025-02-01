
from .models import Category
#will return dictionary of all categories

def menu_links(request):
    links = Category.objects.all()
    return dict(categories=links)