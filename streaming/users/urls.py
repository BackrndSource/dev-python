from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('acccount', views.cpanel, name='account'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]