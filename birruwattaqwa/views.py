from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import AdminCreateUserForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import JadwalGuru
from .forms import JadwalGuruForm
from .models import Absensi
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from .forms import AbsensiForm
from .models import ProfilGuru
from django.shortcuts import get_object_or_404
from datetime import date
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import qrcode
import math
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.models import User


from django.http import HttpResponse


lokasi_qr = {"lat": -6.347026500806624, "lon": 106.69148695767142, "radius": 5}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # meter

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

    return render(request, 'birruwattaqwa/guru/absent.html', {
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

from django.contrib.auth.models import User  # Import model User

@login_required
def view_absensi(request):
    user = request.user
    guru_filter = request.GET.get('guru', '')
    search_query = request.GET.get('search', '')

    if user.groups.filter(name='Admin').exists():
        absensi_list = Absensi.objects.all()
        guru_list = User.objects.filter(groups__name='Guru')

        if guru_filter:
            absensi_list = absensi_list.filter(guru__id=guru_filter)
        if search_query:
            absensi_list = absensi_list.filter(keterangan__icontains=search_query)
    else:
        absensi_list = Absensi.objects.filter(guru=user)
        guru_list = None
        if search_query:
            absensi_list = absensi_list.filter(keterangan__icontains=search_query)

    # ✅ Export ke Excel jika diminta
    if 'export' in request.GET:
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=rekap_absensi_{datetime.date.today()}.xlsx'

        wb = Workbook()
        ws = wb.active
        ws.title = "Rekap Absensi"

        # Header style
        headers = ['Nama', 'Tanggal', 'Status', 'Keterangan']
        header_font = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
        header_alignment = Alignment(horizontal='center')

        ws.append(headers)
        for col_num, column_title in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment

        # Data rows
        for absensi in absensi_list:
            ws.append([
                absensi.guru.username,
                absensi.tanggal.strftime("%Y-%m-%d"),
                absensi.status,
                absensi.keterangan
            ])

        # Auto-width kolom
        for column_cells in ws.columns:
            max_length = 0
            column = column_cells[0].column_letter
            for cell in column_cells:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = max_length + 2
            ws.column_dimensions[column].width = adjusted_width

        wb.save(response)
        return response

    return render(request, 'birruwattaqwa/admin/list_absen.html', {
        'absensi_list': absensi_list,
        'guru_list': guru_list,
        'selected_guru': guru_filter,
        'search_query': search_query,
    })


from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Absensi, User  # Pastikan model sudah sesuai

@login_required
def dashboard_admin(request):
    # Dapatkan hari ini
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    # Filter absensi 7 hari terakhir
    absensi_minggu_ini = Absensi.objects.filter(tanggal__range=[seven_days_ago, today])

    # Buat dictionary: tanggal -> jumlah status
    kehadiran_per_hari = {}
    for i in range(7):
        hari = seven_days_ago + timedelta(days=i)
        kehadiran_per_hari[hari.strftime('%d-%m')] = {'Hadir': 0, 'Izin': 0, 'Sakit': 0, 'Alfa': 0}

    for a in absensi_minggu_ini:
        key = a.tanggal.strftime('%d-%m')
        if a.status in kehadiran_per_hari[key]:
            kehadiran_per_hari[key][a.status] += 1

    # Ambil data untuk grafik
    labels = list(kehadiran_per_hari.keys())
    hadir_data = [kehadiran_per_hari[tgl]['Hadir'] for tgl in labels]
    izin_data = [kehadiran_per_hari[tgl]['Izin'] for tgl in labels]
    sakit_data = [kehadiran_per_hari[tgl]['Sakit'] for tgl in labels]
    alfa_data = [kehadiran_per_hari[tgl]['Alfa'] for tgl in labels]

    # Ambil total jumlah guru dan absensi hari ini
    total_guru = User.objects.filter(groups__name='Guru').count()
    total_hadir = Absensi.objects.filter(tanggal=today, status='Hadir').count()
    total_izin = Absensi.objects.filter(tanggal=today, status='Izin').count()
    total_sakit = Absensi.objects.filter(tanggal=today, status='Sakit').count()
    total_alfa = Absensi.objects.filter(tanggal=today, status='Alfa').count()

    # Konteks yang akan diteruskan ke template
    context = {
        # Data untuk grafik
        'labels': labels,
        'hadir_data': hadir_data,
        'izin_data': izin_data,
        'sakit_data': sakit_data,
        'alfa_data': alfa_data,
        # Data untuk statistik kecil
        'total_guru': total_guru,
        'total_izin': total_izin,
        'total_sakit': total_sakit,
        'total_alfa': total_alfa,
        'total_hadir' : total_hadir
    }

    return render(request, 'birruwattaqwa/admin/dashboard_admin.html', context)

@login_required
def dashboard_guru(request):
    return render(request, 'birruwattaqwa/guru/dashboard_guru.html')

@login_required
def redirect_dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif request.user.groups.filter(name='Guru').exists():
        return redirect('dashboard_guru')
    else:
        return redirect('home')  # Jika role tidak terdaftar

@csrf_exempt
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


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())  # Hanya Admin yang bisa akses
def jadwal_admin(request):
    """Admin bisa melihat & menambah jadwal guru dalam satu halaman"""
    if request.method == "POST":
        form = JadwalGuruForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jadwal_admin')  # Refresh halaman agar daftar jadwal update
    else:
        form = JadwalGuruForm()

    jadwal_list = JadwalGuru.objects.all()  # Ambil semua jadwal

    return render(request, 'birruwattaqwa/admin/jadwal_admin.html', {'form': form, 'jadwal_list': jadwal_list})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())  
def edit_jadwal(request, jadwal_id):
    """Admin mengedit jadwal guru"""
    jadwal = get_object_or_404(JadwalGuru, id=jadwal_id)

    if request.method == "POST":
        form = JadwalGuruForm(request.POST, instance=jadwal)
        if form.is_valid():
            form.save()
            return redirect('jadwal_admin')  # Redirect setelah edit
    else:
        form = JadwalGuruForm(instance=jadwal)

    return render(request, 'birruwattaqwa/edit_jadwal.html', {'form': form})


@login_required
def jadwal_guru(request):
    """Guru melihat jadwal yang sudah diposting oleh Admin."""
    jadwal_guru = JadwalGuru.objects.filter(guru=request.user)  # Ambil jadwal untuk user login
    return render(request, 'birruwattaqwa/guru/jadwal_guru.html', {'jadwal_guru': jadwal_guru})




@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())  # Hanya Admin bisa akses
def create_user(request):
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("User akan disimpan:", user.username, user.email)
            user.save()

            # Tambahkan ke grup (buat jika belum ada)
            group, created = Group.objects.get_or_create(name=form.cleaned_data['role'])
            print("Grup ditemukan atau dibuat:", group)
            user.groups.add(group)

            # Simpan data alamat dan jabatan ke model ProfilGuru
            ProfilGuru.objects.create(
                user=user,
                alamat=form.cleaned_data['alamat'],
                jabatan=form.cleaned_data['jabatan']
            )
            print("ProfilGuru berhasil dibuat")

            return redirect('list_users')  # Redirect ke daftar pengguna
        else:
            print("Form tidak valid:", form.errors)
    else:
        form = AdminCreateUserForm()
    
    return render(request, 'registrasi/registrasi.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())  # Hanya Admin bisa akses
def list_users(request):
    users = User.objects.filter(groups__name__in=['Guru', 'Admin'])  # Ambil user dengan role Guru/Admin
    return render(request, 'birruwattaqwa/admin/list_users.html', {'users': users})



# views.py

from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.utils import timezone
from .models import DailyQRCode
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def generate_daily_qrcode(request, tanggal):
    if request.user.groups.filter(name='Guru').exists():
        tanggal = timezone.localdate()

        # Ambil lokasi dari query string
        try:
            lat = float(request.GET.get("lat"))
            lon = float(request.GET.get("lon"))
        except (TypeError, ValueError):
            return HttpResponse("❌ Lokasi tidak valid atau tidak tersedia.")

        # Hitung jarak
        jarak = haversine(lat, lon, lokasi_qr["lat"], lokasi_qr["lon"])
        print(f"Lokasi user: {lat}, {lon}")
        print(f"Lokasi sekolah: {lokasi_qr['lat']}, {lokasi_qr['lon']}")
        print(f"Jarak dihitung: {jarak} meter")
        if jarak > lokasi_qr["radius"]:
            return HttpResponse(f"📍 Kamu terlalu jauh dari lokasi absen. (Jarakmu: {int(jarak)} m)")

        # Cek apakah sudah absen
        if not Absensi.objects.filter(guru=request.user, tanggal=tanggal).exists():
            Absensi.objects.create(
                guru=request.user,
                tanggal=tanggal,
                tahun=tanggal.year,
                bulan=tanggal.strftime("%B"),
                status="Hadir",
                keterangan="Absen via QR"
            )
            return HttpResponse("✅ Absensi berhasil tercatat.")
        else:
            return HttpResponse("⚠️ Kamu sudah absen hari ini.")
    
    return HttpResponse("❌ Hanya guru yang bisa absen lewat QR code.")


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())  # Cuma admin bisa akses
def generate_admin_qrcode(request):
    today = timezone.localdate()
    daily_qr, created = DailyQRCode.objects.get_or_create(tanggal=today)
    if created or not daily_qr.qrcode:
        # Gunakan URL lokal atau URL absensi yang valid
        url = request.build_absolute_uri(f"/absensi/{today}/")
        qr_img = qrcode.make(url)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        daily_qr.qrcode.save(f'qr_{today}.png', ContentFile(buffer.getvalue()))
        daily_qr.save()
    return render(request, 'birruwattaqwa/admin/admin_qrcode.html', {'daily_qr': daily_qr})

@login_required
def scan_qr_view(request):
    return render(request, 'qrcodes.html')


def simple_view(request):
    return HttpResponse("Hello Ngrok!")









