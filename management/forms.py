
from django import forms
from django.contrib.auth.forms import UserCreationForm
from requests import request
from .models import Skill, User
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from .models import Profile
import logging




##------------------------------REGISTRATION FORM------------------------------##

class RegisterForm(UserCreationForm):
    username=forms.CharField(error_messages={'required':'Enter your username'})
    email=forms.EmailField(error_messages={'required':'Enter your email'})
    password1 = forms.CharField(error_messages={'required':'Enter your password'},widget=forms.PasswordInput)
    password2 = forms.CharField(error_messages={'required':'Enter your confirm password'},widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields["username"].widget.attrs.update({
            'name':'username',
            'id':'username',
             'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Username',
            'maxlength':'50',
            'minlength':'6'
        })
        self.fields["email"].widget.attrs.update({
            'name':'email',
             'style':'height:40px',
            'size':'50px',
            'id':'email',
            'type':'text',
            'class':'form-control',
            'placeholder':'Email',
            'maxlength':'50',
            'minlength':'6',
        })
        self.fields["password1"].widget.attrs.update({
            'name':'password1',
            'size':'50px',
            'style':'height:40px',
            'id':'password1',
            'type':'text',
            'class':'form-control',
            'placeholder':'Password',
            'maxlength':'50',
            'minlength':'6'
        })
        self.fields["password2"].widget.attrs.update({
            'name':'password2',
            'id':'password2',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'color':'red',
            'class':'form-control',
            'placeholder':'Confirm password',
            'maxlength':'50',
            'minlength':'6',
        })

    class Meta:
        model=User
        fields=['username','email','password1','password2']
    
        help_texts = {
            'username': None,
        }

    def clean_username(self):
        username=self.cleaned_data['username']    
        if len(username) <=3:
            raise forms.ValidationError('username is too short ')
            
        return username 

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email is already taken')       
        return email    

##----------------------------LOGIN FORM ----------------------------------##

class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,error_messages={'required':'enter your username'})
    password=forms.CharField(max_length=50,widget=forms.PasswordInput,error_messages={'required':'enter your password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            # 'required':'',
            'name':'username',
            'id':'username',
             'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            # 'placeholder':'Username',
            'maxlength':'50',
            'minlength':'6'
        })
        self.fields["password"].widget.attrs.update({
            # 'required':'',
            'name':'password',
             'style':'height:40px',
            'size':'50px',
            'id':'password',
            'type':'text',
            'class':'form-control',
            # 'placeholder':'password',
            'maxlength':'50',
            'minlength':'6'
        })
    def clean_username(self):
        username=self.cleaned_data['username']    
        if not  User.objects.filter(username=username).exists():
            raise forms.ValidationError('username doesnot exist ')
        return username

    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if password:
    #         self.password = authenticate(password=password)
    #         if self.password is None:
    #             raise forms.ValidationError("Please enter a correct password!")
    #         elif not self.password.is_active:
    #             raise forms.ValidationError("This account is inactive.") 

    #     return password
            
##-----------------------FORGET PASSWORD FORM-------------------------------##
class ForgetPasswordform(forms.Form):
    email=forms.EmailField() 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            # 'required':'',
            'name':'email',
            'id':'email',
             'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            # 'placeholder':'Username',
            'maxlength':'50',
            'minlength':'6'
        })
    def clean_email(self):
        email=self.cleaned_data['email']    
        if not  User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email doesn't exist")
        return email      

class ChangePasswordForm(forms.Form):
    password=forms.CharField(error_messages={'required':'enter new-password'},widget=forms.PasswordInput,validators=[validate_password])
    conform_password=forms.CharField(error_messages={'required':'enter conform new-password'},widget=forms.PasswordInput,validators=[validate_password])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs.update({
            # 'required':'',
            'name':'password',
            'id':'password',
             'style':'height:40px',
            'size':'50px',
            'type':'text',
            'placeholder':'password',
            'class':'form-control',
            'maxlength':'50',
            'minlength':'6'
        })
        self.fields["conform_password"].widget.attrs.update({
            'name':'conform_password',
             'style':'height:40px',
            'size':'50px',
            'id':'conform_password',
            'type':'text',
            'class':'form-control',
            'placeholder':'conform-password',
            'maxlength':'50',
            'minlength':'6'
        })
    def clean_conform_password(self):
        password = self.cleaned_data['password']
        conform_password = self.cleaned_data['conform_password']
        if password and conform_password:
                if password != conform_password:
                   raise forms.ValidationError('Password mismatch')
        return conform_password


class Userchangeform(UserChangeForm):
    # first_name=forms.CharField(max_length=50,error_messages={'required':'Enter username'})
    # last_name=forms.CharField(max_length=50,error_messages={'required':'Enter last name'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields["username"].widget.attrs.update({
            
            'name':'username',
            'id':'username',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Username',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["email"].widget.attrs.update({
            # 'required':'',
            'name':'email',
             'style':'height:40px',
            'size':'50px',
            'id':'email',
            'type':'text',
            'class':'form-control',
            'placeholder':'Email',
            'maxlength':'50',
            'minlength':'6',
        })
        self.fields["first_name"].widget.attrs.update({
            'name':'first_name',
            'size':'50px',
            'style':'height:40px',
            'id':'first_name',
            'type':'text',
            'class':'form-control',
            'placeholder':'first_name',
            'maxlength':'50',
            'minlength':'6'
        })
        self.fields["last_name"].widget.attrs.update({
            'name':'last_name',
            'id':'last_name',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'color':'red',
            'class':'form-control',
            'placeholder':'last_name',
            'maxlength':'50',
            'minlength':'6',
        })
        self.fields["user_permissions"].widget.attrs.update({
            'name':'user_permissions',
            'id':'user_permissions',
            'style':'height:200px',
            'size':'50px',
            'type':'text',
            'color':'red',
            'class':'form-control',
            'placeholder':'user_permissions',
            'maxlength':'50',
            'minlength':'6',
        })
        self.fields["date_joined"].widget.attrs.update({
            'name':'date_joined',
            'id':'date_joined',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'color':'red',
            'class':'form-control',
            'placeholder':'date_joined',
            'maxlength':'50',
            'minlength':'6',
        })
        self.fields["last_login"].widget.attrs.update({
            'name':'last_login',
            'id':'last_login',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'color':'red',
            'class':'form-control',
            'placeholder':'last_login',
            'maxlength':'50',
            'minlength':'6',
        })
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','is_superuser','is_staff','last_login','date_joined','user_permissions']
        help_texts = {
                'username': None,
            }    
    

class ProfileForm(forms.ModelForm):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields["avatar"].widget.attrs.update({
            
            'name':'avatar',
            'id':'avatar',
            'style':'height:40px',                                                                                  
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'avatar',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["desc"].widget.attrs.update({
            
            'name':'bio',
            'id':'bio',
            'style':'height:200px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Description',
            'minlength':'6',
            'value':''
        })
        self.fields["address"].widget.attrs.update({
            
            'name':'address',
            'id':'address',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Address',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["work_at"].widget.attrs.update({
            
            'name':'work_at',
            'id':'work_at',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Work_at',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["city"].widget.attrs.update({
            
            'name':'city',
            'id':'city',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Delhi',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["post_code"].widget.attrs.update({
            
            'name':'post_code',
            'id':'post_code',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'203302',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["mobile_no"].widget.attrs.update({
            
            'name':'mobile_no',
            'id':'mobile_no',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'8424656525',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["country"].widget.attrs.update({
            
            'name':'country',
            'id':'country',
            'style':'height:40px',
            # 'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'India',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["state"].widget.attrs.update({
            
            'name':'state',
            'id':'state',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Punjab',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["facebook"].widget.attrs.update({
            
            'name':'facebook',
            'id':'facebook',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Place your facebook url',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["teitter"].widget.attrs.update({
            
            'name':'twitter',
            'id':'twitter',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Place your twitter url',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["instagram"].widget.attrs.update({
            
            'name':'instagram',
            'id':'instagram',
            'style':'height:40px',
            'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'Place your instagram url',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        self.fields["status"].widget.attrs.update({
            
            'name':'status',
            'id':'status',
            'style':'height:40px',
            # 'size':'50px',
            'type':'text',
            'class':'form-control',
            'placeholder':'',
            'maxlength':'50',
            'minlength':'6',
            'value':''
        })
        


    class Meta:
        model=Profile
        fields=['avatar','desc','address','work_at','city','post_code','mobile_no','country','state','facebook','teitter','instagram','status']
###---------------------------------------------------------------------------------------####        

class Skill_form(forms.ModelForm):
    class Meta:
        model=Skill
        fields=['css','html','javascripts','jquery','bootstrap','react','java','python']