from django.urls import path

from . import views

urlpatterns = [
    path('data', views.index, name='index'),
    path('state',views.state,name='state'),
    path('city',views.city,name='city'),
    path('', views.home, name='home')
]
