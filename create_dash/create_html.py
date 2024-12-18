import math
class generate_html:
    def __init__(self,marca,mes,sede):
        self.marca=marca
        self.mes=mes
        self.sede=sede
    
    
    
    def pagina_1(self,Gsemana,impavsfac,general,facturas,venta):
      def formatear_venta(venta):
        if venta >= 1_000_000: 
            return "{:.1f} M".format(venta / 1_000_000)
        elif venta >= 1_000:
            return "{:,}".format(math.ceil(venta)).replace(",", ".")
        else:
            return "{:,}".format(math.ceil(venta)).replace(",", ".")
      # cajas info
      impactos=general['impactos'].iloc[0]    
      recompra=general['dato'].iloc[0]
      devolucion=general['facturas'].iloc[0]
      tiket=general['venta'].iloc[0]
      # Modelado de datos:
      venta=formatear_venta(venta)
      tiket=formatear_venta(tiket)
      devolucion=round(devolucion,1)
      recompra=round(float(recompra),1)
      facturas=int(facturas)
      css="""
      <style>
     :root {
       --color-primary-blue: #2c3e50;
       --color-accent-blue: #3498db;
       --color-background: #f8f9fa;
       --color-text-dark: #2c3e50;
       --color-text-light: #ffffff;
       --color-highlight: #e74c3c;
       --color-border: #24a853;
       --color-coropo2: #9dd33e;
       --color-corpo1: #16c263;
     }
  
     * {
       margin: 0;
       padding: 0;
       box-sizing: border-box;
     }
  
     body {
       font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
         Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
         sans-serif;
       background-color: var(--color-background);
       color: var(--color-text-dark);
       line-height: 1.6;
     }
  
     .dashboard {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      padding: 0;
      margin: 0;
      flex-direction: column;
    }
  
     .header-container {
       display: flex;
       align-items: center;
       background: linear-gradient(
         135deg,
         var(--color-corpo1) 0%,
         var(--color-coropo2) 100%
       );
       padding: 1rem; /* Adjusted from 1.5rem to reduce height */
       margin-bottom: 1rem;
       box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
       position: relative;
       overflow: hidden;
       height: 15%;
     }
  
     .header-container::before {
       content: "";
       position: absolute;
       top: -50%;
       right: -50%;
       width: 200%;
       height: 200%;
       background: rgba(255, 255, 255, 0.1);
       transform: rotate(-45deg);
     }
  
     .logo {
       width: 120px;
       height: 120px;
       object-fit: contain;
       margin-right: 2rem;
     }
  
     .header {
       flex-grow: 1;
       display: flex;
       flex-direction: column;
     }
  
     .header h1 {
       font-weight: 300;
       font-size: 2.5rem;
       color: var(--color-text-light);
       margin-bottom: 0.5rem;
       position: relative;
       display: inline-block;
     }
  
     .header .subtitle {
       color: rgba(255, 255, 255, 0.8);
       font-size: 1rem;
       font-weight: 300;
     }
  
     .header h1::after {
       content: "";
       position: absolute;
       bottom: -10px;
       left: 0;
       width: 70%;
       height: 4px;
       background-color: var(--color-highlight);
       border-radius: 2px;
     }
  
     .dashboard-grid {
       display: grid;
       grid-template-columns: repeat(5, 1fr);
       grid-template-rows: repeat(3, auto);
       gap: 1.5rem;
       height: auto;
     }
  
     .metrics {
       grid-column: 1 / 6;
       display: grid;
       grid-template-columns: repeat(6, 1fr);
       gap: 1rem;
       height: 50px;
       margin-bottom: 3.4%;
       margin-left: 5px;
       margin-right: 5px;
     }
  
     .metric-card {
       background-color: var(--color-text-light);
       border-radius: 8px;
       text-align: center;
       box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
       border: 1px solid var(--color-border);
       display: flex;
       flex-direction: column;
       align-items: center;
       justify-content: center;
     }
  
      .metric-card .icon {
       font-size: 2.1rem;
       margin-top: 0.3rem;
       color: var(--color-highlight);
       opacity: 0.8;
     }
  
     .metric-card h2 {
       color: var(--color-primary-blue);
       font-size: 1.5rem;
       /* margin-bottom: 0.5rem; */
     }
  
     .metric-card p {
       color: var(--color-text-dark);
       font-size: 1rem;
       opacity: 0.7;
     }
  
     .secondary-charts {
       grid-column: 3 / 6; 
       grid-row: 2 / 3;
       background-color: var(--color-text-light);
       border-radius: 8px;
       box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
       border: 1px solid var(--color-border);
       height: 290px;
     }
  
     .main-chart {
         grid-column: 1 / 3; 
         grid-row: 2 / 3;
         background-color: var(--color-text-light);
         border-radius: 8px;
         box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
         border: 1px solid var(--color-border);
         display: flex;
         flex-direction: column;
         align-items: center;
         justify-content: center;
         height: 290px;
     }
  
     .main-chart h3, 
     .secondary-charts h3 {
       color: var(--color-primary-blue);
       margin-bottom: 1rem;
       font-size: 1.5rem;
     }
  
     .last-row {
       grid-column: 1 / 6;
       grid-row: 3 / 4;
       display: grid;
       grid-template-columns: 58% 40%;
       gap: 1.5rem;
       height:300px;
     }
     .last-row-left{
         height: 335px;
     }
     /* .div-conclucion{
         margin-left: 12%;
         width:350px;
         height: 258;
         margin-top: 3%;
     } */
  
     .last-row > div {
       background-color: var(--color-text-light);
       border-radius: 8px;
       box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
       border: 1px solid var(--color-border);
     }
  
     .princi {
       width: 100%;
       height: 100%;
       object-fit: fill;
     }
   </style>
        """
      html=f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Dashboars Servimax</title>
    <link rel="stylesheet" href="/resource/html/all.min.css"/>
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
      rel="stylesheet"/>
</head>
    {css}
        <body>
        <!-- imagen oculta para dar tiempo de renderizado -->
          <img src="https://cdn-icons-png.freepik.com/256/10042/10042887.png?semt=ais_hybrid" alt="" style="width: 1px; height: 1px; visibility: hidden;" >
          <img src="https://media.istockphoto.com/id/1151557689/vector/vector-image-of-a-flat-isolated-icon-dollar-sign-currency-exchange-dollar-united-states.jpg?s=1024x1024&w=is&k=20&c=wtyPBkx4KX1U_CcsRuFH23hbLogVVWYioJzDXbk30Y8=23Trr" alt="" style="width: 1px; height: 1px; visibility: hidden;" >
        <div class="dashboard">
          <div class="header-container">
            <img
              src="https://storage.googleapis.com/attachments-servimax-isa/servimaxHomePage/logo2.0.png"
              alt="Servimax Logo"
              class="logo"
            />

            <div class="header">
              <h1>{self.marca}</h1>
              <div class="subtitle">
                Análisis Integral de Rendimiento Corporativo
              </div>
            </div>
          </div>

          <div class="dashboard-grid">
            <div class="metrics">
              <div class="metric-card">
                <i class="icon fas fa-users"></i>
                <h2>{impactos}</h2>
                <p>impactos</p>
              </div>
              <div class="metric-card">
                <i class="icon fas fa-project-diagram"></i>
                <h2>{facturas}</h2>
                <p>Facturas</p>
              </div>
              <div class="metric-card">
                <i class="icon fas fa-dollar-sign"></i>
                <h2>${venta}</h2>
                <p>Ventas Totales</p>
              </div>
              <div class="metric-card">
                <i class="icon fas fa-project-diagram"></i>
                <h2>${tiket}</h2>
                <p>TIket</p>
              </div>
              <div class="metric-card">
                <i class="icon fas fa-info-circle"></i>
                <h2>{recompra}%</h2>
                <p>Tasa de recompra</p>
              </div>
              <div class="metric-card">
                <i class="icon fas fa-chart-line"></i>
                <h2>{devolucion}%</h2>
                <p>Tasa de Devolución</p>
              </div>
            </div>

            <div class="secondary-charts">
              <img
                src="data:image/png;base64,{Gsemana}"
                alt="Gráfica Principal"
                class="princi"
              />
            </div>

            <div class="main-chart">
              <img
                src="data:image/png;base64,{impavsfac}"
                alt="grafica secundaria"
                class="princi"
              />
            </div>

            <div class="last-row">
              <div class="last-row-left">
                <img
                  src="data:image/png;base64,{impavsfac}"
                  alt="grafica secundaria"
                  class="princi"
                />
              </div>
              <div class="div-conclucion">
                <h3>Analisis y tendencias</h3>
              </div>
            </div>
          </div>
        </div>
      </body>
    </html>
        """
    
    
      with open("resource/html/hoja_1.html", "w") as file:
            file.write(html)    
            
            
            
