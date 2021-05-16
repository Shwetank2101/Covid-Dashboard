from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('covid',views.covid, name='covid')
]