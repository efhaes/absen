from django import forms
from .models import Absensi

class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = [ 'keterangan', 'status']  # Sesuaikan dengan field yang dibutuhkan
