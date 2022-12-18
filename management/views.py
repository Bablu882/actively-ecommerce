
from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, logout as auth_logout
from django.contrib.auth import login as login_dj
from .decorator import authenticate_user
from django.contrib.auth.decorators import login_required
from .models import Profile,User
import uuid
from django.core.mail import send_mail,BadHeaderError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.http import HttpResponse  
from django.utils.encoding import force_bytes  
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from .token import account_activation_token
from .forms import ChangePasswordForm, ForgetPasswordform, RegisterForm,LoginForm, Userchangeform,ProfileForm
from .forms import Skill_form
from django.db.models import Q
import logging
from .models import Skill
from django.contrib.auth.decorators import user_passes_test


def check_admin(user):
    return user.is_superuser




def test1_view(request):
    return render(request,'management/test1.html')

@user_passes_test(check_admin)    
@login_required(login_url='login')
def add_user(request):
    return render(request,'management/add-user.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request ,'management/dashboard.html')    

def forgot_password(request):
    return render(request,'management/forget-password.html') 
       
@user_passes_test(check_admin)
@login_required(login_url='login')
def listing(request):
    users=User.objects.all()
    return render(request,'management/listing.html',{'user':users})

@login_required(login_url='login')
def profile(request):
    list=[]
    skills=Skill.objects.get(user=request.user)
    printd=vars(skills)
    for key in printd:
        if printd[key]==True and key != 'user_id':
            list.append(key)
    return render(request,'management/profile.html',{'names':list})


###------------------------------------Register User------------------------------------###

@authenticate_user
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        try: 
            form = RegisterForm(request.POST)
            if form.is_valid():
                user=form.save(commit=False)
                user.is_active=False
                user.save()
                current_site=get_current_site(request)
                mail_subject='verify mail'
                message = render_to_string('management/activate.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })
                to_email = form.cleaned_data.get('email')  
                email = EmailMessage(  
                            mail_subject, message, to=[to_email]  
                )  
                email.send()
                messages.add_message(request,messages.SUCCESS,'we have sent you a mail to verify your account')
        except Exception as e:
            logging.error(e)
            return redirect('/register')
    else:
        form = RegisterForm()
    return render(request, 'management/register.html', {'form':form}) 

###-------------------------------------Click For Activate----------------------------------###

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        messages.success(request,'Your email is verified now you can login') 
        return redirect('/login')  
    else: 
        return HttpResponse('Activation link is invalid!')       


##--------------------------------LOGOUT---------------------------------------##

def logout(request):
    auth_logout(request=request)
    messages.add_message(request, messages.SUCCESS,'Successfully logged out')
    return redirect('/login')    




##-----------------Forget password--------------------------------##

def forget_password(request):
    form=ForgetPasswordform()
    try:
        if request.method=='POST':
            form=ForgetPasswordform(request.POST)
            if form.is_valid(): 
                email=form.cleaned_data['email']   
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
                messages.success(request,'please check your mail we have sent a link')
                return redirect('/forget-password')
    except Exception as e:
        logging.error(e)
    return render(request,'management/forget-password.html',{'form':form})

###-----------------------------Redirect On Change Password Form---------------------------##



def change_password(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        User = None
    print(user)
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                newpass=form.cleaned_data['password']
                userobj=User.objects.get(pk=uid)
                userobj.set_password(newpass)
                userobj.is_active=True
                userobj.save()
                messages.success(request, "Your password has been set. Now you can login")
                return redirect('/login')
        else:
            form=ChangePasswordForm() 
    else:
        return HttpResponse('invilid link')               
    return render(request,'management/change-password.html',{'form':form})        
                

###------------------------------------Forget Password Mail---------------------------------###



def send_forget_password_mail(email,token):
    subject="Change your password"
    message=f'click here http://127.0.0.1:8000/change-password/{token}'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)


##----------------------------------------LOGIN------------------------------------------------##

def login(request):
    form =LoginForm()
    try:       
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],)
                if user is not None:
                    login_dj(request, user)
                    messages.success(request,f'Welcome {user.username}')
                    return redirect('/dashboard')
                else:
                    messages.error(request,'Provide valid credentials or check your mail')
    except Exception as e:
        logging.error(e)
    return render(request, 'management/login.html', context={'form': form,}) 

###------------------------------------Admin Add User------------------------------------------------####
@user_passes_test(check_admin)
@login_required(login_url='login')
def add_user_admin(request):
    form=RegisterForm()
    try:    
        if request.method=='POST':
            form=RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                form=RegisterForm()
                messages.success(request,'Add user successfully')
        else:
            form=RegisterForm()        
    except Exception as e:
        logging.error(e)
    return render(request,'management/admin-add-user.html',{'form':form})

###------------------------------------Admin Delete User------------------------------------###

@user_passes_test(check_admin)
@login_required(login_url='login')
def delete_user(request,slug):
        user=User.objects.get(username=slug)
        user.delete()
        messages.success(request,'User deleted successfully !!')
        return redirect('/listing')

###-----------------------------------Admin Edit User--------------------------------------###

@user_passes_test(check_admin)
@login_required(login_url='login')
def edit_user(request,slug):
    try:    
        request.method=='POST'
        gt=User.objects.get(username=slug)
        pro=Profile.objects.get(slug=slug)
        form=Userchangeform(request.POST,request.FILES,instance=gt)
        form2=ProfileForm(request.POST,request.FILES,instance=pro)
        form3=Skill_form(request.POST,instance=gt.skill)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            email=form.cleaned_data['email']
            if User.objects.exclude(id=gt.id).filter(email=email).exists():
                messages.error(request,'Email has already taken choose another one !')
                return render(request,'management/change-user-form.html')
            form.save()
            form2.save()
            form3.save()
            messages.success(request,'User updated successfully!!')
        else:
            gt=User.objects.get(username=slug)
            pro=Profile.objects.get(slug=slug)
            form=Userchangeform(instance=gt)
            form2=ProfileForm(instance=pro)
            form3=Skill_form(instance=gt.skill)
    except Exception as e:
        logging.error(e)
    return render(request,'management/change-user-form.html',{'form':form,'form2':form2,'form3':form3,'image':gt})

###---------------------------------------Edit User Profile---------------------------------###

@login_required(login_url='login')
def edit_profile(request):
    try: 
        request.method=='POST'
        gt=User.objects.get(id=request.user.id)
        form=Userchangeform(request.POST,instance=gt)
        form2=ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        form3=Skill_form(request.POST,instance=request.user.skill)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            email=form.cleaned_data['email']
            if User.objects.exclude(id=gt.id).filter(email=email).exists():
                messages.error(request,'Email has already taken choose another one !')
                return redirect('/edit-profile')
            form.save()
            form2.save()
            form3.save()
            messages.success(request,'Profile updated successfully!!')
            return redirect('/profile')
        else:
            gt=User.objects.get(id=request.user.id)
            form=Userchangeform(instance=gt)
            form2=ProfileForm(instance=request.user.profile)
            form3=Skill_form(instance=request.user.skill)
    except Exception as e:
        logging.error(e)
    return render(request,'management/edit-profile.html',{'form':form,'form2':form2,'form3':form3})    

@user_passes_test(check_admin)
@login_required(login_url='login')
def view_user_profile(request,slug):
    print(slug)
    list=[]
    get=User.objects.get(username=slug)
    profiles=Profile.objects.get(slug=slug)
    skills=Skill.objects.get(user=get)
    image=profiles.avatar
    printd=vars(skills)
    for key in printd:
        if printd[key]==True and key != 'user_id':
            list.append(key)
    
    return render(request,'management/view-profile.html',{'image':image,'user':get,'profiles':profiles,'skills':list})    

###---------------------------------------------------------------------------------------###
def logging_error(request):
    logging.error('this is error')
    logging.info('this is info ')
    logging.warning('this is warning')
    logging.debug('this is debug')
    logging.critical('this is critical')
    return render(request,'management/logging.html')


    

# from .models import Skill

# def skill(request):
#     list=[]
#     skills=Skill.objects.get(user=request.user)
#     printd=vars(skills)
#     for key in printd:
#         if printd[key]==True and key != 'user_id':
#             list.append(key)
#     return render(request,'management/profile.html',{'names':list})
    

# def user_skill(request):
#     if request.method=='POST':
#         form=Skill_form(request.POST,instance=request.user.skill)
#         if form.is_valid():
#             form.save()
#     form=Skill_form(instance=request.user.skill)
#     return render(request,'management/form.html',{'form':form})

