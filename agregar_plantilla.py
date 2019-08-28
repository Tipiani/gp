#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import aa_cabecera
import aa_elementos
import aa_tabla

independientes, dependientes = aa_elementos.elementos()
independientes_2 = independientes + ['modelo']
#independientes = ['area','despliegue','servicio','vendor']
#dependientes = ['modelo','plantilla','variable']

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

form = cgi.FieldStorage()

if len(form) > 0:
  print "Content-type:text/html\r\n\r\n"
else:
  print "Location: pri_menu.py\r\n\r\n"
  sys.exit()

print "<html>"
print "<head>"
print txt_in_head
print "<style>"
print txt_in_css
print '''body {
           margin: 0px;
           font-family: 'Roboto', sans-serif;
           font-size: 14px;
         }'''
print "</style>"
print "</head>"
print "<body>"
print txt_show_menu

print '<br><br><div style="margin:10px;">'

temp = []

#print form

for elemento in form: 
  temp.append(elemento)

#print temp
#print '<br><br>'

def consulta(val0,val1,val2,val3):
  mycursor = mydb.cursor()
  #print "select "+str(val0)+" from "+val1+" where "+str(val2)+"='"+str(val3)+"';"
  mycursor.execute("select "+str(val0)+" from "+val1+" where "+str(val2)+"='"+str(val3)+"';")
  return mycursor.fetchall()

# Get data from fields

num_item = {}
nom_item = {}

cabeceras = ['Area','Despliegue','Servicio','Vendor','Modelo de Equipo']
conten = []
nombrs = []
cabcr = []

if len(temp)>0:
  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )
  for xjxj in range(0,len(temp)):
    cabcr.append(cabeceras[xjxj])
    elem = independientes_2[xjxj]
    if len(str(form.getvalue(elem)).split('_'))==4:
      num_item['item_'+str(elem)] = form.getvalue(elem).split('_')[2]
      nom_item['nom_'+str(elem)] = form.getvalue(elem).split('_')[3]
      conten.append(form.getvalue(elem).split('_')[3])
    else:
      num_item['item_'+str(elem)] = consulta('id',elem,str('nombre_')+elem,form.getvalue(elem))[0][0]
      nom_item['nom_'+str(elem)] = form.getvalue(elem)
      conten.append(form.getvalue(elem))
    nombrs.append(elem)

if len(temp)==5:
    ruta_plant = ''
    for elem in independientes:
      ruta_plant = ruta_plant + '_' + str(num_item['item_'+str(elem)])
    num_val = []
    selec = ''
    for datoxx in range(0,len(cabeceras)):
      num_val.append(consulta('id',nombrs[datoxx],'nombre_'+str(nombrs[datoxx]),conten[datoxx])[0][0])
      selec = selec + ' and ' + nombrs[datoxx] + "_id = "+str(num_val[datoxx])
    selec = selec + ";"
    
    mycursor = mydb.cursor() 
    mycursor.execute("select nombre_plantilla from plantilla where 1=1" + selec)
    plant_lista = mycursor.fetchall()
    plant_flista = ''

    print '''<form action = "agregar_plantilla_2.py" method = "post">'''
    print aa_tabla.tabla_2_filas(cabcr,conten,nombrs)
    print '<br><br>'
    print 'Se encontraron las siguientes <b>plantillas</b> en esta ruta:<br><br>'
    print '<div style="background-color:#e8e8e8;width:304px;border:1px solid #a9a9a9;border-radius:3px">'
    print '<div style="width:100%;margin-left:5px"><br>'
    for xitem in plant_lista:
      plant_flista = plant_flista + str(xitem[0]) + '<br>'
    print plant_flista
    print '<br></div>'
    print '</div><br>'
    print '''Escribe el nombre de la <b>Plantilla</b> que vas a agregar:<br><br>'''
    print '''<input type="text" name = "plantilla'''+ruta_plant+'''"/><br>
      <span style="color:#8c8c8c;font-size:11px">
      *Los subguiones o espacios en blanco seran reemplazados por guiones (-)<br>
      *Los caracteres no-alfanumericos seran omitidos</span>'''
    print'''<br><br><br>Ingresa aqui el contenido de la <b>Plantilla</b> que vas a agregar:<br><br>
    <textarea id="contenido_plantilla" name = "contenido" cols = "60" rows = "20"></textarea>'''
    print '''<br><br><br><input type = "submit" value = "Continuar"/>
    </form>'''

    print '''<script>
    document.getElementById('contenido_plantilla').onchange = function() {
    var textarea = document.getElementById('contenido_plantilla');
    var re = new RegExp( "<|>", "gm" );
    if (re.test(textarea.value)) {
      alert('found');
    }
    }
    </script>'''

elif len(temp)==4:
  #Buscar modelos asociados al vendor
  lista = ''
  myresult = consulta('*','modelo','vendor_id',num_item['item_vendor'])
  if len(myresult)>0:
    for val in myresult:
      lista = lista + '<option value = "modelo_item_'+str(val[0])+'_'+str(val[3])+'">'+str(val[3])+'</option>'
    print '''<form action = "agregar_plantilla.py" method = "post">'''
    print aa_tabla.tabla_2_filas(cabcr,conten,nombrs)
    print '<br><br>Elige el <b>Modelo de Equipo</b> asociado a la plantilla que vas a agregar:<br><br>'
    print '''<select name = "modelo">'''
    print lista
    print '</select>'
    print '''<br><br><br><input type = "submit" value = "Continuar"/>
    </form>'''
  else:
    print "<br><br>No se tienen modelos asociados al vendor <b>"+nom_item['nom_vendor']+"</b>!"
    print '''<form action = "pri_menu.py" method = "post">
          <input type = "submit" value = "Inicio"/>
          </form>'''

print '</div>'
print "</body>"
print "</html>"
