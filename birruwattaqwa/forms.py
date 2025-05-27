from django import forms
from .models import Absensi
from .models import JadwalGuru
from .models import ProfilGuru
from .models import LokasiAbsen,Kelas, MataPelajaran
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.models import Group 
from django.contrib.auth.forms import UserCreationForm # Tambahkan ini!


class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = [ 'keterangan', 'status']  # Sesuaikan dengan field yang dibutuhkan
        
class JadwalGuruForm(forms.ModelForm):
    guru = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Guru'),
        label="Guru"
    )

    class Meta:
        model = JadwalGuru
        fields = ['guru', 'hari', 'jam_mulai', 'jam_selesai', 'mata_pelajaran', 'kelas']
        widgets = {
            'jam_mulai': forms.TimeInput(attrs={'type': 'time'}),
            'jam_selesai': forms.TimeInput(attrs={'type': 'time'}),
        }
        


class AdminCreateUserForm(UserCreationForm):
    ROLE_CHOICES = (
        ('Guru', 'Guru'),
        ('Admin', 'Admin'),
    )
    username = forms.CharField(label="Nama Lengkap", max_length=150, required=True)
    email = forms.EmailField(required=True)
    jabatan = forms.CharField(label="Jabatan", max_length=100, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            # Simpan data tambahan di model ProfilGuru
            ProfilGuru.objects.create(
                user=user,
                jabatan=self.cleaned_data['jabatan'],
            )

            # Tambahkan user ke grup sesuai role
            group = Group.objects.get(name=self.cleaned_data['role'])
            user.groups.add(group)

        return user


class LokasiAbsenForm(forms.ModelForm):
    class Meta:
        model = LokasiAbsen
        fields = ['nama_tempat', 'latitude', 'longitude', 'radius_meter']
        


class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ['nama']

class MataPelajaranForm(forms.ModelForm):
    class Meta:
        model = MataPelajaran
        fields = ['nama']
        
class AbsensiManualForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ['guru', 'status', 'keterangan']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    # Override untuk isi bulan dan tahun otomatis
    def save(self, commit=True):
        absensi = super().save(commit=False)
        absensi.bulan = now().strftime('%B')  # Misal: 'Mei'
        absensi.tahun = now().year
        if commit:
            absensi.save()
        return absensi
