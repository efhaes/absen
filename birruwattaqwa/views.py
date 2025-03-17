from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Absensi
from django.conf import settings

import math

def haversine(lat1, lon1, lat2, lon2):
    """Menghitung jarak antara dua titik koordinat dalam meter."""
    R = 6371  # Radius bumi dalam km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c * 1000  # Konversi ke meter

@login_required
def absen_guru(request):
    user = request.user  
    today = now().date()
    bulan, tahun = now().strftime('%B'), now().year
    qr_code_value = f"ABSEN-{today}"  # QR unik per hari

    error_message = None  # Untuk pesan error jika di luar radius

    if request.method == 'POST':
        status = request.POST.get('status')
        keterangan = ""

        # Ambil alasan jika sakit atau izin
        if status == "Sakit":
            keterangan = request.POST.get('keterangan_sakit', '').strip()
        elif status == "Izin":
            keterangan = request.POST.get('keterangan_izin', '').strip()
        elif status == "Alfa":
            keterangan = "Tidak Hadir (Alpha)"

        # Ambil lokasi dari POST
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)

        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            # Ambil koordinat sekolah dari settings.py
            school_lat = settings.SCHOOL_LOCATION["latitude"]
            school_lon = settings.SCHOOL_LOCATION["longitude"]

            # Hitung jarak pengguna dengan sekolah
            distance = haversine(latitude, longitude, school_lat, school_lon)

            # Jika lebih dari 50 meter, beri peringatan
            if distance > 50:
                error_message = "Anda berada di luar area absensi! Jarak: {:.2f} meter".format(distance)
            else:
                # Simpan absensi jika dalam radius 50m
                Absensi.objects.create(
                    guru=user,
                    tanggal=today,
                    status=status,
                    keterangan=keterangan,
                    bulan=bulan,
                    tahun=tahun,
                    jam_absensi=now().time(),
                    lokasi=f"{latitude}, {longitude}"
                )
                return redirect('home')  

    return render(request, 'birruwattaqwa/absen.html', {
        'qr_code_value': qr_code_value,
        'error_message': error_message
    })

@login_required
def scan_qr(request, qr_code):
    """Verifikasi QR Code untuk mencatat kehadiran"""
    today = now().strftime('%Y-%m-%d')
    expected_code = f"ABSEN-{today}"

    if qr_code == expected_code:
        Absensi.objects.create(
            guru=request.user,
            tanggal=now().date(),
            status="Hadir",
            bulan=now().strftime('%B'),
            tahun=now().year,
            jam_absensi=now().time(),
            lokasi="Sekolah"
        )
        return JsonResponse({"message": "Absensi berhasil!"})
    
    return JsonResponse({"error": "QR Code tidak valid!"})

def login_guru(request):
    """Halaman Login: Setelah login, diarahkan ke halaman absen"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('absen')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'registrasi/login.html')

def generate_qr_code(request):
    """Mengembalikan QR Code unik per hari dalam bentuk JSON"""
    today = now().strftime('%Y-%m-%d')
    qr_code_value = f"ABSEN-{today}"
    return JsonResponse({"qr_code_value": qr_code_value})

def logout_guru(request):
    """Logout dan kembali ke halaman home"""
    logout(request)
    return redirect('home')


def home(request):
    """Halaman Home: Bisa diakses semua orang"""
    
    return render(request, 'home.html')