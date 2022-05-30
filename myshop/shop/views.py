from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic

from cart.forms import CartAddProductForm
from .forms import SearchForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None

    products = Product.objects.filter(available=True).order_by(
        get_order_by_products(request))

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'shop/product/list.html',
                  {'category': category, 'page': page, 'products': products})


def get_order_by_products(request):
    order_by = ''
    if request.GET.__contains__('sort') and request.GET.__contains__('up'):
        sort = request.GET['sort']
        up = request.GET['up']
        if sort == 'price' or sort == 'name':
            if up == '0':
                order_by = '-'
            order_by += sort
    if not order_by:
        order_by = '-created'
    return order_by


def delivery(request):
    return render(
        request,
        'shop/delivery.html'
    )


def contacts(request):
    return render(
        request,
        'shop/contacts.html'
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


# class ProductDetailView(generic.DetailView):
#     model = Product
#     cart_product_form = CartAddProductForm()
#
#     template_name = 'shop/product/detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#         context['products'] = Product.objects. \
#                                   filter(
#             category__exact=self.get_object().category). \
#                                   exclude(id=self.get_object().id).order_by(
#             '?')[:4]
#         return context


def handler404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    # result = prerender(request)
    # if result:
    #     return result
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(year__icontains=q) | Q(
                author__icontains=q) |
            Q(description__icontains=q)
        )
        # page = request.GET.get('page', 1)
        # paginator = Paginator(products, 4)
        # try:
        #     products = paginator.page(page)
        # except PageNotAnInteger:
        #     products = paginator.page(1)
        # except EmptyPage:
        #     products = paginator.page(paginator.num_pages)

        context = {'products': products, 'q': q}
        return render(
            request,
            'shop/search.html',
            context=context
        )
