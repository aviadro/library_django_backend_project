from django.urls import path
from . import views

urlpatterns = [
    path('', views.customers, name='customers'),
    path('register', views.register, name="register"),
    path('display_customers', views.display_customers, name="display_customers"),
    path('find_customer/<str:name>/',views.find_customer_by_name, name='find_customer_by_name'),
    path('remove_customer/<int:customer_id>/', views.remove_customer, name='remove_customer'),
    path('update_customer/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('customer/<int:customer_id>/', views.get_customer_by_id, name='get_customer_by_id'),

]
