# Generated by Django 4.2.7 on 2025-03-16 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birruwattaqwa', '0002_absensi_qr_code_alter_absensi_bulan_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='absensi',
            old_name='keterangan',
            new_name='alasan_izin',
        ),
        migrations.AddField(
            model_name='absensi',
            name='alasan_sakit',
            field=models.TextField(blank=True, null=True),
        ),
    ]
