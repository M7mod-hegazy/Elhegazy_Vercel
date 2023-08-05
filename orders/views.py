from products.views import products
from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product, Child
from .models import Order, OrderDetails, Payment
from django.utils import timezone
import re
from django.http import JsonResponse


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


def remove_from_cart_ajax(request, orderdetails_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
            if orderdetails.order.user.id == request.user.id:
                orderdetails.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Unauthorized'})
                
        except OrderDetails.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order details not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)

        if orderdetails.order.user.id == request.user.id:
            orderdetails.quantity += 1
            orderdetails.save()

    return redirect('cart')


def add_qty_ajax(request, orderdetails_id):
    if request.user.is_authenticated and orderdetails_id:
        try:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id, order__user=request.user)
            orderdetails.quantity += 1
            orderdetails.save()

            response_data = {'success': True, 'new_quantity': orderdetails.quantity}
        except OrderDetails.DoesNotExist:
            response_data = {'success': False}
    else:
        response_data = {'success': False}

    return JsonResponse(response_data)


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            if orderdetails.order.user.id == request.user.id:
                orderdetails.quantity -= 1
                orderdetails.save()
        elif orderdetails.quantity == 1:
                orderdetails.delete()

    return redirect('cart')

def sub_qty_ajax(request, orderdetails_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            orderdetails = OrderDetails.objects.get(id=orderdetails_id)
            if orderdetails.quantity > 1:
                if orderdetails.order.user.id == request.user.id:
                    orderdetails.quantity -= 1
                    orderdetails.save()
            elif orderdetails.quantity == 1:
                orderdetails.delete()

            response_data = {'new_quantity': orderdetails.quantity}
        except OrderDetails.DoesNotExist:
            response_data = {'error': 'Order details not found'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request'})

def payment(request):
    context = {'products': Product.objects.all()}
    

    if request.method == 'POST' and 'payBtn' in request.POST:
  
        # هنا عملية الدفع بعد الضغط على الزر
        ship_address = None
        ship_phone = None
        is_added = None
        if 'ship_address' in request.POST:
             ship_address = request.POST['ship_address']
        else:
            messages.error(request, 'خطأ في عنوان التوصيل')
        if 'ship_phone' in request.POST:
             ship_phone = request.POST['ship_phone']
        else:
            messages.error(request, 'خطأ في رقم التلفون')    
        print(request.POST)
        if ship_phone and ship_address:
                if request.user.is_authenticated and not request.user.is_anonymous :
                    patt = "^01[0-2]\d{1,8}$"
                    if re.match(patt, ship_phone):
                        if Order.objects.all().filter(user=request.user, is_finished=False):
                            order = Order.objects.get(user=request.user, is_finished=False)
                            payment = Payment(order=order, shipment_address=ship_address, shipment_phone=ship_phone)
                            payment.save()
                            order.is_finished = True
                            order.save()
                            is_added = True
                            messages.success(request, 'تم تنفيز طلبك بنجاح')

                            context = {
                                'ship_address': ship_address,
                                'ship_phone': ship_phone,
                                'is_added': is_added,
                                'order': order,
                                'is_finished': True,
                                'products': Product.objects.all()
                            }
                    else:
                        messages.error(request, 'تحقق من رقم التلفون')
                        
            
        else:   
            messages.error(request, 'تحقق من الحقول الفارغه')
        

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                order.is_finished = False
                prototal = 0
                for prosup in orderdetails:
                    prototal += prosup.quantity
                context = {
                    'is_finished': False,
                    'is_added': False,
                    'order': order,
                    'orderdetails': orderdetails,
                    'prototal': prototal,
                    'products': Product.objects.all(),
                }    
                return render(request, 'orders/payment.html', context)   
                           

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
                    'prototal': prototal,
                    'total': total,
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
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            prototal = 0
            for prosup in orderdetails:
                prototal += prosup.quantity
    context = {
        'order': order,
        'prototal': prototal,
        'all_orders': all_orders,
        'products': Product.objects.all(),
        'total': total

    }
    return render(request, 'orders/show_orders.html', context)
