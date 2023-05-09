from django.urls import path
from .views import homeView, testView

urlpatterns = [
    path('', homeView, name='home'),
    path('hello/', testView, name='test'),
]