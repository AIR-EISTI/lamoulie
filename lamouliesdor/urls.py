"""lamouliesdor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from polls import views

urlpatterns = [
    path('', views.home, name='home'),
    path('answers/', views.postAnswer, name='postAnswer'),
    path('answers/question/<int:pk>/', views.delAnswer, name='delAnswer'),
    path('stats/', views.stats, name='stats'),
    path('stats/question/<int:pk>/', views.getQuestionResults, name='getQuestionResults'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social'))
]
