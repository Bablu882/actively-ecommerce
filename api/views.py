from email.policy import default
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect,render
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
from management.views import profile, send_forget_password_mail
from management.token import account_activation_token

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterUserAPI(APIView):
    def post(self,request,format=None):
        serializer=RegisterSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'message':'Email has been sent please check your mail and verify','token':token},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class LoginUser(APIView):
    def post(self,request,format=None):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username=serializer.data.get('username')
            password=serializer.data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
               token=get_tokens_for_user(user)
               return Response({'message':'login success','token':token})
            else:
                return Response({'error':{'non_field_errors':['invalid credentials']}},status=status.HTTP_404_NOT_FOUND)


class LogoutUser(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,fromat=None):
        logout(request)
        return Response({'message':'User logout successfully'},status=status.HTTP_200_OK)


class ForgetPassword(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        data=request.data
        email=data['email']
        user=User.objects.get(email=email)
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        mail_subject="password reset request"
        message = render_to_string('api/activate.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })
        to_email = email  
        email = EmailMessage(  
                    mail_subject, message, to=[to_email]  
        )  
        email.send()
        return Response({'message':'Forget password email has been sent please check your inbox'})
        
    

###----------------------------using class based views------------------------------------------------------------###

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from django.http import Http404


class StudentView(APIView):
    def get(self,request,format=None):
        queryset=Student.objects.all()
        serializer=StudentSerializer(queryset,context={'request': request}, many=True)
        return Response (serializer.data)
    def post(self,request,format=None):
        serializer=StudentSerializer(data=request.data)    
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StudentViewSet(APIView):
    def get_object(self,pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        objects=self.get_object(pk)
        serializer=StudentSerializer(objects)
        return Response(serializer.data)

    def put(self,request,pk,foramt=None):
        objects=self.get_object(pk)    
        serializer=StudentSerializer(objects,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND) 

    def delete(self,request,pk,format=None):
        objects=self.get_object(pk)        
        objects.delete()
        return Response({"mess":"Student deleted successfully !"},status=status.HTTP_200_OK)

##-----------------------------------using mixins class based views-----------------------------------------------------###                     

from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
class StudentMixinList(ListModelMixin,CreateModelMixin,GenericAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)    

class StudentMixinDetail(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)    

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)    


###---------------------------using generic class based vivews-------------------------------###

from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView

class StudentGenericList(ListCreateAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class StudentGenericDetails(RetrieveUpdateDestroyAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

###--------------------------------------------------------------------------------------###
class UserGenericList(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserGenericDetails(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=User.objects.all()    
    serializer_class=UserSerializer
###------------------------------------------------------------------------------------####
class UserViewList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        queryset=User.objects.all()           
        serializer=UserSerializer(queryset,context={"request":request},many=True)
        return Response(serializer.data)
        
    def post(self,request,foramt=None):
        serializer=UserSerializer(data=request.data)    
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,{'message':'user created !'})
        return Response(serializer.errors)    

class UserViewDetail(APIView):
    permission_classes=[IsAuthenticated]
    def get_user_objects(self,pk):
        try:
            User.objects.get(pk=pk)    
        except User.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        user=self.get_user_objects(pk)            
        serializer=UserSerializer(user)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        user=self.get_user_objects(pk)    
        serializer=UserSerializer(user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)  
          
    def delete(self,request,pk,format=None):
        user=self.get_user_objects(pk)
        user.delete()
        return Response({"message":"user deleted successfully"})

###----------------------------------------------------------------------------------------###

class UserMixinList(ListModelMixin,CreateModelMixin,GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)   
    

class UserMixinDetail(RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)    

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)    

class ProfileView(APIView):
    def get(self,request,pk,format=None):
        try:
            user=User.objects.get(pk=pk)
        except User.DoesNotExist:
            user=None
        try:    
            profile=Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile=None    
        serializer=ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        user=User.objects.get(pk=pk)
        profile=Profile.objects.get(user=user)
        serializer=ProfileSerializer(profile,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors)    
####-----------------------------cookies-------------------------------------------------------------#####
from datetime import datetime,timedelta

def setcookies(request):
    response= render (request,'api/set_cookie.html')
    response.set_signed_cookie('name','webnyxa',secure=True,salt='nm',expires=datetime.utcnow()+timedelta(days=2))
    return response

def getcookies(request):
    name=request.get_signed_cookie('name',default='guest',salt='nmm')
    return render(request,'api/get_cookie.html',{'name':name})

def deletecookies(request):
    response=render(request,'api/delete_cookie.html')
    response.delete_cookie('name')
    return response


    