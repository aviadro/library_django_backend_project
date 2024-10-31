from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response

from customers.models import Customer 


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