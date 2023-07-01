from django.contrib.auth import get_user_model
from rest_auth.registration import serializers as reg_serializers
from rest_framework import serializers
from rest_framework.fields import empty

from core.models import LoanOffer, LoanRequest

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email','first_name','last_name', 'is_superuser', 'pk', 'is_admin', 
                  'is_investor', 'is_borrower',
                  'phone_number', 'balance']
        

class UserSerializerSafeRead(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name','last_name', 'pk',  'is_investor', 'is_borrower',]


class FundSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    card_number = serializers.CharField(required=True)
    card_holder = serializers.CharField(required=True)
    expiry_date = serializers.CharField(required=True)
    cvv = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['amount', 'card_number', 'card_holder', 'expiry_date', 'cvv']


class RegisterSerializer(reg_serializers.RegisterSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    is_investor = serializers.BooleanField(required=True)
    is_borrower = serializers.BooleanField(required=True)
    def save(self, request):
        is_investor = self.data.get('is_investor')
        is_borrower = self.data.get('is_borrower')
        if not is_investor and not is_borrower:
            raise serializers.ValidationError("User must be either investor or borrower")
        if is_borrower and is_investor:
            raise serializers.ValidationError("User can't be both investor and borrower")
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.phone_number = self.data.get('phone_number')
        user.is_investor = is_investor
        user.is_borrower = is_borrower
        user.save()
        return user

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ['loan_amount', 'loan_period']


class LoanRequestGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'


class LoanOfferSerializer(serializers.ModelSerializer):
    investor = UserSerializerSafeRead(read_only=True)
    class Meta:
        model = LoanOffer
        fields = '__all__'


class LoanOfferGetSerializer(serializers.ModelSerializer):
    investor = UserSerializerSafeRead(read_only=True)
    class Meta:
        model = LoanOffer
        fields = '__all__'

class LoanOfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffer
        fields = ['loan_request', 'annual_interest_rate']
