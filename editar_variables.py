#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import re
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import aa_cabecera
import aa_elementos
import aa_tabla

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()
independientes, dependientes = aa_elementos.elementos()

form = cgi.FieldStorage()

if len(form) > 0:
  print "Content-type:text/html\r\n\r\n"
  print "<html>"
  print "<head>"
  print txt_in_head
  print "<style>"
  print txt_in_css
  print '''body {
           margin:0px;
           font-family: 'Roboto', sans-serif;
           font-size: 14px;
         }'''
  print "</style>"
  print "</head>"
  print "<body>"
  print txt_show_menu
  print '<div style="border-top:1px solid #3fa338;height:25px;background-color: #3fa338; color:white"><div style="margin-left:11px;margin-top:4px;font-size:14px;font-family: Calibri, sans-serif">Editar Variables</div></div>'
  print '<br><br><div style="margin:10px;">'

else:
  print "Location: pri_menu.php\r\n\r\n"
  sys.exit()

listado_items = independientes + ['modelo','plantilla']

camposdict = {}

#print form
#print '<br><br>'

var_form = []

for campo in form:
  for campos in listado_items:
    if campos in campo:
      if len(campo.split('_')) == 3:
        camposdict[campo] = form.getvalue(campo)
      else:
        camposdict['_'.join(campo.split('_')[0:2])+'_'] = campo

#print camposdict
#print '<br>'
#print var_form
#print '<br>'

def unico(val0):
  temporal = []
  for resultado in val0:
    if resultado not in temporal:
      temporal.append(resultado)
  return temporal

def consulta(val1):
  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )
  mycursor = mydb.cursor()
  mycursor.execute(val1)
  return mycursor.fetchall()

def revision(item_gen):
  mensaje_pri = '''<div style="padding:5px;width:730px;border:1px solid #ccc;">
  <b>Importante:</b><br>
  <ul>
  <li>Solo se muestran las plantillas que tengan variables creadas.</li>
  <li>Solo se muestran las areas, despliegues, servicios, vendors y modelos asociados a plantillas.</li>
  </ul></div><br><br>'''
  inicial_1 = ''
  inicial_2 = ''
  estatico = ''

  itemstabla = item_gen[len(item_gen)-1]+'.id, '+item_gen[len(item_gen)-1]+'.creacion, '+item_gen[len(item_gen)-1]+'.nombre_'+item_gen[len(item_gen)-1]
    
  if len(item_gen) > 0:
    call_var_1 = ''
    call_var_2 = '1=1;'
  else:
    call_var_1 = ', variable'
    call_var_2 = 'plantilla.id = variable.plantilla_id;'

  for elemento_item in item_gen:
    if elemento_item == 'plantilla':
      inicial_1 = inicial_1
    else:
      inicial_1 = inicial_1 + elemento_item + ', '
      buscado =  elemento_item + "_item_"
    if elemento_item == 'plantilla':
      inicial_2 = inicial_2
    elif buscado in camposdict:
      inicial_2 = inicial_2 + 'plantilla.'+ camposdict[buscado].split('_')[0] +'_id = '+ camposdict[buscado].split('_')[2] +' and '
    else:
      inicial_2 = inicial_2 + elemento_item + '.id = plantilla.'+ elemento_item +'_id and '
 
  #print '<br>select distinct '+ itemstabla +' from '+inicial_1+'plantilla, variable where '+inicial_2+'plantilla.id = variable.plantilla_id;<br><br>'
  #print 'select '+ itemstabla +' from '+inicial_1+'plantilla, variable where '+inicial_2+'plantilla.id = variable.plantilla_id;'
  
  #print 'select '+ itemstabla +' from '+inicial_1+'plantilla'+call_var_1+' where '+inicial_2+call_var_2

  prevresult_1 = consulta('select distinct '+ itemstabla +' from '+inicial_1+'plantilla'+call_var_1+' where '+inicial_2+call_var_2) 

  myresult_1 = unico(prevresult_1)

  cabcr = []
  nombr = []
  contn = []

  ruta_plantilla = ''

  if len(item_gen)>1:
    for numitem in range(0,len(item_gen)):
      for x,y in camposdict.items():
        if item_gen[numitem] in x:
          aparece_item = y.split('_')[3]
          #estatico = estatico + '<b>'+item_gen[numitem].capitalize()+'</b> asociado(a) a la <b>configuracion</b> que vas a generar:<br><br>' + '<input style="text-align: center;" type="text" name="'+str(y)+'" value="'+str(aparece_item)+'" readonly><br><br>'
          cabcr.append(item_gen[numitem].capitalize())
          nombr.append(str(y))
          contn.append(str(aparece_item))
    ruta_plantilla = aa_tabla.tabla_2_filas(cabcr,contn,nombr) + '<br><br>'
  
  lista_1 = ''

  if len(camposdict) == len(listado_items):
    print mensaje_pri
    #print aa_tabla.tabla_2_filas(cabcr,contn,nombr)
    print '''<form action = "'''+script+'''.py" method = "post">'''
    print ruta_plantilla
    #print estatico
    print '<br><input type = "submit" value = "Continuar" style="width:100px; height:20px;"/>'
  elif len(myresult_1)>0:
    for val in myresult_1:
      lista_1 = lista_1 + '<option value = "'+item_gen[len(item_gen)-1]+'_item_'+str(val[0])+'_'+str(val[2])+'">'+str(val[2])+'</option>'
    print mensaje_pri
    #print aa_tabla.tabla_2_filas(cabcr,contn,nombr)
    print '''<form action = "'''+script+'''.py" method = "post">'''
    print ruta_plantilla
    #print estatico
    print '<b>'+item_gen[len(item_gen)-1].capitalize()+'</b> asociado(a) a la <b>configuracion</b> que vas a generar:<br><br>'
    print '<select name = "'+item_gen[len(item_gen)-1]+'_item_">'
    print lista_1
    print '</select>'
    print '<br><br><br><input type = "submit" value = "Continuar" style="width:100px; height:20px;"/>'
  elif len(myresult_1)==0:
    print "No se encontraron plantillas asociadas a algun <b>"+item_gen[len(item_gen)-1].capitalize()+"</b>!<br><br><br>"

  print '</form>'
  print '''&nbsp;&nbsp;&nbsp;<form action = "pri_menu.php" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''

# Get data from fields

if len(camposdict)<len(listado_items)-1:
  script = 'editar_variables'
  if len(camposdict) == 0:
    revision([listado_items[0]])
  else:
    revision(listado_items[0:len(camposdict)+1])
elif len(camposdict)>len(listado_items)-2:
  script = 'agrega_variable'
  revision(listado_items[0:len(camposdict)+1])
  
print '</div>'
print "</body>"
print "</html>"
