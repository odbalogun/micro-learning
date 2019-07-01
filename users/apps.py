from django.apps import AppConfig
# from django.db.models.signals import post_save
# from django.conf import settings

# from .signals import post_save_user_receiver


class UsersConfig(AppConfig):
    name = 'users'
    #
    # def ready(self):
    #     """
    #     Importing signals to ensure they are properly configured
    #     """
    #     import users.signals