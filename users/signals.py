from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def post_save_user_receiver(sender, instance, created, **kwargs):
    """
    Send an email to users, created by admins, with their passwords
    """
    print("got here")
    if instance.created_by:
        print(instance._password)
        instance.email_user(subject="Your account has been created", title="Your account has been created", 
                        subtitle="Your account has been created", 
                        content="Your Olade has been created. Your password is {}".format(instance._password))


# post_save.connect(post_save_user_receiver, sender='users.User')
