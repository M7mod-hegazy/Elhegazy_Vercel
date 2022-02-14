from products.views import products
from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product, Child
from .models import Order, OrderDetails, Payment
from django.utils import timezone

# Create your views here.


def add_to_cart(request):
    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and 'code' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        code = request.GET['code']
        order = Order.objects.all().filter(user=request.user, is_finished=False)

        if not Child.objects.all().filter(id=pro_id).exists():
            return redirect('/products/' + request.GET['father'] + '/info/' + request.GET['pro_id'])

        pro = Child.objects.get(id=pro_id)

        if order:
            messages.success(request, 'تمت إضافة المنتج الى السله')
            old_order = Order.objects.get(user=request.user, is_finished=False)
            if OrderDetails.objects.all().filter(order=old_order, product=pro).exists():
                orderdetails = OrderDetails.objects.get(
                    order=old_order, product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else:
                orderdetails = OrderDetails.objects.create(
                    product=pro, order=old_order, price=pro.price, code=pro.code, quantity=qty)
        else:
            messages.success(request, 'تم إنشاء سله و إضافة طلبك')
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            order_details = OrderDetails.objects.create(
                product=pro, order=new_order, price=pro.price, code=pro.code, quantity=qty)

        return redirect('/products/' + request.GET['father'] + '/info/' + request.GET['pro_id'])
    else:
        if 'pro_id' in request.GET:
            messages.error(request, 'يجب تسجيل الدخول لأستخدام هذه الخدمه')
            return redirect('/products/' + request.GET['father'] + '/info/' + request.GET['pro_id'])
        else:
            return redirect('index')


def cart(request):
    context = {
        'products': Product.objects.all()
    }
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total = 0
            prototal = 0
            for sup in orderdetails:
                total += sup.price * sup.quantity
            for prosup in orderdetails:
                prototal += prosup.quantity
            context = {
                'order': order,
                'orderdetails': orderdetails,
                'total': total,
                'prototal': prototal,
                'products': Product.objects.all(),

            }
    return render(request, 'orders/cart.html', context)


def remove_from_cart(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.delete()

    return redirect('cart')


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)

        if orderdetails.order.user.id == request.user.id:
            orderdetails.quantity += 1
            orderdetails.save()

    return redirect('cart')


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            if orderdetails.order.user.id == request.user.id:
                orderdetails.quantity -= 1
                orderdetails.save()

    return redirect('cart')


def payment(request):
    context = {'products': Product.objects.all()}
    ship_address = None
    ship_phone = None
    card_number = None
    card_name = None
    expire = None
    security_code = None
    is_added = None

    if request.method == 'POST' and 'btnpayment' in request.POST and 'ship_address' in request.POST and 'ship_phone' in request.POST and 'card_number' in request.POST and 'card_name' in request.POST and 'expire' in request.POST and 'security_code' in request.POST:

        # هنا عملية الدفع بعد الضغط على الزر
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        card_name = request.POST['card_name']
        expire = request.POST['expire']
        security_code = request.POST['security_code']

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                payment = Payment(order=order, shipment_address=ship_address, shipment_phone=ship_phone,
                                  card_number=card_number, card_name=card_name, expire=expire, security_code=security_code)
                payment.save()
                order.is_finished = True
                order.save()
                is_added = True
                messages.success(request, 'تم تنفيز طلبك بنجاح')

            context = {
                'ship_address': ship_address,
                'ship_phone': ship_phone,
                'card_number': card_number,
                'card_name': card_name,
                'expire': expire,
                'security_code': security_code,
                'is_added': is_added,
                'products': Product.objects.all()
            }
    else:
        # هنا العرض قبل الضغط على الدفع
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                prototal = 0
                for sup in orderdetails:
                    total += sup.price * sup.quantity
                for prosup in orderdetails:
                    prototal += prosup.quantity
                context = {
                    'order': order,
                    'orderdetails': orderdetails,
                    'total': total,
                    'prototal': prototal,
                    'products': Product.objects.all(),

                }

    return render(request, 'orders/payment.html', context)


def show_orders(request):
    context = {'products': Product.objects.all()}
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.get(id=x.id)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                prototal = 0
                for sup in orderdetails:
                    total += sup.price * sup.quantity
                x.total = total
                x.items_count = orderdetails.count

    context = {
        'all_orders': all_orders,
        'products': Product.objects.all(),
        'total': total

    }
    return render(request, 'orders/show_orders.html', context)
