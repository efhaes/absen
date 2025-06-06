# Generated by Django 4.2.7 on 2025-04-29 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyQRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(default=django.utils.timezone.localdate, unique=True)),
                ('qrcode', models.ImageField(upload_to='qr_codes/')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilGuru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jabatan', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JadwalGuru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari', models.CharField(choices=[('Senin', 'Senin'), ('Selasa', 'Selasa'), ('Rabu', 'Rabu'), ('Kamis', 'Kamis'), ('Jumat', 'Jumat'), ('Sabtu', 'Sabtu')], max_length=20)),
                ('jam_mulai', models.DateTimeField()),
                ('jam_selesai', models.DateTimeField()),
                ('mata_pelajaran', models.CharField(choices=[('IPA', 'IPA'), ('IPS', 'IPS'), ('Bahasa Indonesia', 'Bahasa Indonesia'), ('Bahasa Inggris', 'Bahasa Inggris'), ('Bahasa Arab', 'Bahasa Arab'), ('Matematika', 'Matematika'), ('PKN', 'PKN'), ('Seni Budaya', 'Seni Budaya'), ('Penjaskes', 'Penjaskes'), ('Pend. Agama Islam', 'Pend. Agama Islam')], max_length=100)),
                ('kelas', models.CharField(choices=[('1A', '1A'), ('1B', '1B'), ('2A', '2A'), ('2B', '2B'), ('3A', '3A'), ('3B', '3B'), ('4A', '4A'), ('4B', '4B'), ('5A', '5A'), ('5B', '5B'), ('6A', '6A'), ('6B', '6B')], max_length=10)),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Hadir', 'Hadir'), ('Izin', 'Izin'), ('Sakit', 'Sakit'), ('Alfa', 'Alfa')], max_length=10)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('bulan', models.CharField(max_length=20)),
                ('tahun', models.IntegerField()),
                ('jam_absensi', models.TimeField(auto_now_add=True)),
                ('lokasi', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('qrcodes', models.ImageField(blank=True, upload_to='qr_codes/')),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
