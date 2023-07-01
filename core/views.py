
# Create your views here.
import datetime
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status
from core.models import LoanOffer, LoanRequest
from .serializers import FundSerializer, LoanOfferCreateSerializer, LoanOfferSerializer, LoanRequestGetSerializer, LoanRequestSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.views.decorators.csrf import csrf_exempt
from .decorators import swagger

LENME_CONSTANT_FEE = 3

User = get_user_model()

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}
"""
LOAN REQUESTS
"""
@swagger('POST', 'Create new loan request', LoanRequestSerializer, LoanRequestSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_create(request):
    loan_request = LoanRequest()
    loan_request.borrower = request.user
    loan_request.loan_status = 'pending'
    serializer = LoanRequestSerializer(loan_request, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)


@swagger('PUT', 'Update loan request', LoanRequestSerializer, LoanRequestSerializer)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_update(request):
    loan_request = LoanRequest.objects.get(id=request.data.get('id', -1))
    if loan_request.borrower != request.user:
        return Response({'error': 'You are not the owner of this loan request'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_request.loan_period != 'pending':
        return Response({'error': 'You can only update a pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = LoanRequestSerializer(loan_request, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors)


@swagger('DELETE', 'Delete loan request', LoanRequestSerializer, LoanRequestSerializer)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_remove(request):
    loan_request = LoanRequest.objects.get(id=request.data.get('id', -1))
    if loan_request.borrower != request.user:
        return Response({'error': 'You are not the owner of this loan request'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_request.loan_period != 'pending':
        return Response({'error': 'You can only delete a pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
    loan_request.delete()
    return Response({'message': 'Loan request deleted successfully'}, status=status.HTTP_200_OK)


@swagger('GET', 'Get loans requests of current auth user', LoanRequestGetSerializer, LoanRequestGetSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_get(request, pk=None):
    if pk:
        loan_request = LoanRequest.objects.filter(id=pk).all()
    else:
        loan_request = LoanRequest.objects.all()
    serializer = LoanRequestGetSerializer(loan_request, context=serializer_context, many=pk is None)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger('GET', 'Get loans requests`s by a specific user', LoanRequestSerializer, LoanRequestSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_requests_by_user(request, pk):
    loan_requests = LoanRequest.objects.filter(borrower=pk)
    serializer = LoanRequestSerializer(loan_requests, many=True, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)



@swagger('GET', 'Get loans requests`s offers of current auth user', LoanOfferSerializer, LoanOfferSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_requests_offers(request, pk=None):
    if pk:
        loan_request = LoanRequest.objects.filter(id=pk, borrower=request.user).all()
        if not loan_request:
            return Response({'error': 'Loan request not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            loan_request = loan_request[0]
        loan_requests_offers = LoanOffer.objects.filter(loan_request=pk).all()
    else:
        loan_requests_offers = LoanOffer.objects.filter(borrower=request.user).prefetch_related('investor').all()
        print(loan_requests_offers)
    serializer = LoanOfferSerializer(loan_requests_offers, context=serializer_context, many=pk is None)
    return Response(serializer.data, status=status.HTTP_200_OK)


"""
LOAN OFFERS
"""
@swagger('POST', 'Create new loan offer', LoanOfferCreateSerializer, LoanOfferSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_create(request):
    loan_request = LoanRequest.objects.filter(id=request.data.get('loan_request', -1))
    if not loan_request:
        return Response({'error': 'Loan request not found'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        loan_request = loan_request[0]
    if loan_request.loan_status != 'pending':
        return Response({'error': 'You can only create a loan offer for a pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_request.borrower == request.user:
        return Response({'error': 'You can not create a loan offer for your own loan request'}, status=status.HTTP_400_BAD_REQUEST)
    if (loan_request.loan_amount+LENME_CONSTANT_FEE) > request.user.balance:
        return Response({'error': 'FUND ALERT! You do not have enough balance to create a loan offer for this loan request, fund your account'}, status=status.HTTP_400_BAD_REQUEST)
    
    loan_offer = LoanOffer()
    loan_offer.borrower = loan_request.borrower
    loan_offer.lenme_fee = LENME_CONSTANT_FEE # 3 USD as a constant value
    loan_offer.investor = request.user
    loan_offer.offer_status = 'pending'
    loan_offer.date_offered = datetime.datetime.now()
    loan_offer.total_loan_amount = loan_request.loan_amount + loan_offer.lenme_fee
    serializer = LoanOfferCreateSerializer(loan_offer, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        serializer = LoanOfferSerializer(loan_offer, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)


@swagger('PUT', 'Update loan offer', LoanOfferSerializer, LoanOfferSerializer)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_update(request):
    loan_offer = LoanOffer.objects.get(id=request.data.get('id', -1))
    if loan_offer.investor != request.user:
        return Response({'error': 'You are not the owner of this loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_offer.offer_status != 'pending':
        return Response({'error': 'You can only update a pending loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = LoanOfferSerializer(loan_offer, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors)


@swagger('DELETE', 'Delete loan offer', LoanOfferSerializer, LoanOfferSerializer)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_remove(request):
    loan_offer = LoanOffer.objects.get(id=request.data.get('id', -1))
    if loan_offer.investor != request.user:
        return Response({'error': 'You are not the owner of this loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_offer.offer_status != 'pending':
        return Response({'error': 'You can only delete a pending loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    loan_offer.delete()
    return Response({'message': 'Loan offer deleted successfully'}, status=status.HTTP_200_OK)


@swagger('GET', 'Get loan offer', LoanOfferSerializer, LoanOfferSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_get(request, pk=None):
    if pk:
        loan_offer = LoanOffer.objects.filter(id=pk).all()
    else:
        loan_offer = LoanOffer.objects.filter(investor=request.user).all()
    serializer = LoanOfferSerializer(loan_offer, context=serializer_context, many=pk is None)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger('GET', 'Get loan offers by user', LoanOfferSerializer, LoanOfferSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offers_by_user(request, pk):
    loan_offers = LoanOffer.objects.filter(investor=pk)
    serializer = LoanOfferSerializer(loan_offers, many=True, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger('POST', 'Accept loan offer', LoanOfferSerializer, LoanOfferSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_accept(request, pk):
    loan_offer = LoanOffer.objects.get(id=pk)
    if not loan_offer:
        return Response({'error': 'Loan offer not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if loan_offer.loan_request.borrower != request.user:
        return Response({'error': 'You are not the owner of this loan request'}, status=status.HTTP_400_BAD_REQUEST)
    
    if loan_offer.loan_request.loan_status != 'pending':
        return Response({'error': 'You can only accept a pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
    
    if loan_offer.offer_status != 'pending':
        return Response({'error': 'You can only accept a pending loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check the balance of the investor
    if loan_offer.investor.balance < loan_offer.loan_request.loan_amount + loan_offer.lenme_fee:
        # TODO: ADD NOTIFICATION TO THE INVESTOR
        return Response({'error': 'Investor does not have enough balance to get accept this loan request at the current time we will notify him!'}, status=status.HTTP_400_BAD_REQUEST)
    else: 
        # TODO: ADD NOTIFICATION TO THE INVESTOR
        loan_offer.investor.balance -= loan_offer.loan_request.loan_amount + loan_offer.lenme_fee
        loan_offer.investor.save()

    loan_offer.loan_request.loan_status = 'funded'
    loan_offer.loan_request.save()
    loan_offer.offer_status = 'accepted'
    loan_offer.save()
    # TODO: TRANSFER THE MONEY TO THE BORROWER ACCOUNT AFTER VERIFICATION
    return Response({'message': 'Loan offer accepted successfully'}, status=status.HTTP_200_OK)



@swagger('POST', 'Cancel loan offer', LoanOfferSerializer, LoanOfferSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_cancel(request, pk):
    loan_offer = LoanOffer.objects.get(id=pk)
    if not loan_offer:
        return Response({'error': 'Loan offer not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if loan_offer.loan_request.borrower != request.user:
        return Response({'error': 'You are not the owner of this loan request'}, status=status.HTTP_400_BAD_REQUEST)
    
    if loan_offer.loan_request.loan_status != 'pending':
        return Response({'error': 'You can only cancel a pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
    
    if loan_offer.offer_status != 'pending':
        return Response({'error': 'You can only cancel a pending loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    
    loan_offer.loan_request.loan_status = 'pending'
    loan_offer.loan_request.save()
    loan_offer.offer_status = 'cancelled'
    loan_offer.save()
    return Response({'message': 'Loan offer cancelled successfully'}, status=status.HTTP_200_OK)


@swagger('GET', 'Get user data', UserSerializer, UserSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def user_get(request, pk=None):
    user = User.objects.get(id=pk if pk else request.user.id)
    serializer = UserSerializer(user, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger('POST', 'Fund user account', FundSerializer, FundSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def user_fund(request):
    fund = FundSerializer(data=request.data)
    if fund.is_valid():
        user = request.user
        user.balance += fund.data['amount']
        user.save()
        return Response({'message': 'Funded successfully'}, status=status.HTTP_200_OK)
    return Response(fund.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger('GET', 'Get loans requests of current auth user', LoanRequestSerializer, LoanRequestSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loans_requests_of_user(request, pk=None):
    user = User.objects.get(id=pk if pk else request.user.id)
    loan_requests = LoanRequest.objects.filter(borrower=user)
    serializer = LoanRequestSerializer(loan_requests, many=True, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)
