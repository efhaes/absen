import uuid
from datetime import date
from .models import QRCode

def generate_daily_qr_code():
    today = date.today()
    qr_code, created = QRCode.objects.get_or_create(date=today)
    if created:
        qr_code.code = str(uuid.uuid4())
        qr_code.save()
    return qr_code

from django.utils import timezone

today = timezone.localdate()  # Mendapatkan tanggal hari ini
url = f"http://127.0.0.1:8000/absensi/{today}/"