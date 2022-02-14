from os import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('profile', views.profile, name='profile'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html'), name='change_password'),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/change_password_done.html'), name='password_change_done'),
    path('<int:pro_id>/pro_fav/<int:chi_id>',
         views.product_favorite, name='product_favorite'),
    path('show_product_favorite', views.show_product_favorite, name='show_product_favorite')

]
