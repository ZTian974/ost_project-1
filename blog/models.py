from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import re
# Create your models here.

def validate_letter(value):
    # can only have digital, letter and '_'
    p = re.compile(r'^[\d\w_]{1,30}$')
    if p.match(value) == None:
        raise ValidationError("The number of letters of Username must less than 30 and letters can only have digital, letter and '_'.")

class User(models.Model):
    username = models.CharField(max_length=30,db_index=True,unique=True, validators=[validate_letter])
    password = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s' %self.name
        
    def get_absolute_url(self):
        pass
#        return reverse('blog:view_blog_category', kwargs={'username':self.username})

class Blog(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=150,db_index=True)
    slug = models.CharField(max_length=150,db_index=True, validators=[validate_letter])
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s' %self.title

    def get_absolute_url(self):
        if slug.strip() == '':
            slug = title.replace()
        pass
    
    class Meta:
        ordering = ('-creation_date',)

class Post(models.Model):
    blog = models.ForeignKey(Blog)
    tags = models.ManyToManyField('Tag',blank=True)
    title = models.CharField(max_length=150,db_index=True)
    body = models.TextField()
    slug = models.CharField(max_length=150,db_index=True, validators=[validate_letter])
    creation_date = models.DateTimeField(auto_now_add=True)    
    modification_date = models.DateTimeField(auto_now=True)    
    
    def __unicode__(self):
        return '%s' %self.title

    def get_absolute_url(self):
        pass

    class Meta:
        ordering = ('-modification_date',)

class Tag(models.Model):
    title = models.CharField(max_length=50,db_index=True)

    def __unicode__(self):
        return '%s' %self.title

    def get_absolute_url(self):
        pass
        
    class Meta:
        ordering = ('title',)
