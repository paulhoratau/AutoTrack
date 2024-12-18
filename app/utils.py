from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(content):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, content)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
