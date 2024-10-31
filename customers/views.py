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
   user = Customer.objects.create_user(
               username=request.data['username'],
               email=request.data['email'],
               password=request.data['password']
           )
   user.is_active = True
   user.is_staff = True
   user.save()
   return Response("new user born")