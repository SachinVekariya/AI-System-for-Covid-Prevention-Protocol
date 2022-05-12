"""FYP_ACP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from API import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('help/',views.help,name='help'),
    path('detect/mask_photo/',views.mask_photo,name='mask_photo'),
    path('detect/mask_video/',views.mask_video,name='mask_video'),
    path('detect/mask_temp/',views.mask_temp,name='mask_temp'),
    path('api/',include('API.urls')), 
    path('admin/', admin.site.urls),
]
