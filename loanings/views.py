from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from customers.models import Customer
from loanings.models import Book, Loan
from loanings.serializers import BookSerializer, LoanSerializer


def welcome(request):
    return HttpResponse("""<h2>Welcome to the Library!</h2>
<p>Available URLs:</p>
<ul>
    <li><strong>Books Management:</strong>
        <ul>
            <li><code>/loans/add_book</code> - Add a new book (admin).</li>
            <li><code>/loans/remove_book/(int:book_id)/</code> - Remove a book (admin).</li>
            <li><code>/loans/update_book/(int:book_id)/</code> - Update book details (admin).</li>
            <li><code>/loans/display_books</code> - View all books.</li>
            <li><code>/loans/display_book/(int:book_id)/</code> - View details of a specific book.</li>
            <li><code>/loans/find_book/(str:name)/</code> - Search for a book by name.</li>
        </ul>
    </li>
    <li><strong>Loans Management:</strong>
        <ul>
            <li><code>/loans/loan_book</code> - Loan a book.</li>
            <li><code>/loans/return_book</code> - Return a book.</li>
            <li><code>/loans/display_loans</code> - View all loans (admin).</li>
            <li><code>/loans/display_active_loans</code> - View all active loans.</li>
            <li><code>/loans/late_loans</code> - View late loans (admin).</li>
            <li><code>/loans/late_loans/(int:customer_id)/</code> - View late loans for a specific customer.</li>
            <li><code>/loans/customer/(int:customer_id)/</code> - View all loans for a specific customer.</li>
        </ul>
    </li>
    <li><strong>Customer Management:</strong>
        <ul>
            <li><code>/customer/register</code> - Register a new customer (admin).</li>
            <li><code>/customer/display_customers</code> - View all customer details (admin).</li>
            <li><code>/customer/find_customer/(str:name)/</code> - Search for a customer by name (admin).</li>
            <li><code>/customer/remove_customer/(int:customer_id)/</code> - Remove a customer (admin).</li>
            <li><code>/customer/update_customer/(int:customer_id)/</code> - Update customer details (admin).</li>
            <li><code>/customer/customer/(int:customer_id)/</code> - View details of a specific customer.</li>
        </ul>
    </li>
</ul>
""")

def loanings(request):
    return HttpResponse("Welcome to loanings!<br>urls in main window..")

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
            due_date=due_date,
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request):
    try:
        # Retrieve loan_id from the request
        loan_id = request.data.get('loan_id')
        
        # Get the loan instance
        loan = Loan.objects.get(id=loan_id)

        # Check if the authenticated user is the customer who loaned the book or an admin
        if not request.user.is_staff and loan.cust_id.id != request.user.id:
            return Response({"error": "Not authorized to return this book"}, status=status.HTTP_403_FORBIDDEN)

        # Check if the loan is already inactive
        if not loan.is_active:
            return Response({"error": "This book is already returned."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the return date to the current date and mark the loan as inactive
        loan.return_date = timezone.now()
        loan.is_active = False
        loan.save()

        # Update the book availability
        loan.book_id.isActive = True
        loan.book_id.save()

        return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)

    except Loan.DoesNotExist:
        return Response({"error": "Loan record not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def display_books(request):
    try:
        # Retrieve all book records
        books = Book.objects.all().order_by('author').values()

        # Serialize the book data
        serializer = BookSerializer(books, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])  # Require the user to be authenticated
def display_book(request, book_id):
    try:
        # Try to retrieve the book by its ID
        book = Book.objects.get(id=book_id)
        
        # Serialize the book data
        serializer = BookSerializer(book)
        
        # Return the book details in the response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Book.DoesNotExist:
        # Return an error if the book is not found
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # Handle any other exceptions
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def display_loans(request):
    try:
        # Retrieve active and inactive loans separately
        active_loans = Loan.objects.filter(is_active=True)
        inactive_loans = Loan.objects.filter(is_active=False)

        # Serialize the loan data
        active_serializer = LoanSerializer(active_loans, many=True)
        inactive_serializer = LoanSerializer(inactive_loans, many=True)

        # Return the serialized data in separate lists for active and inactive loans
        return Response({
            "active_loans": active_serializer.data,
            "inactive_loans": inactive_serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def display_active_loans(request):
        active_loans = Loan.objects.filter(is_active=True)#.select_related('book', 'customer')
        serializer = LoanSerializer(active_loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def display_customer_loans(request, customer_id):
    try:
        # Check if the customer exists
        customer = Customer.objects.get(id=customer_id)

        # Check if the requesting user is either an admin or the specified customer
        if not (request.user.is_staff or request.user.id == customer.id):
            return Response({"error": "Not authorized to view these loans"}, status=status.HTTP_403_FORBIDDEN)

        # Filter loans for the specified customer
        active_loans = Loan.objects.filter(cust_id=customer, is_active=True)
        inactive_loans = Loan.objects.filter(cust_id=customer, is_active=False)

        # Serialize the loan data
        active_serializer = LoanSerializer(active_loans, many=True)
        inactive_serializer = LoanSerializer(inactive_loans, many=True)

        # Return the serialized data in separate lists for active and inactive loans
        return Response({
            "active_loans": active_serializer.data,
            "inactive_loans": inactive_serializer.data
        }, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def display_late_loans(request):
    try:
        # Filter loans where the return date has passed and the loan is still active
        late_loans = Loan.objects.filter(due_date__lt=timezone.now(), is_active=True)

        # Serialize the late loan data
        serializer = LoanSerializer(late_loans, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def display_customer_late_loans(request, customer_id):
    try:
        # Retrieve the customer instance
        customer = Customer.objects.get(id=customer_id)

        # Check if the requesting user is either an admin or the specified customer
        if not (request.user.is_staff or request.user.id == customer.id):
            return Response({"error": "Not authorized to view these loans"}, status=status.HTTP_403_FORBIDDEN)

        # Filter late loans for the specified customer
        late_loans = Loan.objects.filter(cust_id=customer, due_date__lt=timezone.now(), is_active=True)

        # Serialize the late loan data
        serializer = LoanSerializer(late_loans, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])  # Allow authenticated users to access, but also allow read-only access
def find_book_by_name(request, name):
    try:
        # Filter books by name (case-insensitive)
        books = Book.objects.filter(title__icontains=name)

        if not books.exists():
            return Response({"error": "No books found with that name"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the book data
        serializer = BookSerializer(books, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def remove_book(request, book_id):
    try:
        # Retrieve the book by ID
        book = Book.objects.get(id=book_id)
        book.delete()  # Delete the book instance

        return Response({"message": "Book removed successfully"}, status=status.HTTP_204_NO_CONTENT)

    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_book(request, book_id):
    try:
        # Retrieve the book by ID
        book = Book.objects.get(id=book_id)
        
        # Update the book fields based on the request data
        book.title = request.data.get('title', book.title)
        book.author = request.data.get('author', book.author)
        book.description = request.data.get('description', book.description)
        book.published_year = request.data.get('published_year', book.published_year)
        book.book_type = request.data.get('book_type', book.book_type)
        book.isActive = request.data.get('isActive', book.isActive)
        book.image = request.data.get('image', book.image)

        # Save the updated book instance
        book.save()

        # Serialize the updated book data
        serializer = BookSerializer(book)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)