import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import seaborn as sns
import io
from matplotlib.table import Table
import base64


class chart_generate:
    
    def __init__(self, title_color, title_size,brand,sede,path):
        self.title_color = title_color
        self.title_size = title_size
        self.marca=brand
        self.sede=sede
        self.paht=path
        
            
    # VENTAS SEMANALES 
    def create_week_sales(self,weekly):
        ventas = weekly['venta']
        min_venta = ventas.min()
        max_venta = ventas.max() 
        weekly['dato']=weekly['dato'].astype(int)
        semanas = weekly['dato']
        crecimiento = [0] + [(ventas.iloc[i] - ventas.iloc[i - 1]) / ventas.iloc[i - 1] * 100 if ventas.iloc[i - 1] != 0 else 0 
                             for i in range(1, len(ventas))]
    
        fig, ax = plt.subplots(figsize=(10, 6))
    
        ax.bar(semanas, ventas, color='skyblue', alpha=0.7, label="Ventas", width=0.6)
        ax.set_ylim(bottom=min_venta * 0.9) 
        ax2 = ax.twinx()
        line, = ax2.plot(semanas, [ventas.iloc[i] for i in range(len(ventas))], 
                         color='orange', marker='o', linestyle='-', label="Crecimiento(%)  ")
    
        for i, porcentaje in enumerate(crecimiento[1:]): 
            color = "green" if porcentaje >= 0 else "red"
            ax2.text(semanas.iloc[i+1], ventas.iloc[i+1]-10.0, f"{porcentaje:.1f}%", 
                     ha='center', va='bottom', fontsize=8, color=color) 
    
        ax.set_title(f" Ventas Semanales", fontsize=14, family="serif")
        ax.set_xlabel("Semana")
        # ax.set_ylabel("Ventas") papu be in title
    
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1_000_000:,.1f} M"))
        ax.set_xticks(semanas) 

                
        ax2.set_yticks([]) 
        ax.legend(loc='upper right', frameon=False)
        ax2.legend(loc='upper right', bbox_to_anchor=(0.9, 1.0), frameon=False)


        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Deshabilitar eje Y secundario completamente
        ax2.set_yticks([])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        ax.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close() 
        buf.seek(0) 
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64,buf
     
     
    # IMPACTOS VS FACTURAS     
    def create_vs_imp_facturas(self,weekly):
        
        impactos = weekly['impactos']
        facturas = weekly['facturas']
        facturas = facturas.astype(int) 
        semana = weekly['dato']
        
        fig, ax = plt.subplots()
        plt.plot(semana, impactos, "o--g" )
        plt.plot(semana, facturas, "s:b" )
        for i in range(len(weekly)):
            ax.text(semana.iloc[i], impactos.iloc[i]-7.0, f"{impactos.iloc[i]}", ha='center', va='top', fontsize=7, color="green")
            ax.text(semana.iloc[i], facturas.iloc[i]+5.0, f"{facturas.iloc[i]}", ha='center', va='bottom', fontsize=7, color="blue")

        plt.legend(["Impactos", "Facturas"])
        plt.title("Facturas & impactos")
        ax.set_xlabel("Semana")
        plt.grid(True)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0) 
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64,buf
    
    # CATEGORIAS MAS VENDIDAS
    def procesar_categorias(self, categoria, porcentaje_minimo=5, max_categorias=5):
        total_ventas = categoria['venta'].sum()
        categoria['porcentaje'] = (categoria['venta'] / total_ventas) * 100

        # Ordenar por ventas
        categoria = categoria.sort_values(by='venta', ascending=False)

        # Verificar si se necesita el grupo "Otros"
        if len(categoria) > max_categorias:
            principales = categoria.head(max_categorias)
            otras = categoria[max_categorias:]

            if not otras.empty:
                otras_ventas = otras['venta'].sum()
                otras_porcentaje = otras['porcentaje'].sum()
                principales = pd.concat([principales, pd.DataFrame({
                    'dato': ['Otros'],
                    'venta': [otras_ventas],
                    'porcentaje': [otras_porcentaje]
                })], ignore_index=True)
        else:
            principales = categoria

        return principales

    def create_categoria_apilada(self, categoria):
        fig, ax = plt.subplots(figsize=(8, 6))

        categoria = categoria.reset_index(drop=True)

        bottom = 0
        colores = ['skyblue', 'orange', 'green', 'red', 'purple', 'gray']  # Colores de las categorías
        for i, (col, valor) in enumerate(zip(categoria['dato'], categoria['venta'])):
            ax.bar(
                "Total Ventas", valor, bottom=bottom, color=colores[i % len(colores)], label=col
            )
            bottom += valor
            porcentaje = categoria.loc[i, 'porcentaje']
            ax.text(
                0, bottom - (valor / 2), f"{porcentaje:.1f}%", ha='center', va='center', fontsize=10, color='black'
            )
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        ax.set_title('Ventas por Categoría', fontsize=14)
        ax.set_ylabel('Ventas Totales')
        ax.legend(title="Categorías", loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()
        # plt.show()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')  
        buf.seek(0) 
        plt.close(fig)
        return buf


    def create_categoria(self, categoria):
        df_procesado = self.procesar_categorias(categoria, porcentaje_minimo=5, max_categorias=5)

        return self.create_categoria_apilada(df_procesado)
        
    
    #GRAFICO DE EMBUDO
    def create_embudo(self, escalones):
        valores = escalones[::-1]
        etapas = ['Maestra', 'Pidieron', 'Compra', 
                  '+3 pedidos', '+5 pedidos'][::-1]
        fig, ax = plt.subplots(figsize=(10, 6))
        
        width = np.array([0.9, 0.8, 0.7, 0.6, 0.5])[::-1] * max(valores)
        y_pos = np.arange(len(etapas)) * 0.9
        
        left = (max(valores) - width) / 2
        
        valor_inicial = valores[-1]
        
        bars = ax.barh(y_pos, width, left=left, height=0.8, 
                      color=['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f1c40f'])
        
        for i, bar in enumerate(bars):
            ax.text(-0.1, y_pos[i], etapas[i], 
                   ha='right', va='center', fontsize=10)
            
            ax.text(max(valores)/2, y_pos[i], f'{valores[i]:,}', 
                   ha='center', va='center', fontweight='bold', color='white')
            
            if i < len(valores) - 1: 
                porcentaje = (valores[i] / valor_inicial) * 100
                ax.text(max(valores) + 100, y_pos[i], 
                       f'↓{porcentaje:.1f}%', ha='left', va='center', 
                       color='#7f8c8d', fontsize=9)

        ax.set_xlim(-max(valores)*0.3, max(valores)*1.2)
        ax.set_ylim(-0.5, max(y_pos) + 0.5)
        
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        plt.title('Análisis de Embudo', pad=20, fontsize=14)
        
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0) 
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64,buf
         
    
        
    # CLOUD      
    def create_cloud(self, producto):
        cadena = " ".join([f"{row['dato']} " * int(row['impactos']) for _, row in producto.iterrows()])
        x, y = np.ogrid[:800, :800]  
        mask = (x - 400) ** 2 + (y - 400) ** 2 > 350 ** 2  
        mask = 255 * mask.astype(int) 

        nube = WordCloud(
            width=800,
            height=800,
            background_color="white",
            colormap="viridis",
            mask=mask
        ).generate(cadena)

        plt.figure(figsize=(8, 8))
        plt.imshow(nube, interpolation='bilinear')
        plt.axis("off")
        plt.title("Nube de palabras en forma de círculo", fontsize=16)
        # plt.show()

     
    #TORTA DE FUENTE
    def create_chartpie(self, fuente):
        if self.sede == "boyaca":
            categorias = [
                "SERVIMAX ASESORES",
                "TENDEROS", 
                "WHATSAPP",
                "otros"
            ]
            tenderos_categorias = [
                "SERVIMAX TENDEROS FRECUENCIA NORMAL",
            ]
        else:  # Bogotá
            categorias = [
                "SERVIMAX ASESORES",
                "TENDEROS",  
                "WHATSAPP",
                "otros"
            ]
            tenderos_categorias = [
                "SERVIMAX TENDEROS FRECUENCIA NORMAL",
                "SERVIMAX TENDEROS EXPRESS"
            ]
        colores = {
            "SERVIMAX ASESORES": "#df0d13",  
            "TENDEROS": "#16c263",
            "WHATSAPP": "#1e90ff", 
            "otros": "#ffd700",  
        }

        def categorizar(dato):
            if dato in tenderos_categorias:
                return "TENDEROS"
            elif dato == "WHATSAPP":
                return "WHATSAPP"
            elif dato in categorias:
                return dato
            else:
                return "otros"

        fuente["categoria"] = fuente["dato"].apply(categorizar)
        
        totales_por_categoria = fuente.groupby("categoria")[["venta", "impactos", "facturas"]].sum()

        for categoria in categorias:
            if categoria not in totales_por_categoria.index:
                totales_por_categoria.loc[categoria] = [0, 0, 0]

        total_ventas = totales_por_categoria["venta"].sum()
        total_impactos = totales_por_categoria["impactos"].sum()
        total_facturas = totales_por_categoria["facturas"].sum()

        fig, axes = plt.subplots(3, 4, figsize=(10, 8), gridspec_kw={'wspace': 0.0, 'hspace':0.0})
        # plt.subplots_adjust(left=0.94, right=0.95, bottom=0.1, top=0.9, hspace=0.4, wspace=0.3)
        metricas = ["venta", "impactos", "facturas"]
        totales_globales = [total_ventas, total_impactos, total_facturas]
        titulos_metricas = ["VENTA  ", "IMPACTOS", "FACTURAS"]
        for i, metrica in enumerate(metricas):
            fig.text(0.02, 0.80 - i * 0.3, titulos_metricas[i], va='center', ha='right', fontsize=12)
            total_global = totales_globales[i]
            vnt = True if i == 0 else False
            for j, categoria in enumerate(categorias):
                valor_actual = totales_por_categoria.at[categoria, metrica]
                porcentaje = (valor_actual / total_global * 100) if total_global > 0 else 0
                ax = axes[i, j]
                ax.clear()
                if valor_actual == 0:
                    ax.pie(
                        [100],
                        colors=["#d3d3d3"], 
                        startangle=90,
                        wedgeprops={"width": 0.3}
                    )
                else:
                    ax.pie(
                        [porcentaje, 100 - porcentaje],
                        colors=[colores[categoria], "#d3d3d3"],
                        startangle=90,
                        counterclock=False,
                        wedgeprops={"width": 0.3}
                    )

                if vnt:
                    ax.set_title(categoria, fontsize=10, pad=15)
                ax.text(
                    0, 0,
                    f'${int(valor_actual):,}' if vnt else f'{int(valor_actual)}',
                    fontsize=12, ha="center", va="center", color="black"
                )
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0) 
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64,buf

    #SEMNAL DIAS HEADMAP
    def create_headmap(self,day):
        spanglis = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
            }
        day['dato']=day['dato'].map(spanglis)
        day.rename(columns={'impactos': 'semana'}, inplace=True)
        
        heatmap_data = day.pivot_table(
        index='semana',
        columns='dato',
        values='venta',
        aggfunc='sum' 
        )
        dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        heatmap_data = heatmap_data[dias_orden]

        plt.figure(figsize=(12, 8))

        formatted_data = heatmap_data.apply(
            lambda row: [f"$ {x:,.0f}" if pd.notnull(x) else "" for x in row], axis=1
        )
        formatted_data = pd.DataFrame(formatted_data.tolist(), index=heatmap_data.index, columns=heatmap_data.columns)

        formatter = mticker.FuncFormatter(lambda x, p: f'{x/1000000:.1f}M')

        sns.heatmap(
            heatmap_data,
            annot=formatted_data,
            fmt="",
            cmap="YlGnBu",
            linewidths=.5,
            cbar_kws={
                'label': 'Ventas',
                'format': formatter  
            }
        )
        plt.title("Mapa de Calor de Ventas", fontsize=16)
        plt.xlabel("", fontsize=12) 
        plt.xticks(rotation=45, ha='right')  
        plt.gca().xaxis.tick_top()  
        plt.ylabel("Semanas", fontsize=12)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0) 
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64,buf
      
    #Tabla de grupo        
    def create_table_group(self,grupo):
        fig, ax = plt.subplots(figsize=(10, len(grupo) * 0.8))
        ax.axis('off')
        table = Table(ax, bbox=[0, 0, 1, 1])

        column_labels = ["Grupo", "Venta", "Impactos", "Facturas", "Ticket"]
        col_widths = [0.2, 0.3, 0.2, 0.2, 0.2]

        for col_idx, label in enumerate(column_labels):
            cell = table.add_cell(-1, col_idx, width=col_widths[col_idx], height=0.4, 
                                  text=label, loc='center', facecolor='#40466e')
            cell.get_text().set_color('white')
            cell.get_text().set_weight('bold')

        for row_idx, (_, row) in enumerate(grupo.iterrows()):
            ticket = row['venta'] / row['facturas'] if row['facturas'] != 0 else 0

            values = [row['dato'], f"${row['venta']:,.2f}", row['impactos'], row['facturas'], f"${ticket:,.2f}"]

            for col_idx, value in enumerate(values):
                table.add_cell(row_idx, col_idx, width=col_widths[col_idx], height=0.3, 
                               text=value, loc='center', facecolor='white')

        ax.add_table(table)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0) 
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64,buf