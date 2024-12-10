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
        """
    try:
        with conexion.cursor() as cursor:
            cursor.execute(query)
            encabezados = [desc[0] for desc in cursor.description]
            respueta=cursor.fetchall()
            return respueta,encabezados
    finally:
        conexion.close()
        
        
        
        