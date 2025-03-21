from django.contrib import admin
from birruwattaqwa.models import Absensi, JadwalGuru  # Tambahkan JadwalGuru

class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('guru', 'tanggal', 'status', 'keterangan', 'bulan', 'tahun', 'jam_absensi', 'lokasi')
    search_fields = ('guru__username', 'tanggal', 'status', 'qr_code')
    list_filter = ('status', 'bulan', 'tahun')
    ordering = ('-tanggal',)

# Tambahkan konfigurasi untuk JadwalGuru
class JadwalGuruAdmin(admin.ModelAdmin):
    list_display = ('guru', 'hari', 'jam_mulai', 'jam_selesai', 'mata_pelajaran')
    search_fields = ('guru__username', 'mata_pelajaran', 'hari')
    list_filter = ('hari',)

# Daftarkan model ke Django Admin
admin.site.register(Absensi, AbsensiAdmin)
admin.site.register(JadwalGuru, JadwalGuruAdmin)  # Ini penting!

