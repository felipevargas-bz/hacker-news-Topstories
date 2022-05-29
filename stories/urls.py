from django.urls import path
from stories import views

urlpatterns = [
    path('', views.stories),
]
