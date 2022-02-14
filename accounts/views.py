
from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from products.models import Product, Child
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages, auth
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import UserProfile
import re
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def signin(request):
    product = Product.objects.all()
    if request.method == 'POST' and 'btnlogin' in request.POST:
        username = request.POST['username']
        password = request.POST['password1']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)

        else:
            messages.error(request, 'خطأ في اسم المسخدم او البريد الإلكتروني')
        return redirect('signin')
    else:
        return render(request, 'accounts/signin.html', {'products': product})


def signup(request):
    product = Product.objects.all()

    if request.method == 'POST' and 'btnsignup' in request.POST:
        # variables for fields
        fname = None
        lname = None
        email = None
        username = None
        password1 = None
        password2 = None
        address = None
        phone = None
        terms = None
        is_added = None

        # GET values from the form
        if 'fname' in request.POST:
            fname = request.POST['fname']
        else:
            messages.error(request, 'خطأ في الاسم الأول')
        if 'lname' in request.POST:
            lname = request.POST['lname']
        else:
            messages.error(request, 'خطأ في الاسم الثاني')
        if 'email' in request.POST:
            email = request.POST['email']
        else:
            messages.error(request, 'خطأ في البريد الإلكتروني')
        if 'username' in request.POST:
            username = request.POST['username']
        else:
            messages.error(request, 'خطأ في اسم المستخدم')
        if 'password1' in request.POST:
            password1 = request.POST['password1']
        else:
            messages.error(request, 'خطأ في كلمة السر')
        if 'password2' in request.POST:
            password2 = request.POST['password2']
        else:
            messages.error(request, 'خطأ في كلمة السر')
        if 'address' in request.POST:
            address = request.POST['address']
        else:
            messages.error(request, 'خطأ في العنوان ')
        if 'phone' in request.POST:
            phone = request.POST['phone']
        else:
            messages.error(request, 'خطأ في رقم الهاتف')
        if 'terms' in request.POST:
            terms = request.POST['terms']
        # check values
        if fname and lname and address and phone and email and password1 and password2 and username:
            if terms == 'on':
                # ckeck if username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'اسم المستخدم هذا مستخدم من قبل')
                else:
                    # check if email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(
                            request, ' البريد الإلكتروني هذا مستخدم من قبل')
                    else:
                        patt = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                        patt2 = '^.{8,32}$'
                        if re.match(patt, email):
                            if password1 == password2:
                                if re.match(patt2, password1):
                                    # add user
                                    user = User.objects.create_user(
                                        first_name=fname, last_name=lname, email=email, username=username, password=password1)
                                    user.save()
                                    # add user peofile
                                    userprofile = UserProfile(
                                        user=user, address=address, tell=phone)
                                    userprofile.save()
                                    # clear fields
                                    fname = ''
                                    lname = ''
                                    email = ''
                                    password1 = ''
                                    password2 = ''
                                    address = ''
                                    phone = ''
                                    username = ''
                                    terms = None

                                    # success messages
                                    messages.success(
                                        request, 'تم إنشاء حسابك بنجاح')
                                    is_added = True
                                else:
                                    messages.error(
                                        request, 'يجب أ ن تزيد كلمة السر عن 8 أرقام او أحرف')
                            else:
                                messages.error(
                                    request, ' تأكيد كلمة السر بها خطأ ')
                        else:
                            messages.error(request, 'خطأ في البريد اللإلكروني')
            else:
                messages.error(request, 'يجب ان توافق على شروط الإستخدام')

        else:
            messages.error(request, 'تحقق من الحقول الفارغه')
        return render(request, 'accounts/signup.html', {'products': product, 'fname': fname, 'lname': lname, 'address': address, 'phone': phone, 'email': email, 'password1': password1, 'password2': password2, 'username': username, 'is_added': is_added})
    else:
        return render(request, 'accounts/signup.html', {'products': product})


def profile(request):

    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                patt2 = '^.{8,32}$'
                if re.match(patt2, password1):
                    if request.POST['fname'] and request.POST['lname'] and request.POST['email'] and request.POST['password1'] and request.POST['password2'] and request.POST['address'] and request.POST['phone']:
                        request.user.first_name = request.POST['fname']
                        request.user.last_name = request.POST['lname']
                        #request.user.email = request.POST['email']
                        #request.user.username = request.POST['username']
                        userprofile.address = request.POST['address']
                        userprofile.tell = request.POST['phone']
                        if not request.POST['password1'].startswith('pbkdf2_sha256$'):
                            request.user.set_password(
                                request.POST['password1'])
                        request.user.save()
                        userprofile.save()
                        auth.login(request, request.user)
                        messages.success(request, 'تم تحديث البيانات بنجاح')

                    else:
                        messages.error(request, 'هناك خطأ في القيم')

                else:
                    messages.error(
                        request, 'يجب أ ن تزيد كلمة السر عن 8 أرقام او أحرف')
            else:
                messages.error(request, ' تأكيد كلمة السر بها خطأ ')
        return redirect('profile')
    else:

        if request.user is not None:
            context = {
                'products': Product.objects.all(),
            }
            if not request.user.is_anonymous:
                userprofile = UserProfile.objects.get(user=request.user)
                context = {
                    'products': Product.objects.all(),
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,
                    'email': request.user.email,
                    'username': request.user.username,
                    'password': request.user.password,
                    'address': userprofile.address,
                    'phone': userprofile.tell

                }

            return render(request, 'accounts/profile.html', context)
        else:
            return redirect('profile')


def product_favorite(request, pro_id, chi_id):
    pchild = get_object_or_404(Child, product__pk=pro_id, pk=chi_id)
    products = Product.objects.all()
    chil = Child.objects.all()
    if request.user.is_authenticated and not request.user.is_anonymous:

        pro_fav = Child.objects.get(product__pk=pro_id, pk=chi_id)

        if UserProfile.objects.filter(user=request.user, product_favorites=pro_fav).exists():
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.remove(pro_fav)
            messages.error(request, 'تم مسح المنتج من المفضله بنجاح ')
            return redirect('/products/' + str(pro_id) + '/info/' + str(chi_id))
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.info(request, 'تم إضافة المنتج للمفضله بنجاح')
            return redirect('/products/' + str(pro_id) + '/info/' + str(chi_id))
    else:
        messages.error(request, 'يجب ان تسجل الدخول أولا')
        return redirect('/products/' + str(pro_id) + '/info/' + str(chi_id))


def show_product_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        pro5 = Product.objects.all()
        p= Paginator(Child.objects.all(), 6)
        page = request.GET.get('page')
        prol2 = p.get_page(page)
        nums = "a" * prol2.paginator.num_pages

        context = {'prol':pro, 'products':pro5, 'prol2':prol2}
    return render(request, 'products/favorite.html', context)    
