from conectar.extract_data import consult_data
from create_chart.chart_generator import chart_generate
from create_dash.create_pdf import create_pdf
import pandas as pd
import tempfile

marca='SUPER'
mes=[10,11,12]
sede='bogota'
paht="resource/img/matplob/chart_image.png"
chart=chart_generate(title_color="darkblue", title_size=12,brand=marca,sede=sede,path=paht)
dash=create_pdf(marca=marca,mes=mes,sede=sede,ruta= 'resource/pdfs/pdf_final.pdf')


def dataframe_exractor(marca,mes,sede):
    data,header=consult_data(marca,mes,sede)
    df=pd.DataFrame(data, columns=header)
    df['venta']=df['venta'].astype(float)
    #dividir data
    month=df[df['tipo']=='mensual']
    weekly=df[df['tipo']=='Semanal']
    group=df[df['tipo']=='grupo']
    fuente=df[df['tipo']=='Fuente']
    product=df[df['tipo']=='articulo']
    category=df[df['tipo']=='categoria']
    day=df[df['tipo']=='day']
    return month,weekly,group,fuente,product,category,day

# clud charts 
month,weekly,group,fuente,product,category,day=dataframe_exractor(marca,mes,sede)

cover='resource/img/Local/portada.png'
dash.add_diapositiva(cover)

# Graficas
semana = chart.create_week_sales(weekly)
with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
    f.write(semana.getvalue())  
    semana_path = f.name  
dash.add_diapositiva(semana_path)

impavsfac = chart.create_vs_imp_facturas(weekly)
with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
    f.write(impavsfac.getvalue())  
    impavsfac_path = f.name  
dash.add_diapositiva(impavsfac_path)

chart_fuente = chart.create_chartpie(fuente)
with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
    f.write(chart_fuente.getvalue())  
    chart_fuente_path = f.name  
dash.add_diapositiva(chart_fuente_path)

# cloudcode = chart.create_cloud(product)
# with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
#     f.write(cloudcode.getvalue())
#     cloudcode_path = f.name
# dash.add_diapositiva(cloudcode_path)

apiladas = chart.create_categoria(category)
with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
    f.write(apiladas.getvalue())  
    apiladas_path = f.name  
dash.add_diapositiva(apiladas_path)



table_hot=chart.create_headmap(day)

dash.save_pdf()




# mes=create_week(month,marca)

# grupo=create_week(group,marca)
# fuenteCompra=create_week(fuente,marca)
# producto=create_week(product,marca)
# categoria=create_week(category,marca)












