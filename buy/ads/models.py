# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class Advert(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    text = models.TextField()
    category = models.ForeignKey(Category)
    #image_main = models.ImageField(upload_to=".", null=True, blank=True)
    #images = models.ManyToManyField(Image, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    price = models.CharField(null=True, blank=True, max_length=32)
    place = models.CharField(null=True, blank=True, max_length=128)
    #start_price = models.IntegerField(null=True, blank=True)
    is_selled = models.BooleanField()
    #is_auction = models.BooleanField()
    sell = models.BooleanField()
  
    def __unicode__(self):
        return self.name

#class Bet(models.Model):
    #price = models.IntegerField()
    #date = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey(User)
    #advert = models.ForeignKey(Advert)
  
    #def __unicode__(self):
        #return '%s %s' % (self.advert, self.price)
    
class Comment(models.Model):
    advert = models.ForeignKey(Advert)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    text = models.TextField()
    
    def __unicode__(self):
        return 'comment %s %s' % (self.user, self.advert)

class PrivateMessage(models.Model):
    user_from = models.ForeignKey(User, related_name='user_from')
    user_to = models.ForeignKey(User, related_name='user_to')
    created = models.DateField(auto_now_add=True)
    text = models.TextField()
    unread = models.BooleanField()
    
    def __unicode__(self):
        return 'from %s to %s' % (self.user_from, self.user_to)

class News(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    name = models.CharField(max_length=100)
    text = models.TextField()
    
    def __unicode__(self):
        return self.name

class NewsComment(models.Model):
    news = models.ForeignKey(News)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    text = models.TextField()
    
    def __unicode__(self):
        return 'comment %s %s' % (self.user, self.advert)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fullname = models.CharField(max_length=128, blank = True)
    info = models.TextField()
    
    def __unicode__(self):
        return '%s profile' % (self.user.username)