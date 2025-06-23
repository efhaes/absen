from django.contrib import admin
from birruwattaqwa.models import Absensi,DailyQRCode, LokasiAbsen # Tambahkan JadwalGuru

class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('guru', 'tanggal', 'status', 'keterangan', 'bulan', 'tahun', 'jam_absensi', 'lokasi', 'latitude', 'longitude')
    search_fields = ('guru__username', 'tanggal', 'status', 'qr_code')
    list_filter = ('status', 'bulan', 'tahun')
    ordering = ('-tanggal',)



admin.site.register(LokasiAbsen)
# Daftarkan model ke Django Admin
admin.site.register(Absensi, AbsensiAdmin)

admin.site.register(DailyQRCode)

