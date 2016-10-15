from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random
import string
from django.contrib.sites.models import Site #for getting the domain name

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name= models.CharField(max_length=40)
    email=models.CharField(max_length=40)
    def __unicode__(self):
        return self.user.username

SHORT_URL_LENGTH = 6

class Url(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    full_url=models.URLField(blank=True)
    short_url=models.URLField(unique=True)
    hit_count=models.IntegerField(default=0)
    def __unicode__(self):
        return self.short_url
        
@receiver(pre_save, sender=Url)
def url_pre_save_callback(sender, instance, *args, **kwargs):
    if not instance.short_url:
        while(1):
            short = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(SHORT_URL_LENGTH))
            if not Url.objects.filter(short_url=short).exists():
                break
        
        current_site=Site.objects.get_current() #added django's site framework in settings.py
        domain_name=current_site.domain    
        instance.short_url = 'https://'+domain_name+'/'+short
    #return short
        
        """def get_shortened_url(self):
            current_site=Site.objects.get_current()
            domain_name=current_site.domain
            #x=request.META['HTTP_HOST']
            short_url=''
            #short_url=x+short
            #strepsil=url_pre_save_callback()
            short_url=domain_name+short"""


    