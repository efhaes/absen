from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Absensi
from django.conf import settings
from .forms import AbsensiForm
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

    error_message = None  
    form = AbsensiForm()

    if request.method == 'POST':
        form = AbsensiForm(request.POST)

        if form.is_valid():
            status = form.cleaned_data['status']
            keterangan = ""

            # Ambil keterangan berdasarkan status
            if status == "Sakit":
                keterangan = request.POST.get('keterangan', '').strip()
            elif status == "Izin":
                keterangan = request.POST.get('keterangan', '').strip()
            elif status == "Alfa":
                keterangan = "Tidak Hadir (Alpha)"
        
            print(f"Status: {status}, Keterangan: {keterangan}")
            print(f"Data POST: {request.POST}")  

            # Jika sakit atau izin, langsung simpan ke database
            if status in ["Sakit", "Izin"]:
                Absensi.objects.create(
                    guru=user,
                    tanggal=today,
                    status=status,
                    keterangan=keterangan,
                    bulan=bulan,
                    tahun=tahun,
                    jam_absensi=now().time(),
                )
                return redirect('home')

            # Jika hadir atau alfa, cek lokasi
            latitude = request.POST.get('latitude', '').strip()
            longitude = request.POST.get('longitude', '').strip()

            if latitude and longitude:  # Cek apakah lokasi dikirim
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)

                    school_lat = settings.SCHOOL_LOCATION["latitude"]
                    school_lon = settings.SCHOOL_LOCATION["longitude"]

                    # Hitung jarak dengan sekolah dalam meter
                    distance = haversine((latitude, longitude), (school_lat, school_lon), unit=Unit.METERS)

                    if distance > 50:
                        error_message = f"Anda berada di luar area absensi! Jarak: {distance:.2f} meter"
                    else:
                        # Simpan ke database jika dalam radius 50m
                        Absensi.objects.create(
                            guru=user,
                            tanggal=today,
                            status=status,
                            keterangan=keterangan,
                            bulan=bulan,
                            tahun=tahun,
                            jam_absensi=now().time(),
                            latitude=latitude,
                            longitude=longitude
                        )
                        return redirect('home')  

                except ValueError:
                    error_message = "Lokasi tidak valid. Pastikan GPS aktif dan coba lagi."
            else:
                error_message = "Lokasi tidak terdeteksi. Pastikan GPS aktif."

    return render(request, 'birruwattaqwa/absent.html', {
        'qr_code_value': qr_code_value,
        'error_message': error_message,
        'form': form,
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

@login_required
def view_absensi(request):
    user = request.user
    # Cek apakah user adalah Admin atau Guru
    if user.groups.filter(name='Admin').exists():
        absensi_list = Absensi.objects.all()  # Admin melihat semua absensi
    else:
        absensi_list = Absensi.objects.filter(guru=user)  # Guru hanya melihat absensinya sendiri

    return render(request, 'birruwattaqwa/list_absen.html', {'absensi_list': absensi_list})

@login_required
def dashboard_admin(request):
    return render(request, 'birruwattaqwa/dashboard_admin.html')

@login_required
def dashboard_guru(request):
    return render(request, 'birruwattaqwa/dashboard_guru.html')

@login_required
def redirect_dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif request.user.groups.filter(name='Guru').exists():
        return redirect('dashboard_guru')
    else:
        return redirect('home')  # Jika role tidak terdaftar


def login_guru(request):
    """Halaman Login: Setelah login, diarahkan ke halaman absen"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
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