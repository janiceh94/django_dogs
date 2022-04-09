from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.About.as_view(), name = 'about'),
    path('dogs/', views.Dog_List.as_view(), name = 'dog_list'),
    path('dogs/new/', views.Dog_Create.as_view(), name="dog_create"),
]