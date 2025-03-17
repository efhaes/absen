from django.db import models
from django.contrib.auth.models import User
import uuid

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
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def generate_qr_code(self):
        """Generate QR Code unik berdasarkan guru dan tanggal"""
        self.qr_code = f"ABSEN-{self.guru.id}-{uuid.uuid4().hex[:8]}"
        self.save()

    def __str__(self):
        return f"{self.guru.username} - {self.tanggal} - {self.status}"
