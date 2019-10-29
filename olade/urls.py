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
from rest_framework import routers


from users.views import UserLoginView
from courses.api_views import CourseApiViewSet, NewEnrolleeApiViewSet
from discounts.api_views import DiscountApiViewSet


# set up rest framework router
router = routers.DefaultRouter()
router.register(r'courses', CourseApiViewSet)
router.register(r'new-enrollee', base_name='new-enrollee', viewset=NewEnrolleeApiViewSet)
router.register(r'discount', DiscountApiViewSet)

# overwrite admin template variables
admin.site.site_header = 'Olade Administration'                    # default: "Django Administration"
admin.site.index_title = 'Administration'                 # default: "Site administration"
admin.site.site_title = 'Olade site admin'      # default: "Django site admin"

urlpatterns = [
    path('', UserLoginView.as_view()),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
