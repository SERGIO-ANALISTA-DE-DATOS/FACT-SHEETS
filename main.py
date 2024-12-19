from conectar.extract_data import consult_data,quey_embudo
from create_chart.chart_generator import chart_generate
from create_dash.create_pdf import create_pdf
from create_dash.create_html import generate_html
import pandas as pd
import tempfile

marca='ALIMENTOS POLAR COLOMBIA S.A.S.'
mes=[10,11,12]
sede='bogota'
paht="resource/img/matplob/chart_image.png"
chart=chart_generate(title_color="darkblue", title_size=12,brand=marca,sede=sede,path=paht)
dash=create_pdf(marca=marca,mes=mes,sede=sede,ruta= 'resource/pdfs/pdf_final.pdf')
sheet=generate_html(marca=marca,mes=mes,sede=sede)

def dataframe_exractor(marca,mes,sede):
    data,header=consult_data(marca,mes,sede)
    df=pd.DataFrame(data, columns=header)
    df['venta']=df['venta'].astype(float)
    #dividir data
    general=df[df['tipo']=='general']
    df['facturas']=df['facturas'].astype(float)
    month=df[df['tipo']=='mensual']
    weekly=df[df['tipo']=='Semanal']
    group=df[df['tipo']=='grupo']
    fuente=df[df['tipo']=='Fuente']
    product=df[df['tipo']=='articulo']
    category=df[df['tipo']=='categoria']
    day=df[df['tipo']=='day']
    
    
    #embudo: 
    escalon=quey_embudo(marca,mes,sede)
    
    return month,weekly,group,fuente,product,category,day,general,escalon

#main var 
month,weekly,group,fuente,product,category,day,general,escalon=dataframe_exractor(marca,mes,sede)

#totalizado 
total_venta=month['venta'].sum()
tota_facturas=month['facturas'].sum()


cover='resource/img/Local/portada.png'
dash.add_diapositiva(cover)

# pagina 1
# semana,buf = chart.create_week_sales(weekly)
# with open('resource/img/Temporal/ventas_week.png', "wb") as f:
#     f.write(buf.getvalue())

# impavsfac,buf = chart.create_vs_imp_facturas(weekly)
# with open('resource/img/Temporal/impactos_week.png', "wb") as f:
#     f.write(buf.getvalue())

 
# embudo,buf=chart.create_embudo(escalon)    
# with open('resource/img/Temporal/embudo_week.png', "wb") as f:
#     f.write(buf.getvalue())
    

# sheet.pagina_1(semana,impavsfac,general,tota_facturas,total_venta,embudo) 

# pagina 2
headmap,buf=chart.create_headmap(day)
with open('resource/img/Temporal/tabal_caliente.png', "wb") as f:
    f.write(buf.getvalue())
    
chart_fuente,buf = chart.create_chartpie(fuente)
with open('resource/img/Temporal/charpie_fuente.png', "wb") as f:
    f.write(buf.getvalue())   
    
    

sheet.pagina_2(headmap)







# Logica para guardar imagen 


# with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
#     f.write(semana.getvalue())  
#     semana_path = f.name  
# dash.add_diapositiva(semana_path)


# # cloudcode = chart.create_cloud(product)
# # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
# #     f.write(cloudcode.getvalue())
# #     cloudcode_path = f.name
# # dash.add_diapositiva(cloudcode_path)

# apiladas = chart.create_categoria(category)
# with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
#     f.write(apiladas.getvalue())  
#     apiladas_path = f.name  
# dash.add_diapositiva(apiladas_path)






# grupo_tabla= chart.create_table_group(group)
# hmtldash='resource/img/matplob/dashboard_image.png'
# dash.add_diapositiva(hmtldash)


# dash.save_pdf()




# mes=create_week(month,marca)

# grupo=create_week(group,marca)
# fuenteCompra=create_week(fuente,marca)
# producto=create_week(product,marca)
# categoria=create_week(category,marca)












