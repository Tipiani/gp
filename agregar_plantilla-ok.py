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
#independientes = ['area','despliegue','servicio','vendor']
#dependientes = ['modelo','plantilla','variable']

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

form = cgi.FieldStorage()

print "Content-type:text/html\r\n\r\n"
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

def consulta(val1,val2):
  mycursor = mydb.cursor()
  mycursor.execute("select * from "+val1+" where vendor_id="+str(val2)+";")
  return mycursor.fetchall()

# Get data from fields

item_tabla = {}
num_tabla = {}

cabcr = ['Area','Despliegue','Servicio','Vendor']
conten = []
nombrs = []

if len(temp)>0:
  mensaje = ''
  for elem in independientes:
    item_tabla['item_'+str(elem)] = form.getvalue(elem).split('_')[2]
    num_tabla['num_'+str(elem)] = form.getvalue(elem).split('_')[3]
    conten.append(form.getvalue(elem).split('_')[3])
    nombrs.append('deshabilitado')

  print aa_tabla.tabla_2_filas(cabcr,conten,nombrs)
  print '<br><br>'
    #mensaje = mensaje + '<form action=""><b>'+str(elem).capitalize()+'</b> asociado a la plantilla que vas a agregar:<br><br><input type="text" name="deshabilitado" value="'+num_tabla['num_'+str(elem)]+'" disabled></form>'

  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )
#Buscar modelos asociados al vendor
  lista = ''
  myresult = consulta('modelo',item_tabla['item_vendor'])
  if len(myresult)>0:
    print mensaje
    for val in myresult:
      lista = lista + '<option value = "modelo_item_'+str(val[0])+'_'+str(val[3])+'">'+str(val[3])+'</option>'
    print 'Elige el <b>Modelo de Equipo</b> asociado a la plantilla que vas a agregar:<br><br>'
    print '''<form action = "agregar_plantilla_2.py" method = "post">
    <select name = "modelo">'''
    print lista
    print '</select>'

    ruta_plant = ''
    for elem in independientes:
      ruta_plant = ruta_plant + '_' + str(item_tabla['item_'+str(elem)])

    print'''<br><br>Escribe el nombre de la <b>Plantilla</b> que vas a agregar:<br><br>
    <input type="text" name = "plantilla'''+ruta_plant+'''"/><br>
      <span style="color:#8c8c8c;font-size:11px">
      *Los subguiones o espacios en blanco seran reemplazados por guiones (-)<br>
      *Los caracteres no-alfanumericos seran omitidos</span>'''
    print'''<br><br>Ingresa aqui el contenido de la <b>Plantilla</b> que vas a agregar:<br><br>
    <textarea id="contenido_plantilla" name = "contenido" cols = "60" rows = "20"></textarea>'''
    print '''<br><br><br><input type = "submit" value = "Continuar"/>
    </form>'''
    print '''<script>
    var textarea = document.getElementById('contenido_plantilla');
    var re = new RegExp( "<|>", "gm" );
    if (re.test(textarea.value)) {
      alert('found');
    }
    </script>'''
  else:
    print "<br><br>No se tienen modelos asociados al vendor <b>"+num_tabla['num_vendor']+"</b>!"
    print '''<form action = "pri_menu.php" method = "post">
          <input type = "submit" value = "Inicio"/>
          </form>'''

print '</div>'
print "</body>"
print "</html>"
