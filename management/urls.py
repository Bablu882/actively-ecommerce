from django.urls import path,include 
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 



urlpatterns=[
    path('',test1_view,name='test1'),
    path('add-user',add_user,name='add-user'),
    path('dashboard',dashboard,name='dashboard'),
    path('forgot-password',forgot_password,name='forgot-password'),
    path('listing',listing,name='listing'),
    path('login',login,name='login'),
    path('profile',profile,name='profile'),
    path('register',register,name='register'),
    path('logout',logout,name='logout'),
    path('forget-password',forget_password,name='forget-password'),
    path('change-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',change_password,name='change-password'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate, name='activate'), 
    path('admin-add-user',add_user_admin,name='admin-add-user'),
    path('change-user/<slug:slug>/',edit_user,name='chane-user'),
    path('delete-user/<slug:slug>/',delete_user,name='delete_user'),
    path('edit-profile',edit_profile,name='edit-profile'),
    path('view-profile/<slug:slug>/',view_user_profile,name='view-profile'),
    path('logging',logging_error,name='logging'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)