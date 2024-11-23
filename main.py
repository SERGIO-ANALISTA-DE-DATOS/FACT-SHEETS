from conectar.extract_data import consult_data
from create_chart.chart_generator import chart_generate
import pandas as pd

marca='SUPER'
mes=[10,11]
sede='bogota'
chart=chart_generate(title_color="darkblue", title_size=12,brand=marca)


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
    return month,weekly,group,fuente,product,category

# clud charts 
month,weekly,group,fuente,product,category=dataframe_exractor(marca,mes,sede)


# Graficas
apiladas=chart.create_categoria(category)
semana=chart.create_week_sales(weekly)
impavsfac=chart.create_vs_imp_facturas(weekly)


# mes=create_week(month,marca)

# grupo=create_week(group,marca)
# fuenteCompra=create_week(fuente,marca)
# producto=create_week(product,marca)
# categoria=create_week(category,marca)












