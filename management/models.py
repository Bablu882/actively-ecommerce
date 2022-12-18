from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .utils import create_shortcode
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_countries.fields import CountryField

from .managers import CustomUserManager
import uuid
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
    desc=models.TextField(blank=True,null=True)        
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified=models.BooleanField(default=False)
    avatar=models.ImageField(null=True,blank=True,default='avatars/default.png',upload_to='avatars')
    address=models.CharField(max_length=500,blank=True,null=True)
    work_at=models.CharField(max_length=100,blank=True,null=True)
    display_name=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    post_code=models.CharField(max_length=50,blank=True,null=True)
    mobile_no=models.CharField(max_length=13,blank=True,null=True)
    country=CountryField()
    state=models.CharField(max_length=50,blank=True,null=True)
    customer='customer'
    vender='vender'
    account_select=[
        (customer,'customer'),
        (vender,'vender'),
    ]
    status=models.CharField(max_length=20,choices=account_select,default=customer,blank=True,null=True)
    admission=models.BooleanField(default=False,verbose_name=_("admission"),blank=True,null=True)
    referrals=models.IntegerField(default=0,blank=True,null=True)
    code=models.CharField(max_length=200,blank=True,null=True)
    recommended_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="recommended_by",blank=True,null=True)
    blance=models.FloatField(default=0.00,blank=True,null=True)
    requested=models.FloatField(default=0.00,blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    date_update=models.DateTimeField(auto_now=True,blank=True,null=True)
    slug=models.SlugField(blank=True,null=True,unique=True,verbose_name=_("Slugfiy"),allow_unicode=True)
    facebook=models.URLField(blank=True,null=True)
    teitter=models.URLField(blank=True,null=True)
    instagram=models.URLField(blank=True,null=True)

    def __str__(self) -> str:
        return self.user.username

    def get_recomended_profile(self):
        queryset=Profile.objects.all()    
        my_records=[]
        for profile in queryset:
            if profile.recomended_by==self.user:
                my_records.append(profile)
        return my_records        

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None or self.slug == "":
            self.slug = slugify(self.user.username, allow_unicode=True)
            qs_exists = Profile.objects.filter(
                slug=self.slug).exists()
            if qs_exists:
                self.slug = create_shortcode(self)
        if self.code is None or self.code == "":
            self.code = f'{self.user}'
        super().save(*args, **kwargs)

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = Profile.objects.create(
              user=kwargs['instance'], )


    post_save.connect(create_profile, sender=User)     


    
class Forget_Password(models.Model):
    email=models.EmailField(max_length=50)



class Skill(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    css=models.BooleanField(default=False)
    html=models.BooleanField(default=False)
    jquery=models.BooleanField(default=False)
    javascripts=models.BooleanField(default=False)
    bootstrap=models.BooleanField(default=False)
    react=models.BooleanField(default=False)
    java=models.BooleanField(default=False)
    python=models.BooleanField(default=False)


    def create_skill(sender, **kwargs):
        if kwargs['created']:
            user_skill = Skill.objects.create(
              user=kwargs['instance'], )


    post_save.connect(create_skill, sender=User)    


class BankAccount(models.Model):
    vendor_profile = models.OneToOneField(
        Profile, on_delete=models.SET_NULL, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True, )
    account_number = models.CharField(max_length=200, blank=True, null=True, )
    swift_code = models.CharField(max_length=200, blank=True, null=True, )
    account_name = models.CharField(max_length=200, blank=True, null=True, )
    country = models.CharField(max_length=200, blank=True, null=True, )
    paypal_email = models.CharField(max_length=200, blank=True, null=True, )
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)