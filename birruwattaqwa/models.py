from django.db import models
from django.contrib.auth.models import User
from datetime import date
import uuid
from django.db import models
from django.utils import timezone

class Absensi(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Izin', 'Izin'),
        ('Sakit', 'Sakit'),
        ('Alfa', 'Alfa'),
    ]
    guru = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    keterangan = models.TextField(blank=True, null=True)  # Keterangan umum
    bulan = models.CharField(max_length=20)  # Simpan bulan sebagai nama, bukan angka 
    tahun = models.IntegerField()
    jam_absensi = models.TimeField(auto_now_add=True)
    lokasi = models.CharField(max_length=255, blank=True, null=True)  
    latitude = models.FloatField(blank=True, null=True)  # Tambahkan ini
    longitude = models.FloatField(blank=True, null=True)  # Tambahkan ini
    qrcodes = models.ImageField(upload_to='qr_codes/', blank=True)
  

    def generate_qr_code(self):
        """Generate QR Code unik berdasarkan guru dan tanggal"""
        self.qr_code = f"ABSEN-{self.guru.id}-{uuid.uuid4().hex[:8]}"
        self.save()

    def __str__(self):
        return f"{self.guru.username} - {self.tanggal} - {self.status}"
    
class MataPelajaran(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class Kelas(models.Model):
    nama = models.CharField(max_length=20)

    def __str__(self):
        return self.nama


class JadwalGuru(models.Model):
    HARI_CHOICES = [
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
    ]

    guru = models.ForeignKey(User, on_delete=models.CASCADE)
    hari = models.CharField(max_length=20, choices=HARI_CHOICES)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.guru.username} - {self.hari} - {self.mata_pelajaran.nama} - {self.kelas.nama}"
    
class ProfilGuru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    jabatan = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.user.username




class DailyQRCode(models.Model):
    tanggal = models.DateField(default=timezone.localdate, unique=True)
    qrcode = models.ImageField(upload_to='qr_codes/')
    
    def __str__(self):
        return f"QR Code {self.tanggal}"
    
class LokasiAbsen(models.Model):
    nama_tempat = models.CharField(max_length=100, default='Sekolah')
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius_meter = models.IntegerField(default=50)  # radius area absensi dalam meter

    def __str__(self):
        return f"{self.nama_tempat} ({self.latitude}, {self.longitude})"
