from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Absensi
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return redirect('home')  # Jika sudah login, arahkan ke dashboard
    return render(request, 'home.html')  # Pastikan path sesuai dengan struktur folder

def get_current_month_year():
    
    return now().strftime('%B'), now().year



def login_guru(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'registrasi/login.html')
@login_required
def logout_guru(request):
    logout(request)  # Logout user yang sedang aktif
    return redirect('home')
