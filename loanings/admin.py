from django.contrib import admin

from loanings.models import Book, Loan

admin.site.register(Book)
admin.site.register(Loan)