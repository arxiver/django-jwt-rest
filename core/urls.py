from django.urls import path
from core import views
from rest_framework.schemas import get_schema_view

urlpatterns = [
        path('openapi/', get_schema_view(
        title="Lenme API",
        description="API for lenme task …",
        version="1.0.0"
    ), name='openapi-schema'),
    
    # Loan Request
    path('loan-req/create', views.loan_request_create, name='loan-req-create'),
    path('loan-req/update', views.loan_request_update, name='loan-req-update'),
    path('loan-req/remove', views.loan_request_remove, name='loan-req-remove'),
    path('loan-req/get', views.loan_request_get, name='loan-req-get'),
    path('loan-req/offers/', views.loan_requests_offers, name='loan-req-get'),
    path('loan-req/offers/<int:pk>', views.loan_requests_offers, name='loan-req-get'),
    path('loan-req/users/<int:pk>', views.loan_requests_by_user, name='loan-req-detail'),
    path('loan-req/<int:pk>', views.loan_request_get, name='loan-req-detail'),
    
    # Loan Offer
    path('loan-offer/create', views.loan_offer_create, name='loan-offer-create'),
    path('loan-offer/update', views.loan_offer_update, name='loan-offer-update'),
    path('loan-offer/remove', views.loan_offer_remove, name='loan-offer-remove'),
    path('loan-offer/users/<int:pk>', views.loan_offers_by_user, name='loan-offer-detail'),
    path('loan-offer/get', views.loan_offer_get, name='loan-offer-get'),
    path('loan-offer/<int:pk>', views.loan_offer_get, name='loan-offer-detail'),
    
    path('loan-offer/<int:pk>/accept', views.loan_offer_accept, name='loan-offer-accept'),
    path('loan-offer/<int:pk>/cancel', views.loan_offer_cancel, name='loan-offer-cancel'),


    # User
    path('user/get', views.user_get, name='user-get'),
    path('user/fund', views.user_fund, name='user-fund'),
    path('user/<int:pk>', views.user_get, name='user-detail'),
    path('user/loans-req/<int:pk>', views.loans_requests_of_user, name='user-loans'),
]