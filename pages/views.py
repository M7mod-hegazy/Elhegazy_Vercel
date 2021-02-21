from pages.models import Slider, Slider2, Slider3
from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product

# Create your views here.


def index(request):
    myslyder = {
        'sliders': Slider.objects.all(),
        'sliders2': Slider2.objects.all(),
        'sliders3': Slider3.objects.all(),
        'products': Product.objects.all()


    }
    return render(request, 'pages/index.html', myslyder)


def location(request):
    context = {
        'products': Product.objects.all()

    }
    return render(request, 'pages/location.html', context)
