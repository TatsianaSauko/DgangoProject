from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
import weasyprint


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.need_delivery = True if form.cleaned_data['delivery'] == 1 else False
            order.save()
            add_user(form.cleaned_data['first_name'], form.cleaned_data['email'])
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])

            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {'name': request.user.first_name,
                       'email': request.user.email}
        form = OrderCreateForm(initial=initial)
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response


def add_user(name, email):
    if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
        return
    password = User.objects.make_random_password()
    user = User.objects.create_user(email, email, password)
    user.first_name = name
    group = Group.objects.get(name='Клиенты')
    user.groups.add(group)
    user.save()

    text = get_template('registration/registration_email.html')
    html = get_template('registration/registration_email.html')

    context = {'username': email, 'password': password}

    subject = 'Регистрация'
    from_email = 'from@booksite.by'
    text_content = text.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@login_required
def orders(request):
    user_orders = Order.objects.filter(email__exact=request.user.email)
    return render(
        request,
        'orders/order/orders.html',
        context={'orders': user_orders}
    )


@permission_required('orders.can_set_status')
def cancelorder(request, order_id):
    print(request.user.has_perm('orders.can_set_status'))
    order = get_object_or_404(Order, id=order_id)
    if order.email == request.user.email and order.status == 'NEW':
        order.status = 'CNL'
        order.save()
    return HttpResponseRedirect(reverse('orders:orders'))
