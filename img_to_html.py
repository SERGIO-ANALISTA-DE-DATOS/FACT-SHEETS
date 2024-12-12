from html2image import Html2Image

# Configuración del convertidor
hti = Html2Image(output_path='resource/img/matplob')


html_file = "dashboard.html"

# Generar imagen desde HTML
hti.screenshot(
    html_file=html_file,
    save_as="dashboard_image.png",
    size=(1400, 750) 
)

print("Imagen generada correctamente.")
