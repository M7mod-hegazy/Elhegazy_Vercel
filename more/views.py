
from products.views import products
from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
from more.models import Work
from orders.models import Order, OrderDetails
from accounts.models import UserProfile



# Import Pagination Stuff
from django.core.paginator import Paginator

# Create your views here.



def location(request):
      context = {
        'products': Product.objects.all()

      }
      if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context = {
              'prol_fav':pro,
              'prol_count':pro.count, 
              'products': Product.objects.all()
           }
        if Order.objects.all().filter(user=request.user, is_finished=False):
            userInfo = UserProfile.objects.get(user=request.user)
            pro = userInfo.product_favorites.all()
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            prototal = 0
            for prosup in orderdetails:
                prototal += prosup.quantity
            context = {
              'prol_fav':pro,
              'prol_count':pro.count,
              'order': order,
              'prototal': prototal, 
              'products': Product.objects.all()

           }
      return render(request, 'more/location.html', context)

def works(request):
  
    products = Product.objects.all()
    work = Work.objects.all()
    # Set up Pagination
    p= Paginator(Work.objects.all(), 3)
    page = request.GET.get('page')
    workl = p.get_page(page)
    nums = "a" * workl.paginator.num_pages
    context = {
     'products':products,
     'work':work,
     'workl':workl,
     'nums':nums
    }
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context = {
              'prol_fav':pro,
              'prol_count':pro.count,
              'products':products,
              'work':work,
              'workl':workl,
              'nums':nums
            }
        if Order.objects.all().filter(user=request.user, is_finished=False):
            userInfo = UserProfile.objects.get(user=request.user)
            pro = userInfo.product_favorites.all()
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            prototal = 0
            for prosup in orderdetails:
                prototal += prosup.quantity
            context = {
              'prol_fav':pro,
              'prol_count':pro.count,
              'order': order,
              'prototal': prototal, 
              'products':products,
              'work':work,
              'workl':workl,
              'nums':nums
            }
    
    return render(request, 'more/works.html', context)