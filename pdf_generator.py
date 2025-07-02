# pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register the Arial font
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))

def generate_pdf(candidate_data: dict, filename: str):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set candidate name
    c.setFont("Arial-Bold", 12)
    text = c.beginText(20, height - 50)
    text.setFont("Arial", 12)
    text.textLines(f"Resume for {candidate_data['name']}")
    c.drawText(text)

    # Set candidate skills
    c.drawString(20, height - 80, f"Skills: {candidate_data['skills']}")

    # Set candidate experience
    c.drawString(20, height - 110, f"Experience: {candidate_data['experience']}")

    c.drawString(20, height - 140, f"Source: {candidate_data['source']}")

    # Save the PDF
    c.save()

