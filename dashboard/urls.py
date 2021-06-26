from django.urls import path

from . import views

urlpatterns = [
    path('state',views.state,name='state'),
    path('city',views.city,name='city'),
    path('vaccination',views.vaccination,name='vaccination'),
    path('covid',views.covid,name='covid'),
    path('', views.home, name='home')
]
