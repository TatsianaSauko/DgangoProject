from .forms import SearchForm
from .models import Category


def add_default_data(request):
    categories = Category.objects.all()
    search_form = SearchForm()
    return {'categories': categories, 'search_form': search_form}
