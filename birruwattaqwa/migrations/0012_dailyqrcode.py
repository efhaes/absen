# Generated by Django 4.2.7 on 2025-04-05 16:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('birruwattaqwa', '0011_remove_absensi_qr_code_absensi_qrcodes'),
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
    ]
