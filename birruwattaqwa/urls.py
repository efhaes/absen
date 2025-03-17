from django.urls import path
from django.conf import settings
from birruwattaqwa.views import login_guru, logout_guru, absen_guru, home, scan_qr, generate_qr_code
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  # Redirect ke halaman login
    path('login/', login_guru, name='login'),
    path('logout/', logout_guru, name='logout'),
    path('absen/', absen_guru, name='absen'),
    path('scan/<str:qr_code>/', scan_qr, name='scan_qr'),
    path('generate_qr/', generate_qr_code, name='generate_qr'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)