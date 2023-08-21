from .models import Myslider, Mysection
from orders.models import Order, OrderDetails
from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product, Child
from accounts.models import UserProfile


# Create your views here.

def index(request):
     chilSale = Child.objects.all().exclude(oldPrice__exact='')
     myslyder = {
        'mysliders': Myslider.objects.all(),
        'products': Product.objects.all(),
        'mysections': Mysection.objects.all(),
        'chil': Child.objects.all(),
        'chil2': chilSale,

     }
     if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        myslyder = {
                'prol_fav':pro,
                'prol_count':pro.count,
                'mysliders': Myslider.objects.all(),
                'products': Product.objects.all(),
                'mysections': Mysection.objects.all(),
                'chil': Child.objects.all(),
                'chil2': chilSale,
            }
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            prototal = 0
            for prosup in orderdetails:
                prototal += prosup.quantity
            myslyder = {
                'prol_fav':pro,
                'prol_count':pro.count,
                'order': order,
                'prototal': prototal,
                'mysliders': Myslider.objects.all(),
                'products': Product.objects.all(),
                'mysections': Mysection.objects.all(),
                'chil': Child.objects.all(),
                'chil2': chilSale,
            }
     return render(request, 'pages/index.html', myslyder)