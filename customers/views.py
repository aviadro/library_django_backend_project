from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status


from customers.models import Customer
from customers.serializers import CustomerSerializer 


def customers(request):
    return HttpResponse("Welcome to the customers!")


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register(request):
    try:

        user = Customer.objects.create_user(
            username=request.data.get('username'),
            email=request.data.get('email', ''),
            password=request.data.get('password', '')  
        )


        # Optional fields for additional attributes in the Customer model
        user.city = request.data.get('city', '')
        user.age = request.data.get('age', None)
        user.phone = request.data.get('phone', '')
        user.is_active = request.data.get('is_active', True)  # Set to True by default
        user.save()

        return Response({"message": "New user registered successfully"}, status=201)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def display_customers(request):
    try:
        # Retrieve all customers
        customers = Customer.objects.all()

        # Serialize the customer data with their loans
        serializer = CustomerSerializer(customers, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])  # Only admins can access this view
def find_customer_by_name(request, name):
    try:
        # Filter customers by name (case-insensitive)
        customers = Customer.objects.filter(username__icontains=name)

        if not customers.exists():
            return Response({"error": "No customers found with that name"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the customer data using the existing CustomerSerializer
        serializer = CustomerSerializer(customers, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def remove_customer(request, customer_id):
    try:
        # Retrieve the customer by ID
        customer = Customer.objects.get(id=customer_id)

        # Mark the customer as inactive instead of deleting
        customer.is_active = False
        customer.save()

        return Response({"message": "Customer marked as inactive successfully."}, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_customer(request, customer_id):
    try:
        # Retrieve the customer by ID
        customer = Customer.objects.get(id=customer_id)

        # Update the customer fields based on the request data
        customer.username = request.data.get('username', customer.username)
        customer.email = request.data.get('email', customer.email)
        customer.city = request.data.get('city', customer.city)
        customer.age = request.data.get('age', customer.age)
        customer.phone = request.data.get('phone', customer.phone)
        customer.is_active = request.data.get('is_active', customer.is_active)

        # Update password if provided
        new_password = request.data.get('password')
        if new_password:
            customer.password = make_password(new_password)  # Hash the new password

        # Save the updated customer instance
        customer.save()

        # Serialize the updated customer data (assuming you have a CustomerSerializer)
        serializer = CustomerSerializer(customer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_customer_by_id(request, customer_id):
    try:
        # Fetch the customer object by ID
        customer = Customer.objects.get(id=customer_id)

        # Serialize the customer data
        serializer = CustomerSerializer(customer)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)