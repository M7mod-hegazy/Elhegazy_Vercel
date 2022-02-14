from .models import Myslider, Mysection
from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product


# Create your views here.


def index(request):


    myslyder = {
        'mysliders': Myslider.objects.all(),
        'products': Product.objects.all(),
        'mysections': Mysection.objects.all(),

        
     

    }
    return render(request, 'pages/index.html', myslyder)


