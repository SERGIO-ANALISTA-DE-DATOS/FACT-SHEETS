from conectar.Connection import conectar_bd
def consult_data(marca,month,sede):
    mes_str = ','.join(map(str, month))
    conexion= conectar_bd()
    query=F"""
        SELECT 
	    'mensual'as tipo,MONTH (STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d'))dato 
        ,sum(total_pedido-total_dev) as venta
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as impactos
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then numero_pedido end ) as facturas
        FROM RESUMEN_VENTAS rv 
        where mes in ({mes_str}) and sede  = '{sede}' and marca='{marca}'
        group by MONTH (STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d')),marca
        union all 
        SELECT 'Semanal'as tipo ,WEEK(STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d'), 1)  AS fecha
        ,sum(total_pedido-total_dev) as venta
             ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as impactos
            ,COUNT(DISTINCT case when total_pedido-total_dev>0 then numero_pedido end ) as facturas
        from RESUMEN_VENTAS rv 
        where mes in ({mes_str}) and sede  = '{sede}' and marca='{marca}'
        GROUP BY WEEK(STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d'), 1),marca
        union all
        SELECT 'grupo' as tipo ,grupo
        ,sum(total_pedido-total_dev) as venta
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as impactos
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then numero_pedido end ) as facturas
        from RESUMEN_VENTAS rv 
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        GROUP  BY grupo 
        UNION  all 
        SELECT 'Fuente' as tipo ,fuente 
        ,sum(total_pedido-total_dev) as venta
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as impactos
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then numero_pedido end ) as facturas
        from RESUMEN_VENTAS rv 
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        GROUP  BY fuente 
        union all 
        SELECT 'articulo' as tipo ,codigoArticulo AS articulo
        ,sum(total_pedido-total_dev) as venta
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as impactos
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then numero_pedido end ) as facturas
        from RESUMEN_VENTAS rv 
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        GROUP  BY codigoArticulo 
        UNION  all
        SELECT 'categoria' as tipo ,categoria  
        ,sum(total_pedido-total_dev) as venta
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as impactos
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then numero_pedido end ) as facturas
        from RESUMEN_VENTAS rv 
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        GROUP  BY categoria
        union all
        SELECT 'day' as tipo 
        ,DAYNAME(STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d'))  as dato
        ,sum(total_pedido-total_dev)  as venta
        ,WEEK(STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d'), 1)as impactos
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as facturas
        from RESUMEN_VENTAS rv
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        group by WEEK(STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d'), 1)
        ,DAYNAME(STR_TO_DATE(CONCAT(anio, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')), '%Y-%m-%d'))
        UNION ALL
        SELECT 'general'                	
        ,re.recompra			  	
        ,base.venta/base.pedido	
        ,base.impac 							
        ,base.devolucion               
        from (
        SELECT 10 as id
        ,sum(total_pedido-total_dev) as venta
        ,sum(total_dev)/sum(total_pedido)*100 as devolucion
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as impac
        ,COUNT(DISTINCT case when total_pedido-total_dev>0 then numero_pedido end ) as pedido
        from RESUMEN_VENTAS rv
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        )base
        join(
        SELECT 10 as id 
        ,count(DISTINCT CASE when transacciones>1 then fiel end) /COUNT(DISTINCT fiel)*100   as recompra
        from (
        SELECT empresa as fiel, COUNT( DISTINCT CASE when total_pedido-total_dev>0 then numero_pedido end) as transacciones
        from RESUMEN_VENTAS rv 
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        Group by empresa 
        ) í
        )re on re.id =base.id
        """
    # print(query)
    # input()    
    try:
        with conexion.cursor() as cursor:
            cursor.execute(query)
            encabezados = [desc[0] for desc in cursor.description]
            respueta=cursor.fetchall()
            return respueta,encabezados
    finally:
        conexion.close()
 
def quey_embudo(marca,month,sede):
    mes_str = ','.join(map(str, month))
    conexion= conectar_bd()
    salida_fin=[]
    query=f"""
        SELECT maestra.cantidad , sub.pedido,sub.compra,fiel.fielone,fiel.fieltwo
        from (
        SELECT 1 as id,COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end ) as cantidad
        from RESUMEN_VENTAS rv
        where sede  = '{sede}' and marca in ('{marca}')
        )maestra
        join(
        SELECT 1 as id,COUNT(DISTINCT empresa) as pedido,
        COUNT(DISTINCT case when total_pedido-total_dev>0 then empresa end )as compra
        from RESUMEN_VENTAS rv
        where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        ) sub on sub.id = maestra.id
        join (
        	SELECT 1 as id  
	        ,count(DISTINCT CASE when transacciones>3 then fiel end)fielone
	        ,count(DISTINCT CASE when transacciones>4 then fiel end) as fieltwo
        	from (
        	SELECT empresa as fiel, COUNT( DISTINCT CASE when total_pedido-total_dev>0 then numero_pedido end) as transacciones
        	from RESUMEN_VENTAS rv 
        	where mes in ({mes_str}) and sede  = '{sede}' and marca in ('{marca}')
        	Group by empresa 
        	) fiel
        )fiel on fiel.id=sub.id 
    """        
    try:
        with conexion.cursor() as cursor:
            cursor.execute(query)
            resultadoParcial = cursor.fetchall()
            salida_fin = list(resultadoParcial[0]) 
            return salida_fin    
    finally:
        conexion.close()    
        
        