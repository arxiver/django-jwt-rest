
# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import generics, status
from core.models import LoanOffer, LoanRequest
from .serializers import LoanOfferSerializer, LoanRequestSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

LENME_CONSTANT_FEE = 3

User = get_user_model()

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}


@swagger_auto_schema(
    method='post',
    operation_summary='Create data',
    request_body=LoanRequestSerializer,
    responses={
        201: openapi.Response(
            description='Created',
            schema=LoanRequestSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_create(request):
    loan_request = LoanRequest()
    loan_request.borrower = request.user
    serializer = LoanRequestSerializer(loan_request, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)


@swagger_auto_schema(
    method='put',
    operation_summary='Update data',
    request_body=LoanRequestSerializer,
    responses={
        200: openapi.Response(
            description='Updated',
            schema=LoanRequestSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_update(request):
    loan_request = LoanRequest.objects.get(id=request.data['id'])
    if loan_request.borrower != request.user:
        return Response({'error': 'You are not the owner of this loan request'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_request.loan_period != 'pending':
        return Response({'error': 'You can only update a pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = LoanRequestSerializer(loan_request, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors)

@swagger_auto_schema(
    method='delete',
    operation_summary='Delete data',
    request_body=LoanRequestSerializer,
    responses={
        200: openapi.Response(
            description='Deleted',
            schema=LoanRequestSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_remove(request):
    loan_request = LoanRequest.objects.get(id=request.data['id'])
    if loan_request.borrower != request.user:
        return Response({'error': 'You are not the owner of this loan request'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_request.loan_period != 'pending':
        return Response({'error': 'You can only delete a pending loan request'}, status=status.HTTP_400_BAD_REQUEST)
    loan_request.delete()
    return Response({'message': 'Loan request deleted successfully'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_summary='Get data',
    responses={
        200: openapi.Response(
            description='Get',
            schema=LoanRequestSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_request_get(request):
    loan_request = LoanRequest.objects.get(id=request.data['id'])
    serializer = LoanRequestSerializer(loan_request, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_summary='Get data',
    responses={
        200: openapi.Response(
            description='Get',
            schema=LoanRequestSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_requests_by_user(request, pk):
    loan_requests = LoanRequest.objects.filter(borrower=pk)
    serializer = LoanRequestSerializer(loan_requests, many=True, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_summary='Create data',
    request_body=LoanOfferSerializer,
    responses={
        201: openapi.Response(
            description='Created',
            schema=LoanOfferSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_create(request):
    loan_offer = LoanOffer()
    loan_offer.lenme_fee = LENME_CONSTANT_FEE # 3 USD as a constant value
    loan_offer.investor = request.user
    serializer = LoanOfferSerializer(loan_offer, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)

@swagger_auto_schema(
    method='put',
    operation_summary='Update data',
    request_body=LoanOfferSerializer,
    responses={
        200: openapi.Response(
            description='Updated',
            schema=LoanOfferSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_update(request):
    loan_offer = LoanOffer.objects.get(id=request.data['id'])
    if loan_offer.investor != request.user:
        return Response({'error': 'You are not the owner of this loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_offer.offer_status != 'pending':
        return Response({'error': 'You can only update a pending loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = LoanOfferSerializer(loan_offer, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors)

@swagger_auto_schema(
    method='delete',
    operation_summary='Delete data',
    request_body=LoanOfferSerializer,
    responses={
        200: openapi.Response(
            description='Deleted',
            schema=LoanOfferSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_remove(request):
    loan_offer = LoanOffer.objects.get(id=request.data['id'])
    if loan_offer.investor != request.user:
        return Response({'error': 'You are not the owner of this loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    if loan_offer.offer_status != 'pending':
        return Response({'error': 'You can only delete a pending loan offer'}, status=status.HTTP_400_BAD_REQUEST)
    loan_offer.delete()
    return Response({'message': 'Loan offer deleted successfully'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_summary='Get data',
    responses={
        200: openapi.Response(
            description='Get',
            schema=LoanOfferSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offer_get(request):
    loan_offer = LoanOffer.objects.get(id=request.data['id'])
    serializer = LoanOfferSerializer(loan_offer, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_summary='Get data',
    responses={
        200: openapi.Response(
            description='Get',
            schema=LoanOfferSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def loan_offers_by_user(request, pk):
    loan_offers = LoanOffer.objects.filter(investor=pk)
    serializer = LoanOfferSerializer(loan_offers, many=True, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='post',
    operation_summary='Create data',
    responses={
        201: openapi.Response(
            description='Created',
            schema=LoanOfferSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
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


@swagger_auto_schema(
    method='post',
    operation_summary='Uop data',
    responses={
        201: openapi.Response(
            description='Created',
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
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


@swagger_auto_schema(
    method='get',
    operation_summary='Get data',
    responses={
        200: openapi.Response(
            description='Get',
            schema=UserSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def user_get(request, pk=None):
    user = User.objects.get(id=pk if pk else request.user.id)
    serializer = UserSerializer(user, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary='Get data',
    responses={
        200: openapi.Response(
            description='Get',
            schema=LoanRequestSerializer
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={

                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def user_loans_requests(request, pk=None):
    user = User.objects.get(id=pk if pk else request.user.id)
    loan_requests = LoanRequest.objects.filter(borrower=user)
    serializer = LoanRequestSerializer(loan_requests, many=True, context=serializer_context)
    return Response(serializer.data, status=status.HTTP_200_OK)
