#coding=utf-8
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    views = models.IntegerField(default=0)#定义被浏览的次数
    likes = models.IntegerField(default=0)#define the number of liking 被点击喜欢的次数
    slug = models.SlugField()#slug是标识的意思，设计这个字段是为了更友好标识页面，而不是用id标识

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural="种类"

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __unicode__(self):
        return self.title

    
    class Meta:
        verbose_name_plural="页面"

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(blank=True,upload_to="profile_images")

    def __unicode__(self):
        return self.user.username
    
    
    
