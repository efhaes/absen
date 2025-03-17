from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import Absensi  # Sesuaikan dengan model Absensi-mu

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name == 'birruwattaqwa':  # Sesuaikan dengan nama aplikasimu
        guru_group, created = Group.objects.get_or_create(name='Guru')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        absensi_content_type = ContentType.objects.get_for_model(Absensi)
        permissions = Permission.objects.filter(content_type=absensi_content_type)

        guru_permissions = permissions.filter(codename__in=['view_absensi', 'add_absensi'])
        guru_group.permissions.set(guru_permissions)

        admin_group.permissions.set(permissions)

        print("Grup Guru dan Admin berhasil dibuat atau diperbarui.")
