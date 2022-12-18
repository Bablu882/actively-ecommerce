from django.db import models

from management.models import User
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=50)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=30)
    highlighted=models.TextField()


    