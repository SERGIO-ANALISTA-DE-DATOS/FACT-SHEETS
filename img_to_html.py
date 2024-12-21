from html2image import Html2Image
import time

# Configuración del convertidor
hti = Html2Image(output_path='resource/img/matplob')
time.sleep(2)

html_file = "resource/html/hoja_1.html"
time.sleep(2)

# Generar imagen desde HTML
hti.screenshot(
    html_file=html_file,
    save_as="dashboard_image.png",
    size=(1300, 930) 
)

print("Imagen generada correctamente.")
