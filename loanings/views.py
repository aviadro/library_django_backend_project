from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from customers.models import Customer
from loanings.models import Book, Loan
from loanings.serializers import BookSerializer


def welcome(request):
    return HttpResponse("Welcome to the library!")

def loanings(request):
    return HttpResponse("Welcome to loanings!")

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loan_book(request):
    try:
        # Retrieve book_id and customer_id from the request
        book_id = request.data.get('book_id')
        customer_id = request.data.get('customer_id')

        # Ensure the authenticated user is either the customer making the loan or an admin
        if not request.user.is_staff and request.user.id != customer_id:
            return Response({"error": "Not authorized to loan this book"}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the book and customer instances
        book = Book.objects.get(id=book_id)
        customer = Customer.objects.get(id=customer_id)

        # Ensure the book is available for loan
        if not book.isActive:
            return Response({"error": "This book is not available for loan"}, status=status.HTTP_400_BAD_REQUEST)

        if book.book_type == 1:
            due_date = timezone.now() + timezone.timedelta(days=10) 
        elif book.book_type == 2:
            due_date = timezone.now() + timezone.timedelta(days=5) 
        if book.book_type == 3:
            due_date = timezone.now() + timezone.timedelta(days=2) 

        # Create the loan
        loan = Loan.objects.create(
            book_id=book,
            cust_id=customer,
            loan_date=timezone.now(),
            due_date=due_date
            is_active=True
        )

        # Update book availability
        book.isActive = False
        book.save()

        return Response({"message": "Book loaned successfully", "loan_id": loan.id}, status=status.HTTP_201_CREATED)

    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
