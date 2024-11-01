from django.urls import path
from . import views

urlpatterns = [
    path('', views.customers, name='customers'),
    path('register', views.register, name="register"),
    path('display_customers', views.display_customers, name="display_customers"),

]
