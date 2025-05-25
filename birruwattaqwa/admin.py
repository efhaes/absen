from django.contrib import admin
from birruwattaqwa.models import Absensi,JadwalGuru,DailyQRCode, LokasiAbsen,MataPelajaran,Kelas # Tambahkan JadwalGuru

class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('guru', 'tanggal', 'status', 'keterangan', 'bulan', 'tahun', 'jam_absensi', 'lokasi', 'latitude', 'longitude')
    search_fields = ('guru__username', 'tanggal', 'status', 'qr_code')
    list_filter = ('status', 'bulan', 'tahun')
    ordering = ('-tanggal',)

# Tambahkan konfigurasi untuk JadwalGuru
class JadwalGuruAdmin(admin.ModelAdmin):
    list_display = ('guru', 'hari', 'jam_mulai', 'jam_selesai', 'mata_pelajaran', 'kelas')
    list_filter = ('hari', 'mata_pelajaran', 'kelas', 'guru')
    search_fields = ('guru__username', 'mata_pelajaran', 'kelas')
    ordering = ('hari', 'jam_mulai')
    
@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')





admin.site.register(LokasiAbsen)
# Daftarkan model ke Django Admin
admin.site.register(Absensi, AbsensiAdmin)
admin.site.register(JadwalGuru, JadwalGuruAdmin)  # Ini penting!
admin.site.register(DailyQRCode)

