# Generated by Django 4.2.7 on 2025-04-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birruwattaqwa', '0010_qrcode_alter_absensi_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absensi',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='absensi',
            name='qrcodes',
            field=models.ImageField(blank=True, upload_to='qr_codes/'),
        ),
    ]
