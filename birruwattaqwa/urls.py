from django.urls import path
from django.conf import settings
from birruwattaqwa.views import login_guru, logout_guru, absen_guru, home, scan_qr, generate_qr_code
from django.conf.urls.static import static
from .views import view_absensi
from .views import dashboard_guru, dashboard_admin,redirect_dashboard,jadwal_guru,jadwal_admin,edit_jadwal,create_user,list_users
from .views import  generate_daily_qrcode, generate_admin_qrcode, scan_qr_view, simple_view,rekap_absensi_guru,atur_lokasi
urlpatterns = [
    path('', home, name='home'),  
    path('login/', login_guru, name='login'),
    path('logout/', logout_guru, name='logout'),
    path('absen/', absen_guru, name='absent'),
    path('scan/<str:qr_code>/', scan_qr, name='scan_qr'),
    path('generate_qr/', generate_qr_code, name='generate_qr'),
    path('absensi/', view_absensi, name='list_absen'),
    path('rekap-guru/', rekap_absensi_guru, name='rekap_guru'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
    path('dashboard/guru/', dashboard_guru, name='dashboard_guru'),
    path('dashboard/', redirect_dashboard, name='dashboard'),
    path('jadwal-guru/', jadwal_guru, name='jadwal_guru'),
    path('jadwal-admin/', jadwal_admin, name='jadwal_admin'),
    path('edit-jadwal-ajax/<int:jadwal_id>/', edit_jadwal, name='edit_jadwal_ajax'),
    path('registrasi/', create_user, name='registrasi'),
    path('users/', list_users, name='list_users'),
    path('admin_qrcode/', generate_admin_qrcode, name='generate_admin_qrcode'),
    path('absensi/<str:tanggal>/', generate_daily_qrcode, name='generate_daily_qrcode'),
    path('scan-qr/', scan_qr_view, name='scan_qr_view'),
    path("test-ngrok/",simple_view, name="test_ngrok"),
    path('atur-lokasi/', atur_lokasi, name='atur_lokasi_absen'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)