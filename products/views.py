from os import name
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Child, Product
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def products(request):
    context = {
        'products': Product.objects.all()

    }

    return render(request, 'products/products.html', context)


def pro_child(request, pro_id):
    prochild = {
        'pchild': get_object_or_404(Product, pk=pro_id),
        'products': Product.objects.all(),
        'chil': Child.objects.all()

    }

    return render(request, 'products/pro_child.html',  prochild)


def product_info(request, pro_id, chi_id):
    pchild = get_object_or_404(Child, product__pk=pro_id, pk=chi_id)
    products = Product.objects.all()
    chil = Child.objects.all()

    return render(request, 'products/product_info.html', {'pchild': pchild, 'products': products, 'chil': chil})


def search_result(request):
    pro2 = Child.objects.all()
    pro5 = Product.objects.all()
    name = None
    code = None

    if 'searchname' in request.GET:
        name = request.GET['searchname']
        if name:
            pro2 = pro2.filter(name__icontains=name)

    if 'searchcode' in request.GET:
        code = request.GET['searchcode']
        if code:
            pro2 = pro2.filter(code__icontains=code)

    context3 = {
       
        'name': name,
        'code': code,
        'products2': pro2,
        'products': pro5,
        

    }
    return render(request, 'products/search_result.html', context3)


def search(request):
    pchild = {

        'products': Product.objects.all(),
    }

    return render(request, 'products/search.html', pchild)
