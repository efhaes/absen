from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import time
from birruwattaqwa.models import Absensi  # Ganti yourapp sesuai nama aplikasimu

class Command(BaseCommand):
    help = 'Tandai guru yang belum absen sampai jam 9 pagi sebagai Alfa'

    def handle(self, *args, **kwargs):
        today = now().date()
        bulan = now().strftime('%B')
        tahun = now().year
        current_time = now().time()

        batas_waktu = time(9, 0)  # Jam 09:00 pagi

        if current_time < batas_waktu:
            self.stdout.write("Belum jam 9 pagi, belum dilakukan penandaan Alfa.")
            return

        semua_guru = User.objects.filter(groups__name='Guru')
        absensi_hari_ini = Absensi.objects.filter(tanggal=today)
        guru_sudah_absen = absensi_hari_ini.values_list('guru__id', flat=True)

        guru_yang_belum_absen = semua_guru.exclude(id__in=guru_sudah_absen)

        total_ditandai = 0
        for guru in guru_yang_belum_absen:
            # Pastikan belum ditandai Alfa
            sudah_alfa = Absensi.objects.filter(guru=guru, tanggal=today, status="Alfa").exists()
            if not sudah_alfa:
                Absensi.objects.create(
                    guru=guru,
                    tanggal=today,
                    status="Alfa",
                    keterangan="Tidak Hadir (Alpha)",
                    bulan=bulan,
                    tahun=tahun,
                    jam_absensi=now().time(),
                )
                total_ditandai += 1

        self.stdout.write(self.style.SUCCESS(f"{total_ditandai} guru ditandai sebagai Alfa."))
