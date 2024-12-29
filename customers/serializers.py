from rest_framework import serializers
from customers.models import Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_admin'] = user.is_staff  # Assuming is_staff represents admin status

        return token