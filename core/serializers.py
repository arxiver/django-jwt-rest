from django.contrib.auth import get_user_model
from rest_auth.registration import serializers as reg_serializers
from rest_framework import serializers
from rest_framework.fields import empty

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # boarded_by_name = serializers.CharField(source='boarded_by.first_name', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email','first_name','last_name', 'is_superuser', 'pk'
                  ,'national_id','phone_number','balance','address','income','company','boarded_date','boarded_by','last_login','city', 'boarded_by_name']



class RegisterSerializer(reg_serializers.RegisterSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user
