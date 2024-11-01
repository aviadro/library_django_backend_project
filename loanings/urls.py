from django.urls import path
from . import views

urlpatterns = [
    path('', views.loanings, name='loanings'),
    path('add_book', views.add_book, name='add_book'),
    path('loan_book', views.loan_book, name='loan_book'),
    path('return_book', views.return_book, name='return_book'),
    path('display_books', views.display_books, name='display_books'),
    path('display_loans', views.display_loans, name='display_loans'),
    path('customer/<int:customer_id>', views.display_customer_loans, name='display_customer_loans'),
    path('late_loans', views.display_late_loans, name='display_late_loans'),
    path('late_loans/<int:customer_id>', views.display_customer_late_loans, name='display_customer_late_loans'),
    path('find_book/<str:name>/', views.find_book_by_name, name='find_book_by_name'),
    path('remove_book/<int:book_id>/', views.remove_book, name='remove_book'),
    path('update_book/<int:book_id>/', views.update_book, name='update_book'),

]