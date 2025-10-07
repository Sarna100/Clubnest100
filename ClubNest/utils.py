# ClubNest/utils.py
from io import BytesIO
from django.core.files import File
from reportlab.pdfgen import canvas
from .models import Certificate

def generate_certificate(cert):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(595, 842))  # A4 size

    participation = cert.participation
    user = participation.user
    event = participation.event

    # PDF content
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(300, 700, "Certificate of Participation")
    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 650, f"Awarded to: {user.get_full_name() or user.username}")
    c.drawCentredString(300, 620, f"For participating in event: {event.title}")
    c.drawCentredString(300, 590, f"Date: {event.date.strftime('%d-%m-%Y')}")

    c.showPage()
    c.save()

    buffer.seek(0)
    cert.pdf_file.save(f"certificate_{participation.id}.pdf", File(buffer), save=True)
