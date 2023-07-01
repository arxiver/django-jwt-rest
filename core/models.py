from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    is_borrower = models.BooleanField(default=False)
    def __str__(self):
        return self.email

    def __repr__(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.first_name + " " + self.last_name

class LoanRequest(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_borrower')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_period = models.IntegerField()
    loan_status = models.TextField(choices=(
        ('pending', 'pending'), 
        ('funded', 'funded'), 
        ('completed', 'completed')
    ))
    date_requested = models.DateTimeField(auto_now=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_cancelled = models.DateTimeField(blank=True, null=True)

class LoanOffer(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_investor')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_borrower')
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name='loan_offer_request')
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    lenme_fee = models.DecimalField(max_digits=5, decimal_places=2)
    total_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_status = models.TextField(choices=(
        ('pending', 'pending'), 
        ('accepted', 'accepted'), 
        ('cancelled', 'cancelled')
    ))
    date_offered = models.DateTimeField(auto_now=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_cancelled = models.DateTimeField(blank=True, null=True)

class Loan(models.Model):
    loan_offer = models.ForeignKey(LoanOffer, on_delete=models.CASCADE, related_name='loan_offer')
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name='loan_request')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_status = models.TextField(choices=(
        ('active', 'active'), 
        ('done', 'done'), 
        ('issue', 'issue')
    ))
    date_paid = models.DateTimeField(auto_now=True)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_borrower')
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_investor')
    next_payment_date = models.DateTimeField(blank=True, null=True)
    date_cancelled = models.DateTimeField(blank=True, null=True)


class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.TextField(choices=(
        ('pending', 'pending'), 
        ('paid', 'paid'), 
        ('cancelled', 'cancelled')
    ))
    date_paid = models.DateTimeField(auto_now=True)
    date_cancelled = models.DateTimeField(blank=True, null=True)
