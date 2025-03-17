from django.urls import path
from django.conf import settings
from birruwattaqwa.views import login_guru, logout_guru, absen_guru, home, scan_qr, generate_qr_code
from django.conf.urls.static import static
from .views import view_absensi, add_absensi
urlpatterns = [
    path('', home, name='home'),  # Redirect ke halaman login
    path('login/', login_guru, name='login'),
    path('logout/', logout_guru, name='logout'),
    path('absen/', absen_guru, name='absen'),
    path('scan/<str:qr_code>/', scan_qr, name='scan_qr'),
    path('generate_qr/', generate_qr_code, name='generate_qr'),
    path('absensi/', view_absensi, name='view_absensi'),
    path('absensi/tambah/', add_absensi, name='add_absensi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)