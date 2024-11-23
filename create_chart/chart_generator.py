import matplotlib.pyplot as plt 
import locale 
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

class chart_generate:
    
    def __init__(self, title_color, title_size,brand):
        self.title_color = title_color
        self.title_size = title_size
        self.marca=brand
    
        
    # VENTAS SEMANALES 
    def create_week_sales(self,weekly):
        # Calcular el porcentaje de crecimiento
        ventas = weekly['venta']
        min_venta = ventas.min() 
        weekly['dato']=weekly['dato'].astype(int)
        semanas = weekly['dato']
        crecimiento = [0] + [(ventas.iloc[i] - ventas.iloc[i - 1]) / ventas.iloc[i - 1] * 100 if ventas.iloc[i - 1] != 0 else 0 
                             for i in range(1, len(ventas))]
    
        fig, ax = plt.subplots(figsize=(10, 6))
    
        ax.bar(semanas, ventas, color='skyblue', alpha=0.7, label="Ventas", width=0.6)
        ax.set_ylim(bottom=min_venta * 0.9)
        # for i, venta in enumerate(ventas):
        # # Coloca el texto fuera de la barra, por la parte de afuera, en el costado derecho de la barra
        #     ax.text(semanas.iloc[i], venta, f"{venta:,.0f}", ha='center', va='center', 
        #         fontsize=8, rotation=90, color='black', position=(semanas.iloc[i] + 0.3, venta))

        
        ax2 = ax.twinx()
        line, = ax2.plot(semanas, [ventas.iloc[i] for i in range(len(ventas))], 
                         color='orange', marker='o', linestyle='-', label="Crecimiento (%)")
    
        for i, porcentaje in enumerate(crecimiento[1:]): 
            color = "green" if porcentaje >= 0 else "red"
            ax2.text(semanas.iloc[i+1], ventas.iloc[i+1]-10.0, f"{porcentaje:.1f}%", 
                     ha='center', va='bottom', fontsize=8, color=color) 
    
        ax.set_title(f"{self.marca} Ventas Semanales y Crecimiento (%)", fontsize=14, color="#16c263", family="serif")
        ax.set_xlabel("Semana")
        ax.set_ylabel("Ventas")
    
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

        ax2.set_yticks([]) 
        
        ax.legend(["Ventas"], loc='upper left', bbox_to_anchor=(1, 1), frameon=False)
        ax2.legend(["Crecimiento (%)"], loc='upper left', bbox_to_anchor=(1, 0.95), frameon=False)

    
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
     
     
    # IMPACTOS VS FACTURAS     
    def create_vs_imp_facturas(self,weekly):
        
        impactos = weekly['impactos']
        facturas = weekly['facturas']
        semana = weekly['dato']
        
        fig, ax = plt.subplots()
        plt.plot(semana, impactos, "o--g" )
        plt.plot(semana, facturas, "s:b" )
        for i in range(len(weekly)):
            ax.text(semana.iloc[i], impactos.iloc[i]-7.0, f"{impactos.iloc[i]}", ha='center', va='top', fontsize=7, color="green")
            ax.text(semana.iloc[i], facturas.iloc[i]+5.0, f"{facturas.iloc[i]}", ha='center', va='bottom', fontsize=7, color="blue")

        plt.legend(["Impactos", "Facturas"])
        plt.title("Ventas vs impactos")
        plt.grid(True)
        plt.show()
        
    def create_categoria(self,categoria):
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Calcular el total de ventas
        total_ventas = categoria['venta'].sum()
        
        # Inicializar el "bottom" para las barras apiladas
        bottom = np.zeros(len(categoria))
        
        # Crear las barras apiladas
        colores = ['skyblue', 'orange', 'green', 'red', 'purple']  # Definir una lista de colores para las categorías
        for i, (col, valor) in enumerate(zip(categoria['dato'], categoria['venta'])):
            ax.bar(categoria['dato'], categoria['venta'], bottom=bottom, color=colores[i % len(colores)], label=col)
            bottom += categoria['venta']  # Actualizar el bottom para apilar la siguiente barra
    
        # Calcular el porcentaje de cada categoría dentro de la barra
        for i, (col, valor) in enumerate(zip(categoria['dato'], categoria['venta'])):
            porcentaje = (valor / total_ventas) * 100
            ax.text(i, bottom[i] - (valor / 2), f"{porcentaje:.1f}%", ha='center', va='center', fontsize=10, color='black')
    
        # Etiquetas y título
        ax.set_title('Distribución de Ventas por Categoria', fontsize=14)
        ax.set_xlabel('Categorías')
        ax.set_ylabel('Ventas Totales')
        ax.legend(title="Categorías", loc='upper left', bbox_to_anchor=(1, 1))
        
        ax.tick_params(axis='x', rotation=45)  # Rota las etiquetas de las categorías si es necesario
    
        # Mostrar la gráfica
        plt.tight_layout()
        plt.show()
        
        