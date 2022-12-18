from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,Profile,Forget_Password,Skill

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Forget_Password)
admin.site.register(Skill)
