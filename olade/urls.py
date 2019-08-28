"""olade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import UserLoginView

# overwrite admin template variables
admin.site.site_header = 'Olade Administration'                    # default: "Django Administration"
admin.site.index_title = 'Administration'                 # default: "Site administration"
admin.site.site_title = 'Olade site admin'      # default: "Django site admin"

urlpatterns = [
    path('', UserLoginView.as_view()),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('payments/', include('payments.urls', namespace='payments')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
