from django.contrib import admin
from django.urls import path
from birruwattaqwa.views import login_guru, logout_guru, absen_guru, home

urlpatterns = [
    path('', home, name='home'),  # Redirect ke halaman login
    path('login/', login_guru, name='login'),
    path('logout/', logout_guru, name='logout'),
    path('absen/', absen_guru, name='absen'),
]