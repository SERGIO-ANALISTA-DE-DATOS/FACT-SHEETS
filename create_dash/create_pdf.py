from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas

class create_pdf:
    def __init__(self,marca,mes,sede,ruta):
        self.marca=marca
        self.mes=mes
        self.sede=sede
        self.filename = ruta 
        self.c = canvas.Canvas(self.filename, pagesize=(960, 540))
     
    def add_diapositiva(self,cover):
        self.c.drawImage(cover, 0, 0, width=960, height=540)
        self.c.showPage() 
    
    def save_pdf(self):
        self.c.save()     