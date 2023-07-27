from django.urls import path
from . import views


urlpatterns = [

    path('', views.products, name='products'),
    path('<int:pro_id>', views.pro_child, name='pro_child'),
    path('<int:pro_id>/info/<int:chi_id>', views.product_info, name='product_info'),
    path('<int:pro_id>/info/<int:chi_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('search_result', views.search_result, name='search_result'),
    path('search', views.search, name='search'),

]
