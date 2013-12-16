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
    
    def create_slug(self):
        if self.slug.strip() == '':
            p = re.compile(r'[^\d\w_-]+')
            self.slug = p.sub('-',self.title[:100]) + str(random.randint(1,999999))
            self.save()
    
    def get_absolute_url(self):
        self.create_slug()
        return reverse('blog:blog_posts',kwargs={'slug':self.slug})
    
    class Meta:
        ordering = ('-creation_date',)

class Post(models.Model):
    blog = models.ForeignKey(Blog)
    tags = models.ManyToManyField('Tag',blank=True)
    title = models.CharField(max_length=150,db_index=True)
    body = models.TextField()
    slug = models.SlugField(max_length=150,db_index=True,editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)    
    modification_date = models.DateTimeField(auto_now=True)    
    
    def __unicode__(self):
        return '%s' %self.title

    def create_slug(self):
        if self.slug.strip() == '':
            p = re.compile(r'[^\d\w_-]+')
            self.slug = p.sub('-',self.title[:100]) + str(random.randint(1,999999))
            self.save()
    
    def add_tags(self,__tags):
        __tags = __tags.strip()
        if __tags =='':
            return
        p = re.compile(r'\s+')
        ts = p.sub(' ',__tags)
        for t in ts.split(' '):
            self.tags.add(t)
        pass     
                        
    def get_absolute_url(self):
        self.create_slug()
        return reverse('blog:post',kwargs={'slug':self.slug})

    class Meta:
        ordering = ('-modification_date',)

class Tag(models.Model):
    title = models.CharField(max_length=50,db_index=True,unique=True)
    slug = models.SlugField(max_length=100,db_index=True,editable=False)    
    
    def __unicode__(self):
        return '%s' %self.title

    def create_slug(self):
        if self.slug.strip() == '':
            p = re.compile(r'[^\d\w_-]+')
            self.slug = p.sub('-',self.title) + str(random.randint(1,999999))
            self.save()

    def get_absolute_url(self):
        self.create_slug()
        return reverse('blog:tag',kwargs={'slug':self.slug})
        
    class Meta:
        ordering = ('title',)
