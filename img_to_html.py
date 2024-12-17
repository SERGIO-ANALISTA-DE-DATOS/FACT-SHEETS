from html2image import Html2Image
import time

# Configuración del convertidor
hti = Html2Image(output_path='resource/img/matplob')


html_file = "resource/html/hoja_1.html"
time.sleep(3)

# Generar imagen desde HTML
hti.screenshot(
    html_file=html_file,
    save_as="dashboard_image.png",
    size=(1200, 650) 
)

print("Imagen generada correctamente.")
