#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import re
import sys
import os
import subprocess as sub

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<style>"
print '''body {
           font-family: 'Roboto', sans-serif;
           font-size: 14px;
         }'''
print "</style>"
print "</head>"
print "<body>"

form = cgi.FieldStorage()

listado_items = ['despliegue','servicio','vendor','modelo','plantilla']

camposdict = {}

#print form
#print '<br><br>'

for campo in form:
  if 'bloque' in campo:
    camposdict[campo] = form.getvalue(campo)
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

mydb = mysql.connector.connect(
  host="localhost",
  user="fernando",
  passwd="f3rn4nd0",
  database="gestor_plantillas"
)
mycursor = mydb.cursor()

def unico(val0):
  temporal = []
  for resultado in val0:
    if resultado not in temporal:
      temporal.append(resultado)
  return temporal

def consulta(val1):
  mycursor.execute(val1)
  return mycursor.fetchall()

mensaje_pri = '''<div style="padding:5px;width:730px;border:1px solid #ccc;">
      <b>Importante:</b><br>
      <ul>
      <li>Solo se muestran las plantillas que tengan variables creadas.</li>
      <li>Solo se muestran los despliegues, servicios, vendors y modelos asociados a plantillas.</li>
      </ul></div><br><br>'''

def agrega_bloque(nom_bloque,cont_bloque,plant_id):
  bloques_plant = consulta("select * from bloque where plantilla_id='"+plant_id+"';")
  mycursor.execute("insert into bloque (nombre_bloque,plantilla_id) values ('"+nom_bloque+"','"+plant_id+"');")
  mydb.commit()

  rutas = []
  raiz = '/var/www/gestion_plantillas'

  if os.path.isdir(raiz) == False:
    sub.Popen(['mkdir','/var/www/gestion_plantillas'],stdout=sub.PIPE,stderr=sub.PIPE)
    sub.Popen(['chown','apache:apache','/var/www/gestion_plantillas'],stdout=sub.PIPE,stderr=sub.PIPE)
    sub.Popen(['chmod','660','/var/www/gestion_plantillas'],stdout=sub.PIPE,stderr=sub.PIPE)

  otro_dict = {}

  for elemento in listado_items:
    for items_form in form:
      if elemento in items_form:
        otro_dict[elemento] = items_form

  rutas.append(raiz+'/'+'despliegue_'+str(otro_dict['despliegue'].split('_')[2]))
  rutas.append(rutas[0]+'/'+'servicio_'+str(otro_dict['servicio'].split('_')[2]))
  rutas.append(rutas[1]+'/'+'vendor_'+str(otro_dict['vendor'].split('_')[2]))
  rutas.append(rutas[2]+'/'+'modelo_'+str(otro_dict['modelo'].split('_')[2]))

  arch_plantilla = 'original_'+str(plant_id)+'_'+str(otro_dict['plantilla'].split('_')[3])+'_'+str(otro_dict['despliegue'].split('_')[2])+'_'+str(otro_dict['servicio'].split('_')[2])+'_'+str(otro_dict['vendor'].split('_')[2])+'_'+str(otro_dict['modelo'].split('_')[2])+'_bloque'+str(len(bloques_plant)+1)+'.txt'

  for parte in rutas:
    if os.path.isdir(parte) == False:
      os.mkdir(parte)

  nueva_plantilla = open(rutas[3]+'/'+arch_plantilla,'w',0)
  nueva_plantilla.write(cont_bloque);
  nueva_plantilla.close()  

  req_bloque(plant_id)
  

def req_bloque(plantilla):
  print 'La plantilla seleccionada tiene la siguiente ruta:<br><br>'

  print '<form action = "editar_bloques.py" method = "post">'

  fila_1 = ''
  fila_2 = ''
  
  for l_items in listado_items:
    fila_1 = fila_1 + '<td><span style="font-size:13px"><b>'+l_items.capitalize()+'</b></span></td>'
    fila_2 = fila_2 + '<td><input style="text-align: center;" type="text" name="'+str(camposdict[l_items+'_item_'])+'" value="'+str(camposdict[l_items+'_item_'].split('_')[3])+'" readonly></td>'

  print '<table>'
  print '<tr align = "center" style="font-size:14px">' + fila_1 + '</tr>'
  print '<tr align="center">' + fila_2 + '</tr>'
  print '</table>'
   
  prev_variables = consulta('select * from variable where plantilla_id='+str(plantilla)+';')
  variables = unico(prev_variables) 

  print '<br><br>Ingresa los datos del bloque que vas a agregar a la plantilla:<br><br>'
  print '<table>'
  print '''<tr><td><span style="font-size:13px"><b>Nombre del Bloque</b></span><br><input type="text" name="nombre_bloque_item_'''+str(camposdict[l_items+'''_item_'''].split('_')[2])+'''" pattern="^\w([^\s]\w+){1,}$" size=30 required><br><br>
  <span style="font-size:13px"><b>Contenido del Bloque</b></span><br>
  <textarea id="contenido_bloque" name="contenido_bloque_item_'''+str(camposdict[l_items+'''_item_'''].split('_')[2])+'''" cols = "60" rows = "20" required></textarea>
  </td></tr></table>
  '''

  print '<br><br><br><input type = "submit" value = "Continuar" style="width:100px; height:20px;"/></form>'
  print '''<form action = "pri_menu.php" method = "post">
  <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
  </form>'''


def revision(item_gen):
  inicial_1 = ''
  inicial_2 = ''
  estatico = ''

  itemstabla = item_gen[len(item_gen)-1]+'.id, '+item_gen[len(item_gen)-1]+'.creacion, '+item_gen[len(item_gen)-1]+'.nombre_'+item_gen[len(item_gen)-1]

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

  prevresult_1 = consulta('select '+ itemstabla +' from '+inicial_1+'plantilla, variable where '+inicial_2+'plantilla.id = variable.plantilla_id;') 

  myresult_1 = unico(prevresult_1)

  if len(item_gen)>1:
    for numitem in range(0,len(item_gen)-1):
      for x,y in camposdict.items():
        if item_gen[numitem] in x:
          aparece_item = y.split('_')[3]
          estatico = estatico + '<b>'+item_gen[numitem].capitalize()+'</b> asociado(a) a la <b>configuracion</b> que vas a generar:<br><br>' + '<input style="text-align: center;" type="text" name="'+str(y)+'" value="'+str(aparece_item)+'" readonly><br><br>'

  lista_1 = ''

  if len(myresult_1)>0:
    for val in myresult_1:
      lista_1 = lista_1 + '<option value = "'+item_gen[len(item_gen)-1]+'_item_'+str(val[0])+'_'+str(val[2])+'">'+str(val[2])+'</option>'
    print mensaje_pri
    print '''<form action = "editar_bloques.py" method = "post">'''
    print estatico
    print '<b>'+item_gen[len(item_gen)-1].capitalize()+'</b> asociado(a) a la <b>configuracion</b> que vas a generar:<br><br>'
    print '<select name = "'+item_gen[len(item_gen)-1]+'_item_">'
    print lista_1
    print '</select>'
    print '<br><br><br><input type = "submit" value = "Continuar" style="width:100px; height:20px;"/></form>'
    print '''<form action = "pri_menu.php" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''
  elif len(myresult_1)==0:
    print "La lista de <b>"+item_gen[len(item_gen)-1].capitalize()+"s</b> esta vacia!<br><br>"
    print '''<form action = "pri_menu.php" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''

# Get data from fields

cant_bloques = 0

for temp_item in camposdict:
  if 'bloque' in temp_item:
    plantilla_id = temp_item.split('_')[3]
    cant_bloques = 1
    if 'nombre_bloque' in temp_item:
      nombre_bloque = form.getvalue(temp_item)
    elif 'contenido_bloque' in temp_item:
      contenido_bloque = form.getvalue(temp_item)

if cant_bloques == 1:
  agrega_bloque(nombre_bloque,contenido_bloque,plantilla_id)
elif len(camposdict)<5:
  if len(camposdict) == 0:
    revision([listado_items[0]])
  else:
    revision(listado_items[0:len(camposdict)+1])
elif len(camposdict)>4:
  id_plantilla = camposdict["plantilla_item_"].split('_')[2]
  req_bloque(id_plantilla)

print "</body>"
print "</html>"
