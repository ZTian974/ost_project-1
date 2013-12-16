from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import re,random
from django.contrib.auth.models import User

class Blog(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=150,db_index=True)
    slug = models.SlugField(max_length=150,db_index=True,editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s' %self.title
    
    def get_absolute_url(self):
        if self.slug.strip() == '':
            p = re.compile(r'[^\d\w_-]+')
            self.slug = p.sub('-',self.title) + str(random.randint(1,999999))
            #don't forget save
            self.save()
        return reverse('blog:blog_posts',kwargs={'slug':self.slug})
    
    class Meta:
        ordering = ('-creation_date',)

class Post(models.Model):
    blog = models.ForeignKey(Blog)
    tags = models.ManyToManyField('Tag',blank=True)
    title = models.CharField(max_length=150,db_index=True)
    body = models.TextField()
    slug = models.SlugField(max_length=150,db_index=True)
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
