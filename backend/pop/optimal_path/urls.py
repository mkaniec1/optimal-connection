from django.urls import path
from . import views

urlpatterns = [
    path('api/connections', views.api_connections),
    path('api/reserve', views.api_reserve),
]
