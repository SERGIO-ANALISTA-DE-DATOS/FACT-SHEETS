import pymysql

def conectar_bd():
     return pymysql.connect(
        host="servimaxinternal.app", 
        user='sergio_naranjo',
        password='5RT_20#',
        db='DASHBOARDS',
        port=4406  
    )
