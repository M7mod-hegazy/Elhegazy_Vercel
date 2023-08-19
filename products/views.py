from math import ceil, floor
from multiprocessing import context
from os import name
from pickle import NONE
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime
from .models import Child, Product
from orders.models import Order, OrderDetails
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import UserProfile
from django.contrib.postgres.search import SearchVector
import qrcode
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Min, Max





# Import Pagination Stuff
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def products(request):
    context = {
        'products': Product.objects.all()

    }
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            prototal = 0
            for prosup in orderdetails:
                prototal += prosup.quantity
            context = {
                'order': order,
                'prototal': prototal,
                'products': Product.objects.all()
            }
    return render(request, 'products/products.html', context)


def pro_child(request, pro_id):
    chil_count = 0
    price_from = None
    price_to = None
    sort_param = None
    sort_param = request.GET.get('sort')
    price_from = request.GET.get('searchPriceFrom')
    price_to = request.GET.get('searchPriceTo')
    chil = Child.objects.all().filter(product__pk=pro_id, is_active=True)
    max_price = Child.objects.filter(product__pk=pro_id, is_active=True).aggregate(max_price=Max('price'))['max_price']
    min_price = Child.objects.filter(product__pk=pro_id, is_active=True).aggregate(min_price=Min('price'))['min_price']
    if ('AtoZ' in request.GET):
        sort_param = 'AtoZ'
        chil = chil.order_by('name')
    elif ('ZtoA' in request.GET): 
        sort_param = 'ZtoA' 
        chil = chil.order_by('-name')
    elif ('priceUP' in request.GET): 
        sort_param = 'priceUP' 
        chil = chil.order_by('price')
    elif ('priceDown' in request.GET): 
        sort_param = 'priceDown' 
        chil = chil.order_by('-price')
    elif ('dateUP' in request.GET):  
        sort_param = 'dateUP'
        chil = chil.order_by('publish_date')
    elif ('dateDown' in request.GET): 
        sort_param = 'dateDown' 
        chil = chil.order_by('-publish_date') 
    elif sort_param == 'AtoZ':
        chil = chil.order_by('name')
    elif sort_param == 'ZtoA':
        chil = chil.order_by('-name')
    elif sort_param == 'priceUP':
        chil = chil.order_by('price')
    elif sort_param == 'priceDown':
        chil = chil.order_by('-price')
    elif sort_param == 'dateUP':
        chil = chil.order_by('publish_date')
    elif sort_param == 'dateDown':
        chil = chil.order_by('-publish_date')            
    # Apply price range filtering

    
    if "searchPriceFrom" in request.GET and "searchPriceTo" in request.GET:
        price_from = request.GET['searchPriceFrom']
        price_to = request.GET['searchPriceTo']

        if price_from and price_to:
            if price_from.isdigit() and price_to.isdigit():
                chil = chil.filter(price__gte=price_from,  price__lte=price_to)

    # Filtering by child name if searchChildName is provided
    search_child_name = request.GET.get('searchChildName')
    if search_child_name:
        chil = chil.filter(Q(name__icontains=search_child_name))

    chil_count = chil.count    
    pchild = get_object_or_404(Product, pk=pro_id)
    product = Product.objects.all().prefetch_related('childs')
    p = Paginator(chil, 12)
    page = request.GET.get('page')
    prol = p.get_page(page)
    nums = "a" * prol.paginator.num_pages
    prochild = {
        'pchild': get_object_or_404(Product, pk=pro_id),
        'products': Product.objects.all(),
        'chil': Child.objects.all(),
        'prol': prol, 
        'nums': nums,
        'price_from':price_from,
        'price_To':price_to,
        'max_price': ceil(max_price),
        'min_price': floor(min_price),
        'chil_count': chil_count,
        'sort_param': sort_param

    }
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            prototal = 0
            for prosup in orderdetails:
                prototal += prosup.quantity
                
            prochild = {
                'order': order,
                'prototal': prototal,
                'products': Product.objects.all(),
                'pchild': get_object_or_404(Product, pk=pro_id),
                'products': Product.objects.all(),
                'chil': Child.objects.all(),
                'sort_param': sort_param,
                'price_from':price_from,
                'price_To':price_to,
                'prol': prol,
                'max_price': ceil(max_price),
                'min_price': floor(min_price),
                'chil_count': chil_count,
                'nums': nums
            }

    return render(request, 'products/pro_child.html',  prochild)


def product_info(request, pro_id, chi_id):
    pchild = get_object_or_404(Child, product__pk=pro_id, pk=chi_id)
    related_children = Child.objects.filter(
        Q(product__pk=pro_id) & ~Q(pk=chi_id)
    )
    pro5 = Product.objects.all()

    if request.user.is_authenticated and not request.user.is_anonymous:
        userprofile = UserProfile.objects.get(user=request.user)
        if Order.objects.filter(user=request.user, is_finished=False).exists():
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.filter(order=order)
            prototal = sum(prosup.quantity for prosup in orderdetails)
            return render(request, 'products/product_info.html', context={
                'pchild': pchild,
                'userprofile': userprofile,
                'order': order,
                'prototal': prototal,
                'products': pro5,
                'related_children': related_children,
            })
        else:
            return render(request, 'products/product_info.html', context={
                'pchild': pchild,
                'products': pro5,
                'related_children': related_children,
            })
    else:
        return render(request, 'products/product_info.html', context={
            'pchild': pchild,
            'products': pro5,
            'related_children': related_children,
        })


def search_result(request):
    pro2 = Child.objects.all()
    pro5 = Product.objects.all()
    name = None
    code = None
    details = None
    seens = None
    p = None
    page = None
    prol = None
    query_string = None

    if 'searchname' in request.GET and request.GET['searchname'].strip():
        query_string = request.GET.get('searchname')
        search_query = Q(name__icontains=query_string) | Q(code__icontains=query_string) | Q(details__icontains=query_string)
        seens = Child.objects.filter(search_query, is_active=True)
        
        page = request.GET.get('page')
        paginator = Paginator(seens, 12)
        try:  
            p = paginator.page(page)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)
        
        prol = seens.count()

        context3 = {
            'name': name,
            'code': code,
            'details': details,
            'products2': pro2,
            'products': pro5,
            'prol': prol,
            'p': p,
            'seens': seens,
            'query_string': query_string
        }
    else:   
        context3 = {
            'name': name,
            'code': code,
            'details': details,
            'products2': pro2,
            'products': pro5,
            'prol': prol,
            'p': p,
            'seens': seens, 
            'query_string': query_string
        }

    # if request.user.is_authenticated and not request.user.is_anonymous:
    #     if Order.objects.all().filter(user=request.user, is_finished=False):
    #         order = Order.objects.get(user=request.user, is_finished=False)
    #         orderdetails = OrderDetails.objects.all().filter(order=order)
    #         prototal = 0
    #         for prosup in orderdetails:
    #             prototal += prosup.quantity
    #         context3 = {
    #             'order': order,
    #             'prototal': prototal,
    #             'name': name,
    #             'code': code,
    #             'details': details,
    #             'products2': pro2,
    #             'products': pro5,
    #             'prol': prol,
    #             'seens': seens,
    #             'query_string': query_string
    #         }    

    return render(request, 'products/search_result.html', context3)


def search(request):
    pchild = {

        'products': Product.objects.all(),
    }

    return render(request, 'products/search.html', pchild)



def generate_qr_code(request, pro_id, chi_id):
    # Construct the complete URL manually without using build_absolute_uri
    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()
    path = request.path

    complete_url = f"{protocol}://{domain}{path}"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(complete_url)
    qr.make(fit=True)

    # Create an image from the QR code data
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a BytesIO buffer to return it as a response
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def generate_qr_code2(request, pro_id):
    # Construct the complete URL manually without using build_absolute_uri
    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()
    path = request.path

    complete_url = f"{protocol}://{domain}{path}"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(complete_url)
    qr.make(fit=True)

    # Create an image from the QR code data
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a BytesIO buffer to return it as a response
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def product_favorite_pro_child(request):
    if request.method == 'POST' and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.POST.get('pro_id')
        chi_id = request.POST.get('chi_id')
        pchild = get_object_or_404(Child, product__pk=pro_id, pk=chi_id)

        if request.user.is_authenticated and not request.user.is_anonymous:
            pro_fav = Child.objects.get(product__pk=pro_id, pk=chi_id)

            userprofile = UserProfile.objects.get(user=request.user)
            if pro_fav in userprofile.product_favorites.all():
                userprofile.product_favorites.remove(pro_fav)
                message = 'تم مسح المنتج من المفضله بنجاح'
                is_favorite = False
            else:
                userprofile.product_favorites.add(pro_fav)
                message = 'تم إضافة المنتج للمفضله بنجاح'
                is_favorite = True

            return JsonResponse({'message': message, 'is_favorite': is_favorite})
        else:
            return JsonResponse({'message': 'يجب ان تسجل الدخول أولا'}, status=403)
    elif not request.user.is_authenticated:
        return JsonResponse({'message': 'يجب ان تسجل الدخول أولا'}, status=403)
    # If the request method is not POST or the user is not authenticated
    return JsonResponse({'message': 'Bad Request'}, status=400)


