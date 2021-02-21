from django.shortcuts import render, redirect
from products.models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
# Create your views here.


def signin(request):
    product = Product.objects.all()

    return render(request, 'accounts/signin.html', {'products': product})


def signup(request):
    product = Product.objects.all()
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')

    return render(request, 'accounts/signup.html', {'form': form, 'products': product})


def profile(request):
    context = {
        'products': Product.objects.all()

    }

    return render(request, 'accounts/profile.html', context)
