from django.contrib import admin

# Register your models here.
from constance.admin import ConstanceAdmin, Config
admin.site.unregister([Config])

Config.Meta.verbose_name_plural = 'settings'
Config.Meta.app_label = 'configurations'

admin.site.register([Config], ConstanceAdmin)
