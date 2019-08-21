from flask import Flask,request,render_template,url_for,redirect
import pyodbc

app = Flask(__name__)

#conexion base de datos 
server = '204.141.52.148' 
database = 'dbKieroNew' 
username = 'MachineBaseConnect3651' 
password = 'H1#KotS(xh5nF+tGv' 



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/datos", methods=['POST'])
def datos():

    if request.method == 'POST':
        consulta = request.form['Consulta']  
        print(consulta)      
        cnxn = pyodbc.connect('DRIVER={SQL SERVER};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        #la consulta es por PARTNERSHIPID
        
        if len(consulta) <= 8 :
            if consulta == '' :
                consulta = None
            cursor.execute('''SELECT CA.GUID,CA.NAME,CA.SHORT_DESCRIPTION,CA.PROVIDER_GUID, PR.PARTNERSHIPID, PR.UPC_EAN,CA.HEIGTH, CA.LONG, CA.WIDTH , CA. WEIGHT 
            FROM [dbKieroNew].[dbo].[NC_CATALOG_PRODUCTS] AS CA INNER JOIN [dbKieroNew].[dbo].[PRNEPARTNERSHIP] AS PR  ON CA.GUID =PR.PRODUCTGUID 
            WHERE (PR.PARTNERSHIPID = ?)''',(consulta))
            datosobjeto = cursor.fetchall()
            #la consulta es por Product-Code
        if len(consulta) > 8 and len(consulta)<= 12 :
            cursor.execute('''SELECT CA.GUID,CA.NAME,CA.SHORT_DESCRIPTION,CA.PROVIDER_GUID, PR.PARTNERSHIPID, PR.UPC_EAN,CA.HEIGTH, CA.LONG, CA.WIDTH , CA. WEIGHT 
            FROM [dbKieroNew].[dbo].[NC_CATALOG_PRODUCTS] AS CA INNER JOIN [dbKieroNew].[dbo].[PRNEPARTNERSHIP] AS PR  ON CA.GUID =PR.PRODUCTGUID 
            WHERE (CA.PRODUCT_CODE= ?)''',(consulta))
            datosobjeto = cursor.fetchall()
        if len(consulta) > 12 :
            cursor.execute('''SELECT CA.GUID,CA.NAME,CA.SHORT_DESCRIPTION,CA.PROVIDER_GUID, PR.PARTNERSHIPID, PR.UPC_EAN,CA.HEIGTH, CA.LONG, CA.WIDTH , CA. WEIGHT 
            FROM [dbKieroNew].[dbo].[NC_CATALOG_PRODUCTS] AS CA INNER JOIN [dbKieroNew].[dbo].[PRNEPARTNERSHIP] AS PR  ON CA.GUID =PR.PRODUCTGUID 
            WHERE (CA.GUID = ?) OR (PR.PRODUCTGUID = ?)''',(consulta,consulta))
            datosobjeto = cursor.fetchall()
            print(datosobjeto)
            cnxn.close()
        #datosobjeto = cursor.fetchall()
        print(datosobjeto)
        return render_template('index.html', informacion = datosobjeto)

 
@app.errorhandler(500)
def page_not_found(error):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='204.141.52.148' ,port=54700)
