from django.urls import path
from . import views

urlpatterns = [
    path('', views.loanings, name='loanings'),
    path('add_book', views.add_book, name='add_book'),
    
]