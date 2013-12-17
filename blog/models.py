from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import re,random
from django.contrib.auth.models import User
from django import forms

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
        for t in __tags.split(','):
            _tag = t.strip()
            if Tag.objects.filter(title=_tag):
                self.tags.add(Tag.objects.get(title=_tag))
            elif _tag:
                t = Tag(title=_tag)
                t.save()
                self.tags.add(t)
            self.save()

    def show_short_body(self):
        short_body=''
        if len(self.body) > 500:
            short_body = self.body[:500] + ' ......'
            return short_body
        else:
            return self.body     

    def show_html_body(self):
        html_text = self.body
        http_link = re.compile(r'http[s]?://[^\s]+')
        http_img = re.compile(r'.jpg|.png|.gif')
        hs = http_link.findall(html_text)
        for h in hs:
            if http_img.search(h):
                img = '<br><img border="0" src="%s" width="600" height="450"><br>' %h
                orl = re.compile(h)
                html_text = orl.sub(img,html_text)
            else:
                text = '<a href="%s">%s</a>' %(h, h)
                orl = re.compile(h)
                html_text = orl.sub(text,html_text)
        line = re.compile(r'\n+')
        html_text = line.sub('<br>',html_text)
        return html_text
                        
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
        
class DocumentForm(forms.Form):
#    title = forms.CharField(max_length=50)
    docfile = forms.FileField(
        label='Select a file'
    )

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    
