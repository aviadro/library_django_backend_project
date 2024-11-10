from rest_framework import serializers

from customers.serializers import CustomerSerializer
from loanings.models import Book, Loan

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(source='book_id', read_only=True)
    customer = CustomerSerializer (source='cust_id', read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'