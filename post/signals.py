from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import *


@receiver(post_save,sender=Post)
def send_mail(sender,instance,created,**kwargs):
    if  created:
        print("post created")
        instance1= str(instance.author.email)
        Post.objects.get(id=instance.id)
        # email_template_name = "posttemp.html"
        # c = {
        #     "email": instance.author.email,
            
        # }
        # email = render_to_string(email_template_name, c)
        # send_mail(
        #             'post created',
        #             email,
        #             settings.EMAIL_HOST_USER,
        #             [instance.author.email],
        #             fail_silently=False,
        #         )