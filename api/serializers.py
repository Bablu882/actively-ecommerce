
from rest_framework import serializers
from management.models import User,Profile
import uuid
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from management.token import account_activation_token
from rest_framework.response import Response
from rest_framework import status
from drf_extra_fields.fields import Base64FileField

class RegisterSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])        
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2=serializers.CharField(required=True,write_only=True)
    class Meta:
        model=User
        fields=('username','email','password','password2',)
        # extra_kwargs={
        #     'first_name':{'required':True},
        #     'last_name':{'required':True}
        # }

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'password field miss matched'})
        return attrs    

    def create(self,validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.is_active=False           
        get=user.save()
        tokenise=uuid.uuid4()
        Profile.objects.create(user=user,token=tokenise)
        current_site=get_current_site(self.context['request'])
        print(current_site)
        mail_subject='verify mail'
        message = render_to_string('management/activate.html', {  
            'user': get,  
            'domain': current_site,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            'token':account_activation_token.make_token(user)
        })
        to_email =validated_data['email']  
        emails = EmailMessage(  
                    mail_subject, message, to=[to_email]  
        )  
        emails.send()
        return user

class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=150)
    class Meta:
        model=User
        fields=['username','password']

class ForgetPasseordSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    class Meta:
        model=User
        fields=['email']
    def validate(self, attrs):
        if User.objects.filter(attrs['email']).exists():
            return attrs
        else:
            return Response({'error':'Email doesnot exists'},status=status.HTTP_400_BAD_REQUEST)    


from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['id','name','city','state']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'        

class ProfileSerializer(serializers.ModelSerializer):
    avatar=serializers.ImageField()
    class Meta:
        model=Profile
        fields=['avatar']
