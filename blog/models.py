from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import re
# Create your models here.

def validate_letter(value):
    p = re.compile(r'^[\d\w_]{1,30}$')
    if p.match(value) == None:
        raise ValidationError("The number of letters of Username must less than 30 and letters can only have digital, letter and '_'.")

class User(models.Model):
    #can only have digital, letter and '_' 
    name = models.CharField(max_length=30,db_index=True,unique=True,validators=[validate_letter])
    password = models.CharField(max_length=20)


class Blog(models.Model):
    # a user can create many blogs
    user = models.ForeignKey(User)
    


class Post(models.Model):
    
    blog = models.ForeignKey(Blog)
