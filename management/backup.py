# def login(request):
#     if request.method=="GET":
#       resp=render(request,'management/login.html')    
#       return resp
#     elif request.method=="POST":
#         u_name=request.POST.get('username')
#         u_pass=request.POST.get('password')
#         p=authenticate(request,username=u_name,password=u_pass)
#         if p is not None:
#             login(request,p)
            
#             return redirect('/profile')
#         else:
#              resp=render(request,'management/login.html')
#              return resp  

#from .forms import SignupForm,UserCreationForm
# def signup_view(request):
#     form=SignupForm(request.POST)

#     if form.is_valid():
    
#         username=form.cleaned_data['username']
#         print(username)
#         email=form.cleaned_datdef login(request):
    # if request.method=="GET":
    #   resp=render(request,'management/login.html')    
    #   return resp
    # elif request.method=="POST":
    #     u_name=request.POST.get('username')
    #     u_pass=request.POST.get('password')
    #     p=authenticate(request,username=u_name,password=u_pass)
    #     if p is not None:
    #         login(request,p)
            
    #         return redirect('/profile')
    #     else:
    #          resp=render(request,'management/login.html')
    #          return resp  

#from .forms import SignupForm,UserCreationForm
# def signup_view(request):a['email']
#         password1=form.cleaned_data['password1']
#         password2=form.cleaned_data['password2']
#         authenticate(username=username,email=email,passowrd1=password1,password2=password2)
#         form.save()
#         return redirect('login')
#         # if new_user is not None:
#         #     login(request,new_user)
#         #     return redirect('login')

        
#     else:
#         form=SignupForm()
#     context={
#         'form':form
#     }    



#     return render(request,'management/register.html',context)


# from django.contrib.auth import get_user_model
# from django_email_verification import SendEmailForVerification

# def logout_user(request):

#     logout(request)

#     messages.add_message(request, messages.SUCCESS,
#                          'Successfully logged out')

#     return redirect(reverse('login'))


# import os
# from django.conf import settings
# from django.shortcuts import render
# from django.templatetags.static import static

# # Create your views here.
# def index(request):
#     path = settings.MEDIA_ROOT
#     img_list = os.listdir(path + '/profile_pics')
#     context = {'images' : img_list}
#     return render(request, "management/profile.html", context)


# @method_decorator(login_required(login_url='login'), name='dispatch')
# class ProfileView(View):
#     profile = None

#     def dispatch(self, request, *args, **kwargs):
#         self.profile, __ = Profile.objects.get_or_create(user=request.user)
#         return super(ProfileView, self).dispatch(request, *args, **kwargs)

#     def get(self, request):
#         context = {'profile': self.profile, 'segment': 'profile'}
#         return render(request, 'management/profile2.html', context)

#     def post(self, request):
#         form = ProfileForm(request.POST, request.FILES, instance=self.profile)

#         if form.is_valid():
#             profile = form.save()
#             profile.user.first_name = form.cleaned_data.get('first_name')
#             profile.user.last_name = form.cleaned_data.get('last_name')
#             profile.user.email = form.cleaned_data.get('email')
#             profile.user.save()

#             messages.success(request, 'Profile saved successfully')
#         else:
#             messages.error(request, form_validation_error(form))
#         return redirect('profile')




# def session_store(request):
#     # …

#     num_authors = User.objects.count()  # The 'all()' is implied by default.

#     # Number of visits to this view, as counted in the session variable.
#     num_visits = request.session.get('num_visits', 0)
#     request.session['num_visits'] = num_visits + 1

#     context = {
#         'num_authors': num_authors,
#         'num_visits': num_visits,
#     }

#     # Render the HTML template index.html with the data in the context variable.
#     return render(request, 'management/dashboard.html', context=context)


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#         print(ip)
#     return ip



# def activate_user(request, uidb64, token):

#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))

#         user = User.objects.get(pk=uid)

#     except Exception as e:
#         user = None

#     if user and generate_token.check_token(user, token):
#        ## user.is_email_verified = True
#         user.save()

#         messages.add_message(request, messages.SUCCESS,
#                              'Email verified, you can now login')
#         return redirect('/login')

#     return render(request, 'management/activate-fail.html', {"user": user})


# class EmailThread(threading.Thread):

#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()



# def send_activation_email(user, request):
#     current_site = get_current_site(request)
#     email_subject = 'Activate your account'
#     email_body = render_to_string('management/activate.html', {
#         'user': user,
#         'domain': current_site,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': generate_token.make_token(user)
#     })

    # email = EmailMessage(subject=email_subject, body=email_body,
    #                      from_email=settings.EMAIL_HOST_USER,
    #                      to=[user.email]
    #                      )

    
    # EmailThread(email).start()
#oninvalid="this.setCustomValidity('Valid email required')"  oninput="setCustomValidity('')" required


#Registration of new user    
def registerUser(request):
    if request.method == "POST":
        context = {'has_error': False,'require':False,'email':False,'password':False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            password_required="Password should be at least 6 characters"
            context['password'] = password_required

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch')
            context['has_error'] = True    

        if not username:
            user_required="Username is required"
            context['require'] = user_required

        if not email:
            email_required="Email is required"    
            context['email']=email_required

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,'Username is taken, choose another one')
            context['has_error'] = True
            return render(request, 'management/register.html', context, status=409)

        if User.objects.filter(email=email).exists():
            messages.add_message(request,messages.SUCCESS,'Email is taken, choose another one')
            context['has_error'] = True
            return render(request, 'management/register.html', context, status=409)

        if context['has_error']:
            return render(request, 'management/register.html', context)

        uid=uuid.uuid4()
        user = User.objects.create(username=username, email=email)
        profile_obj=Profile.objects.create(user=user,token=uid)
        print(profile_obj)
        user.set_password(password)
        user.save()
        send_mail_after(user.email,uid)
        messages.add_message(request,messages.SUCCESS,'we have sent you a mail to verify your account')
        return redirect('register')

    return render(request, 'management/register.html')



@authenticate_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login_dj(request, user)
                return redirect('dashboard')
            else:
                print('TEST')
                messages.info(request, 'Inactive user')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username/password!')
        return redirect('login')
    else:
        return render(request, 'management/login.html', {})


#Send mail after registration
# def send_mail_after(email,token):
#     subject="verify email"
#     message=f'click here http://127.0.0.1:8000/verify-email/{token}'
#     from_email=settings.EMAIL_HOST_USER
#     recipient_list=[email]
#     send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)

# #verify mail after registration send link to user mail 
# def verify_mail(request,token):
#     profile_id=Profile.objects.filter(token=token).first()
#     print(profile_id)
#     profile_id.is_verified=True
#     profile_id.save()
#     messages.success(request,'Your account is verified now you can login')
#     return redirect('login')


# from .forms import ForgetPasswordform
# # def forget_password(request):
# #     form=ForgetPasswordform()
# #     if request.method=='POST':
# #         form=ForgetPasswordform(request.POST)        
# #         if form.is_valid():
# #             user=form.cleaned_data['email']
# #             username=User.objects.filter(email=user)
# #             current_site=get_current_site(request)
# #             mail_subject='verify mail'
# #             message = render_to_string('management/activate-forget-password.html', {  
# #                 'user': username,  
# #                 'domain': current_site.domain,  
# #                 'uid':urlsafe_base64_encode(force_bytes(username.pk)),  
# #                 'token':account_activation_token.make_token(username),  
# #             })
# #             to_email = form.cleaned_data.get('email')  
# #             email = EmailMessage(  
# #                         mail_subject, message, to=[to_email]  
# #             )  
# #             email.send() 
# #             messages.add_message(request,messages.SUCCESS,'we have sent you a mail to verify your account')
# #         else:
# #             messages.error(request,'invilid email')
# #             return render(request,'management/activate-forget-password.html')
            
# #     else:
# #         form=ForgetPasswordform()    
# #             # clean=form.cleaned_data['email']
# #     return render(request,'management/forget-password.html',{'form':form})


# from django.db.models.query_utils import Q


# # def forget_password(request):

# # 	if request.method == "POST":
# # 		password_reset_form = ForgetPasswordform(request.POST)
# # 		if password_reset_form.is_valid():
# # 			data = password_reset_form.cleaned_data['email']
# # 			associated_users = User.objects.filter(Q(email=data))
# # 			if associated_users.exists():
# # 				for user in associated_users:
# # 					subject = "Password Reset Requested"
                    
# # 					email_template_name = "management/activate-forget-password.html"
# # 					c = {
# # 					"email":user.email,
# # 					'domain':'127.0.0.1:8000',
# # 					'site_name': 'Website',
# # 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# # 					"user": user,
# # 					'token': account_activation_token .make_token(user),
# # 					'protocol': 'http',
        
# # 					}
# # 					email = render_to_string(email_template_name, c)
                
# # 					try:
# # 						send_mail(subject, email, recipient_list=[data], fail_silently=False,from_email=settings.EMAIL_HOST_USER)
# # 					except BadHeaderError:
# # 						return HttpResponse('Invalid header found.')
# # 					return redirect ("forget-password")
# # 	password_reset_form = ForgetPasswordform()
# # 	return render(request, "management/forget-password.html", context={"password_reset_form":password_reset_form})


#     # current_site=get_current_site(request)
#     #         mail_subject='verify mail'
#     #         message = render_to_string('management/activate.html', {  
#     #             'user': user,  
#     #             'domain': current_site.domain,  
#     #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
#     #             'token':account_activation_token.make_token(user),  
#     #         })
#     #         to_email = form.cleaned_data.get('email')  
#     #         email = EmailMessage(  
#     #                     mail_subject, message, to=[to_email]  
#     #         )  
#     #         email.send() 
# from .forms import ChangePasswordForm
# # def activate_forget_email(request,token):
# #     form=ChangePasswordForm()
# #     if request.method=='POST':
# #         form=ChangePasswordForm(request.POST)
# #         password=form.cleaned_data[password]
# #         conform_password=form.cleaned_data[conform_password]
# #         if password!=conform_password:
# #             messages.error(request,'both password must be same')
# #             return redirect('forget-password/{token}')
# #     return render(request,'management/change-password.html',{'form':form})


# # from django.contrib.auth import update_session_auth_hash

# # def change_password(request,token):
# #     form=ChangePasswordForm()
# #     # if request.method == 'POST':
# #     #     form = ChangePasswordForm(user=request.user, data=request.POST)
# #     #     if form.is_valid():
# #     #         pass
# #     #         update_session_auth_hash(request, form.user)
# #     #         return redirect('dashboard')
# #     # else:

    
# #     return render(request,'management/change-password.html',{'form':form})

# # def change_password(request, uidb64, token):  
# #     User = get_user_model()  
# #     try:  
# #         uid = force_str(urlsafe_base64_decode(uidb64))  
# #         user = User.objects.get(pk=uid)  
# #     except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
# #         user = None  
# #     if user is not None and account_activation_token.check_token(user, token):  
# #         user.is_active = True  
# #         user.save()  
# #         return redirect('login')  
# #     else:  
# #         return HttpResponse('Activation link is invalid!') 

# def forget_password(request):
# 	if request.method == "POST":
# 		password_reset_form = ForgetPasswordform(request.POST)
# 		if password_reset_form.is_valid():    
# 			data = password_reset_form.cleaned_data['email']
            
# 			associated_users = User.objects.filter(Q(email=data))
            
            
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
                    
# 					email_template_name = "management/activate-forget-password.html"
# 					c = {
# 					"email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': account_activation_token.make_token(user),
# 					'protocol': 'http',
        
# 					}
# 					email = render_to_string(email_template_name, c)
                    
                
# 					try:
# 						send_mail(subject, email, recipient_list=[data], fail_silently=False,from_email=settings.EMAIL_HOST_USER)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect ("forget-password")
# 	password_reset_form = ForgetPasswordform()
# 	return render(request, "management/forget-password.html", context={"password_reset_form":password_reset_form})

# def forget_password(request):
#     if request.method=='POST':
#         password_form=ForgetPasswordform(request.POST)
#         if password_form.is_valid():
#             data=password_form.cleaned_data['email']
            
#             Forget_Password.objects.create(email=data)
#             associated_users = User.objects.filter(Q(email=data))
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject='password reset requested'
#                     email_template_name = "management/activate-forget-password.html"
#                     c={
#                       "email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': account_activation_token.make_token(user),
# 					'protocol': 'http',  
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, recipient_list=[data], fail_silently=False,from_email=settings.EMAIL_HOST_USER)
#                     except BadHeaderError:
#                         return HttpResponse('invilid header found !')
#                     messages.success(request,'please check your mail')    
#                     return redirect('forget-password')         
#     password_form = ForgetPasswordform()      
#     return render(request,'management/forget-password.html',{'form':password_form})
# def forget_password(request):
#     form = ForgetPasswordform()
#     if request.method == 'POST':
#         form = ForgetPasswordform(request.POST)
#         user=ForgetPasswordform.cleaned_data['email']
#         current_site=get_current_site(request)
#         mail_subject='verify mail'
#         message = render_to_string('management/activate.html', {  
#             'user': user,  
#             'domain': current_site.domain,  
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
#             'token':account_activation_token.make_token(user),  
#         })
#         to_email = form.cleaned_data.get('email')  
#         email = EmailMessage(  
#                     mail_subject, message, to=[to_email]  
#         )  
#         email.send()
#         token=uuid.uuid4()
#         print(token)
#         profile=Profile.objects.create(user=user,token=token) 
#         print(profile)
#         messages.add_message(request,messages.SUCCESS,'we have sent you a mail to verify your account')

#         return redirect('forget-password')

#     else:
#         form = RegisterForm()
#     return render(request, 'management/forget-password.html', {'form':form}) 

# def activate_user(request, uidb64, token):  
#     User = get_user_model()  
#     try:  
#         uid = force_str(urlsafe_base64_decode(uidb64))  
#         user = User.objects.get(pk=uid)  
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
#         user = None  
#     if user is not None and account_activation_token.check_token(user, token):  
#         # user.is_active = True  
#         # user.save()  
#         return redirect('change-password')  
#     else:  
#         return HttpResponse('Activation link is invalid!')

#Change forgot password 
# def change_password(request,token):
#     context={}
#     try:
#         profile=Profile.objects.filter(token=token).first()
#         print(profile.user.id)
#         if request.method == 'POST':
#             newpass=request.POST.get('newpassword')
#             conformpass=request.POST.get('conform-newpassword')
#             user_id=request.POST.get('user_id')

#             if len(newpass) < 6:
#                 messages.error(request,'password required atleast 6 charactor')
#                 return redirect(f"/change-password/{token}")

#             if user_id is None:
#                 messages.error(request,'No user is found')
#                 return redirect(f"/change-password/{token}/")

#             if newpass != conformpass:
#                 messages.error(request,'password is missmatched')    
#                 return redirect(f"/change-password/{token}")

#             user_obj=User.objects.get(id=user_id)    
#             user_obj.set_password(newpass)
#             user_obj.save()
#             messages.success(request,'New password changed now login with new password')
#             return redirect('login')
#         context={'user_id':profile.user.id}  
#     except Exception as e:
#         print(e)
#     return render(request,'management/change-password.html',context)
class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        def get_label(obj):
            permission_name = str(obj).split('|')[2].strip()
            model_name = permission_name.split(' ')[2].strip()
            return '%s | %s' % (model_name.title(), permission_name)

        User = get_user_model()
        content_type = ContentType.objects.get_for_model(User)
        self.fields['user_permissions'].queryset = Permission.objects.filter(content_type=content_type)
        self.fields['user_permissions'].widget.attrs.update({'class': 'permission-select'})
        self.fields['user_permissions'].help_text = None
        self.fields['user_permissions'].label = "Label"
        self.fields['user_permissions'].label_from_instance = get_label

    def save(self, commit=True):
        user_instance = super(UserForm, self).save(commit)
        user_instance.save()
        user_instance.user_permissions.set(self.cleaned_data.get('user_permissions'))
        return user_instance

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'user_permissions']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'user_permissions': forms.SelectMultiple(attrs={'style': 'width: 350px; height: 200px;'})
        }


 ###-----------------------------------------------------------------------------------###
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)        
    token=models.CharField(max_length=50)
    is_verified=models.BooleanField(default=False)
    
class Forget_Password(models.Model):
    email=models.EmailField(max_length=50)
       



from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,Profile,Forget_Password
from .forms import CustomUserChangeForm,RegisterForm
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Forget_Password)