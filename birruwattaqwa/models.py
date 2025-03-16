from django.db import models
from django.contrib.auth.models import User

class Absensi(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Izin', 'Izin'),
        ('Sakit', 'Sakit'),
        ('Alfa', 'Alfa'),
    ]
    
    guru = models.ForeignKey(User, on_delete=models.CASCADE)  # ID Guru dari User Django
    tanggal = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    keterangan = models.TextField(blank=True, null=True)
    bulan = models.CharField(max_length=10)
    tahun = models.IntegerField()
    jam_absensi = models.TimeField(auto_now_add=True)
    lokasi = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.guru.username} - {self.tanggal} - {self.status}"
