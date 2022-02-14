
from products.views import products
from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
from more.models import Work

# Import Pagination Stuff
from django.core.paginator import Paginator

# Create your views here.



def location(request):
    context = {
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

    
    return render(request, 'more/works.html', {'products':products, 'work':work, 'workl':workl, 'nums':nums})