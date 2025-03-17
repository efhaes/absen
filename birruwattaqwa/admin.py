from django.contrib import admin
# Konfigurasi Admin Django
from birruwattaqwa.models import Absensi

class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('guru', 'tanggal', 'status','keterangan', 'bulan', 'tahun', 'jam_absensi', 'lokasi')
    search_fields = ('guru__username', 'tanggal', 'status','qr_code')
    list_filter = ('status', 'bulan', 'tahun')
    ordering = ('-tanggal',)

admin.site.register(Absensi, AbsensiAdmin)
