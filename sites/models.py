from django.db import models

# Create your models here.


class Sites(models.Model):
    site_name=models.CharField(max_length=100,blank=True,null=True)
    site_title=models.CharField(max_length=100,blank=True,null=True)
    site_discription=models.CharField(max_length=500,blank=True,null=True)
    site_address=models.CharField(max_length=200,blank=True,null=True)
    site_url=models.URLField(blank=True,null=True)
    site_logo=models.ImageField(blank=True,null=True,upload_to='sites/images')
    site_favicon=models.ImageField(blank=True,null=True,upload_to='sites/images')
    site_form_image=models.ImageField(blank=True,null=True,upload_to='sites/images')
    site_contect_no1=models.CharField(max_length=20,blank=True,null=True)
    site_contect_no2=models.CharField(max_length=20,blank=True,null=True)
    site_work_time=models.CharField(max_length=100,blank=True,null=True)
    site_email=models.EmailField(blank=True,null=True)
    site_facebook=models.URLField(blank=True,null=True)
    site_instagram=models.URLField(blank=True,null=True)
    site_twitter=models.URLField(blank=True,null=True)
    site_youtube=models.URLField(blank=True,null=True)