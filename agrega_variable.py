#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import cgi, cgitb
import os
import re
import random
import aa_cabecera
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import aa_cabecera
import aa_elementos
import aa_tabla

independientes, dependientes = aa_elementos.elementos()
txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

items_gest = independientes + ['modelo']

form = cgi.FieldStorage()

if len(form) > 0:
  print "Content-type:text/html\r\n\r\n"
else: 
  print "Location: pri_menu.php\r\n\r\n"
  sys.exit()
  
print "<html>"
print "<head>"
print txt_in_head
print "<style>"
print txt_in_css
print '''body {
margin: 0px;
font-family: 'Roboto', sans-serif;
font-size: 12px;
}

thead.fixedHeader tr {
	position: relative;
}

thead.fixedHeader th {
	background: black;
	border-left: 1px solid white;
	border-right: 1px solid white;
	border-top: 1px solid white;
	font-weight: normal;
	/*padding: 4px 3px;*/
        padding: 4px 3px 4px 4px;
	text-align: left
}

html>body tbody.scrollContent {
	display: block;
	height: 217px;
	overflow: auto;
	width: 665px
}

html>body thead.fixedHeader {
	display: table;
	overflow: auto;
	width: 660px
}

tbody.scrollContent td, tbody.scrollContent tr.normalRow td {
	background: white;
	border-top: none;
	border-left: 1px solid white;
	border-right: 1px solid #CCC;
	border-bottom: 1px solid #DDD;
	padding: 2px 3px 3px 4px
}

tbody.scrollContent tr.alternateRow td {
	background: #EEE;
	border-top: none;
	border-left: 1px solid white;
	border-right: 1px solid #CCC;
	border-bottom: 1px solid #DDD;
	padding: 2px 3px 3px 4px
}

'''

#print "</style>"
#print "</head>"
#print "<body>"

temp = []
variables_nombre = []
variables_tipo = []
variables_regex = []
variables_items = []
variables_concatenar = []
variables_texto = []
variables_num = []
variables_suma_ipv4 = []
variables_cuanto_ipv4 = []
eliminar_var = []
variables_comentario = []
mens_rep_out = ''

#tipos = ['Formato IP','IP/Mask','Lista','Solo numeros','Personalizado','Texto Libre','Sin Espacios','Concatenar']
tipos = ['Formato IPv4','Lista','Solo numeros','Personalizado','Texto Libre','Sin Espacios','IPv4 y Mask (Standard)','IPv4 y Mask (Huawei)','IPv4 y Mask (Mikrotik)','IPv4 Suma']
tipos = sorted(tipos, key=lambda x: x[0])
#tipos = {'formato_ip':'Formato IP','lista':'Lista','solo_numeros':'Solo numeros','personalizado':'Personalizado','texto_libre':'Texto Libre','sin_espacios':'Sin Espacios'}

tipos_regex = {'ipv4_y_mask__mikrotik_':'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}','ipv4_y_mask__huawei_':'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,2}','ipv4_y_mask__standard_':'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\/| )\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$','formato_ipv4':'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$','solo_numeros':'^\d+$','texto_libre':'.+','sin_espacios':'^\w([^\s]\w+){1,}$'}

r = lambda: random.randint(0,255)
resaltar = '%d,%d,%d,0.6' % (r(),r(),r())

for elemento in form: 
  temp.append(elemento)

#print temp
#print '<br><br</b>'

nombres = {}
nomcom = {}

ped_lista = None

for valval in temp:
  match = False
  for eleme in items_gest:
    if eleme+'_' in valval:
      nombres['nom_'+eleme] = form.getvalue(valval)
      nomcom['nom_com_'+eleme] = valval
      match = True
      break
  if not match:
    if 'pedir_lista' in valval:
      ped_lista = form.getvalue(valval) 
    elif 'del_' in valval:
      eliminar_var.append(valval)
    elif 'plantilla_' in valval:
      if len(form.getvalue(valval).split('_'))>1:
        nombres['nom_plantilla'] = form.getvalue(valval).split('_')[3]
      else:
        nombres['nom_plantilla'] = form.getvalue(valval)
    elif '_variable_nombre' in valval:
      variables_nombre.append(valval)
    elif '_variable_comentario' in valval:
      variables_comentario.append(valval)
    elif '_variable_concatenar' in valval:
      variables_concatenar.append(valval)
    elif '_variable_tipo' in valval:
      variables_tipo.append(valval)
    elif '_variable_regex' in valval:
        variables_regex.append(valval)
    elif '_variable_items' in valval:
      variables_items.append(valval)
    elif '_parte_texto' in valval:
      variables_texto.append(valval)
    elif '_variable_suma_ipv4' in valval:
      variables_suma_ipv4.append(valval)
    elif 'variable_cuanto_ipv4' in valval:
      variables_cuanto_ipv4.append(valval)

mydb = mysql.connector.connect(
  host="localhost",
  user="fernando",
  passwd="f3rn4nd0",
  database="gestor_plantillas"
)

mycursor = mydb.cursor()
mycursor.execute("select id from plantilla where nombre_plantilla='"+nombres['nom_plantilla']+"';")
id_plantilla = mycursor.fetchall()

mycursor = mydb.cursor()

def adaptar(val):
  final = re.sub(r'\s+|\_+|-+','-',val)
  final = re.sub(r';','',final)
  final = re.sub(r'/','slashesves',final)
  final = re.sub(r';','estasonpuntocomasves',final)
  final = re.sub(r',','estasoncomasves',final)
  final = re.sub(r'-','hola1fer2jotache',final)
  final = re.sub(r'\W','',final)
  final = re.sub(r'hola1fer2jotache','-',final)
  final = re.sub(r'slashesves','/',final)
  final = re.sub(r'estasoncomasves',',',final)
  final = re.sub(r'estasonpuntocomasves',',',final)
  return final

def adaptar_2(val_2):
  final_2 = re.sub(r'^ +| +$','',val_2)
  final_2 = final_2.replace('\\','\\\\')
  final_2 = final_2.replace('\/','\\/')
  final_2 = final_2.replace('\"','')
  final_2 = final_2.replace("\'","")
  return final_2

#mensaje = 'No olvides que debes ingresar el nombre de la Variable.'
mensaje = ''
color = 'green'

def validar_rep(item1,item2):
  mycursor = mydb.cursor()
  mycursor.execute('select nombre_variable,relacion_palabra from variable where relacion_palabra like "%'+re.sub(' ',':nbsp;',parte_asoc)+'%";')
  res1 = mycursor.fetchall()
  mycursor.execute('select nombre_variable from variable where nombre_variable="'+nombre_var+'";')
  res2 = mycursor.fetchall() 
  return sirepetido

ids = {}
parte = ''
parte_sub = ''

for eleme in items_gest:
  ids['id_'+eleme] = nomcom['nom_com_'+eleme].split('_')[2]
  parte = parte + '_' + str(ids['id_'+eleme])
  parte_sub = parte_sub + '/' + eleme + '_' + ids['id_'+eleme]

mycursor = mydb.cursor()
mycursor.execute("select id from plantilla where nombre_plantilla = '"+str(nombres['nom_plantilla'])+"';")

# original_22_plantilla-21_7_3_8.txt
# Abrir contenido de la plantilla

nombre_plantilla_f = 'original_'+str(mycursor.fetchall()[0][0])+'_'+str(nombres['nom_plantilla'])+parte+'.txt'

rutatxt = '/var/www/gestion_plantillas'+parte_sub+'/'+nombre_plantilla_f

texto_bruto = open(rutatxt,'r',1)
text_content = texto_bruto.read()

text_content = re.sub(r'\n+','\n',text_content)
text_content = re.sub(r'\n\s+\n','\n',text_content)
text_content = re.sub(r'\s+\n','\n',text_content)

show_text = re.sub(r'\n','<br>',text_content)
show_text = re.sub(r' ','&nbsp;',show_text)

####################################################

def insert_variable(val_plant_id, var_nombre, var_tipo, var_contenido, var_texto, color_resalta, var_coment):
  mycursor.execute("select * from variable where plantilla_id="+str(val_plant_id)+" and nombre_variable='"+str(var_nombre)+"';")
  coinci = mycursor.fetchall()
  mycursor.execute("select * from variable where plantilla_id="+str(val_plant_id)+" and relacion_palabra like '%"+str(re.sub(' ','&nbsp;',var_texto))+"%';")
  coinci_2 = mycursor.fetchall()
  mycursor.execute("select * from variable where instr('"+str(var_texto)+"',relacion_palabra) > 0 and plantilla_id="+str(val_plant_id)+";")
  coinci_3 = mycursor.fetchall()
  if not var_texto in text_content:
    mens_rep = "ERROR AL CREAR VARIABLE.\\nEl texto usado como referencia para la variable no ha sido encontrado en el contenido de la plantilla."
  elif len(coinci)>0:
    mens_rep = "ERROR AL CREAR VARIABLE.\\nLa plantilla ya tiene una variable llamada '"+str(var_nombre)+"'"
  elif len(coinci_2)>0:
    mens_rep = "ERROR AL CREAR VARIABLE.\\nEl texto seleccionado '"+str(var_texto)+"' ya se encuentra asociado a la variable '"+coinci_2[0][3]+"'."
  elif len(coinci_3)>0:
    mens_rep = "ERROR AL CREAR VARIABLE.\\nEl texto seleccionado '"+str(var_texto)+"' contiene el texto asociado a la variable '"+coinci_3[0][3]+"'."
  else:  
    mycursor.execute("insert into variable (plantilla_id,nombre_variable,tipo,contenido,relacion_palabra,color,comentario) values ('"+str(val_plant_id)+"','"+str(var_nombre)+"','"+var_tipo+"','"+str(var_contenido)+"','"+str(var_texto).replace(' ','&nbsp;')+"','"+str(color_resalta)+"','"+str(var_coment)+"');")
    mydb.commit()
    mens_rep = ''
  return mens_rep

if len(eliminar_var) > 0:
  for del_var in eliminar_var:
    mycursor.execute('select nombre_variable from variable where id='+str(form.getvalue(del_var).split('_')[1])+';')
    variab_del = mycursor.fetchall()[0][0]
    mycursor.execute('delete from variable where id='+str(form.getvalue(del_var).split('_')[1])+';')
    mydb.commit()
    mycursor.execute("delete from variable where plantilla_id="+str(id_plantilla[0][0])+" and contenido like '"+str(variab_del)+"&nbsp;\+&nbsp;%';")
    mydb.commit()
    
if len(variables_nombre)>0 and len(variables_texto)>0:
  parte_asoc = re.sub(r'^ +| +$','',str(form.getvalue(variables_texto[0])))
  color = 'red'
  nombre_var = adaptar(form.getvalue(variables_nombre[0])).upper()
  plant_id = id_plantilla[0][0]
  if len(variables_comentario)>0:
    txt_comentario = form.getvalue(variables_comentario[0])
  else:
    txt_comentario = ''
  match = False
  for eleme in tipos_regex.keys():
    if form.getvalue(variables_tipo[0]) == eleme:
      tipo_var = eleme
      regularexp = adaptar_2(tipos_regex[eleme])    
      mens_rep_out = insert_variable(plant_id, nombre_var, tipo_var, regularexp, parte_asoc, resaltar, txt_comentario)
      match = True
  if not match:
    if form.getvalue(variables_tipo[0]) == 'lista':
      if len(variables_items)>0:
        tipo_var = 'lista'
        listado = adaptar_2(form.getvalue(variables_items[0]))
        mens_rep_out = insert_variable(plant_id, nombre_var, tipo_var, listado, parte_asoc, resaltar, txt_comentario)
      else:
        mensaje = "No has ingresado items para la variable del tipo 'Lista'."
    elif form.getvalue(variables_tipo[0]) == 'personalizado':
      if len(variables_regex)>0:
        tipo_var = 'personalizado'
        regexxx = adaptar_2(form.getvalue(variables_regex[0]))
        mens_rep_out = insert_variable(plant_id, nombre_var, tipo_var, regexxx, parte_asoc, resaltar, txt_comentario)
      else:
        mensaje = 'No has ingresado una expresion regular.'
    elif form.getvalue(variables_tipo[0]) == 'ipv4_suma':
      if len(variables_suma_ipv4)>0 and len(variables_cuanto_ipv4)>0:
        tipo_var = 'ipv4_suma'
        suma_var = str(form.getvalue(variables_suma_ipv4[0])) + '&nbsp;+&nbsp;' + str(form.getvalue(variables_cuanto_ipv4[0]))
        mens_rep_out = insert_variable(plant_id, nombre_var, tipo_var, suma_var, parte_asoc, resaltar, txt_comentario)
      else:
        mensaje = 'No has ingresado items para concatenar.'
    else:
      mensaje = 'No existe registro del tipo de variable seleccionado.'
else:
  color = 'red'
  mensaje = 'No olvides que debes ingresar el nombre de la variable y el texto al cual será asociado.'

mycursor = mydb.cursor()
mycursor.execute("select id,nombre_variable,tipo,contenido,relacion_palabra,color from variable where plantilla_id='"+str(id_plantilla[0][0])+"'order by nombre_variable asc;")
match_plantilla_var = mycursor.fetchall()

mycursor.execute("select nombre_variable from variable where plantilla_id='"+str(id_plantilla[0][0])+"'order by creacion desc limit 1;")
ultimo_var = mycursor.fetchall()

print "</style>"

if len(mens_rep_out)>1 or len(mensaje)>1:
  print '<script>'
  print '''function myFunction() {
  alert("'''+mens_rep_out+'''\\n'''+mensaje+'''");
  }'''
  print '</script>'
  print '</head>'
  print '<body onload="myFunction()">'
else:
  print "</head>"
  print "<body>"

print txt_show_menu
print '<div style="border-top:1px solid #3fa338;height:25px;background-color: #3fa338; color:white"><div style="margin-left:11px;margin-top:4px;font-size:14px;font-family: Calibri, sans-serif">Editar Variables</div></div><br><br>'

print '''<span style="margin-left:5px">Vas a agregar <b>variables</b> para la plantilla <b>"'''+nombres['nom_plantilla']+'''"</b>:</span>
<br><br><br>
<span style="margin-left:5px">Has asociado la plantilla de la siguiente manera:<br><br><br></span>'''

print '<form style="margin-left:5px" action = "agrega_variable.py" method = "post">'

cabecers = ['Area','Despliegue','Servicio','Vendor','Modelo de Equipo','Nombre de Plantilla']

contents = []
tbnomb = []

for eleme in items_gest:
  contents.append(nombres['nom_'+eleme])
  tbnomb.append(nomcom['nom_com_'+eleme])

contents = contents + [nombres['nom_plantilla']]
tbnomb = tbnomb + ['plantilla_'+nombres['nom_plantilla']]

print aa_tabla.tabla_2_filas(cabecers,contents,tbnomb)

for asoc in match_plantilla_var:
  texto_asoc_parte = asoc[4] 
  color_resalta = asoc[5]
  show_text = show_text.replace(str(texto_asoc_parte),'<span title="var: '+str(asoc[1])+'" style="text-shadow:0.5px 0.5px 2px #FFF;background-color:rgba('+str(color_resalta)+')">'+str(texto_asoc_parte)+'</span>')

print '<br><br><hr>'

print '<table>'
print '<th>'
#######
print '<td style="font-size:12px;vertical-align: top;width: 55%;">'

salto_text = show_text.split("<br>")

informativo = '#747474'

ixxj = 0
num_text = ""

ubicaciones = {}

for partecita in salto_text:
  ixxj = ixxj + 1
  num_text = num_text + '<br><span id="linea_'+str(ixxj)+'" style="color:'+informativo+'">' + str(ixxj) + '.</span> ' + partecita
  for registro in match_plantilla_var:
    if registro[4] in partecita:
      if registro[4] in ubicaciones:
        ubicaciones[registro[4]] = str(ubicaciones[registro[4]])+', <a href="agrega_variable.py#linea_'+str(ixxj)+'">'+str(ixxj)+'</a>'
      else:
        ubicaciones[registro[4]] = '<a href="agrega_variable.py#linea_'+str(ixxj)+'">'+str(ixxj)+'</a>'

ixj = 0

if len(match_plantilla_var)>0:
  medidas1 = ['50px','100px','90px','190px','150px','30px','50px']
  medidas = ['50px','100px','90px','190px','150px','30px','50px']
  #medidas = ['10px','82px','61px','181px','98px','62px']
  
  print '<br>Variables asociadas a la plantilla <b>"'+nombres['nom_plantilla']+'":</b><br><br>'
  print '<table border="0" cellpadding="0" cellspacing="0" width="100%" class="scrollTable">'
  print '''<thead class="fixedHeader">
  <tr align = "center" style="font-size:12px;background-color: black; color: white;">
  <th style="width:'''+str(medidas1[0])+'''"><b>Elim.</b></th>
  <th style="width:'''+str(medidas1[1])+'''"><b>Variable</b></th>
  <th style="width:'''+str(medidas1[2])+'''"><b>Tipo</b></th>
  <th style="width:'''+str(medidas1[3])+'''"><b>Contenido</b></th>
  <th style="width:'''+str(medidas1[4])+'''"><b>Asociado a</b></th>
  <th style="width:'''+str(medidas1[5])+'''"><b>Color</b></th>
  <th style="width:'''+str(medidas1[5])+'''"><b>Lineas</b></th>
  </tr></thead>'''

  tablita = '<tbody class="scrollContent">'
  for registro in match_plantilla_var:
     tablita = tablita + '<tr align = "center" style="font-size:12px;background-color: #e1e7f2">'
     for celda in registro:
       ixj = ixj + 1
       if ixj == 1:
         tablita = tablita + '<td style="width:'+str(medidas[ixj-1])+'"><input type="checkbox" name="del_'+str(celda)+'" value="del_'+str(celda)+'"></td>'
       elif ixj == 2:
         if celda == ultimo_var[0][0]:
           tablita = tablita + '<td style="width:'+str(medidas[ixj-1])+'"><b>' + str(celda) + '</b></td>'
         else:
           tablita = tablita + '<td style="width:'+str(medidas[ixj-1])+'">' + str(celda) + '</td>'
       elif ixj == len(registro):
         tablita = tablita + '<td style="width:'+str(medidas[ixj-1])+'; background-color:rgba(' + str(celda) + ')"></td>'
       elif ixj == 4:
         tablita = tablita + '<td style="width:'+str(medidas[ixj-1])+';word-break: break-all;">' + str(celda) + '</td>'
       else:
         tablita = tablita + '<td style="width:'+str(medidas[ixj-1])+';word-break: break-all;">' + str(celda) + '</td>'
     tablita = tablita + '<td style="width:'+str(medidas[ixj-1])+'">' + str(ubicaciones[registro[4]]) + '</td>'
     tablita = tablita + '</tr>'
     ixj = 0
  print tablita
  print '</tbody></table>'
else:
  print '<br><br>No hay variables asociadas a la plantilla <b>"'+nombres['nom_plantilla']+'"</b>.'

print '</td>'

print '<td style="font-size:12px;vertical-align: top; width: 45%;">'

##############################################

#salto_text = show_text.split("<br>")

#informativo = '#747474'

#ixxj = 0
#num_text = ""

#for partecita in salto_text:
#  ixxj = ixxj + 1
#  num_text = num_text + '<br><span style="color:'+informativo+'">' + str(ixxj) + '.</span> ' + partecita

print '<br><b>Contenido de la plantilla:</b><br><br>'
print '''<div style="background: white;font-size:11px;font-family:Lucida Console;height:240px;width:800px;border:1px solid #ccc;overflow:scroll;">'''
print num_text
print "</div>"

###
#
print '<table>'
print '<tr>'
print '<td>'

table_text = show_text.split('<br>')

print '</td>'
print '</tr>'
print '</table>'

print '</td>'

print '</th>'
print '<table>'

print '<br><hr>'

if ped_lista is None:
  mycursor.execute("select var_lista from plantilla where id = " + str(id_plantilla[0][0]) + ";")
  ped_lista = mycursor.fetchall()[0][0]
elif ped_lista == 'si':
  mycursor.execute("update plantilla set var_lista = 'si' where id = " + str(id_plantilla[0][0]) + ";")
  mydb.commit()
else:
  mycursor.execute("update plantilla set var_lista = 'no' where id = " + str(id_plantilla[0][0]) + ";")
  mydb.commit()

mycursor.execute("select var_lista from plantilla where id = " + str(id_plantilla[0][0]) + ";")
var_como_list = mycursor.fetchall()

if var_como_list[0][0] == 'si':
  sol_msg = 'Si<input type="radio" name="pedir_lista" value="si" checked="checked">&nbsp;&nbsp;No<input type="radio" name="pedir_lista" value="no">'
else:
  sol_msg = 'Si<input type="radio" name="pedir_lista" value="si">&nbsp;&nbsp;No<input type="radio" name="pedir_lista" value="no" checked="checked">'
 
print '<table style="font-size:12px;">'
print '<tr><td>'
print '<br>Agregar <b>variables:</b><br>'
print '</td></tr>'
print '<tr><td colspan=3 style="vertical-align:middle;">'
print '<br><b>Solicitar lista de variables</b> (para plantillas que usan datos de tablas excel):&nbsp;&nbsp;&nbsp;' + sol_msg
print '</td></tr>'
print '<tr><td>'
print '<span style="color:'+color+'; font-size:12px;"><br></span>'

print '<span style="font-size:12px;"><b>Texto asociado a variable</b></span><br>'
print '<input type="text" name="'+str(id_plantilla[0][0])+'_parte_texto" pattern=".{3,}" title="De 3 caracteres a más." size="25"/><br><br>'
print '</td></tr>'
print '<tr>'
print '<td><b>Nombre de Variable</b></td>'
print '<td><b>Tipo</b></td>'
print '<td><span id="texto_suma_ipv4" style="display:none"><b>Variable Existente</b></span></td>'
print '<td><span id="texto_cuanto_ipv4" style="display:none"><b></b></span></td>'
print '<td><span id="texto_custom" style="display:none"><b>Regex</b></span></td>'
print '<td><span id="texto_lista" style="display:none"><b>Items de la lista</b></span></td>'
print '</tr>'
print '<tr>'
print '<td><input type="text" name="'+str(id_plantilla[0][0])+'_variable_nombre" size="25"/>'
print '''<br><span style="color:white;font-size:11px">
      a</span>'''
print '</td>'

lista = ''
lista_sum = ''

for items in tipos:
  if str(items[0]).upper()+str(items[1:]) == 'Lista':
    if var_como_list[0][0] == 'si':
      lista = lista + '<option style="display:none;" value = "'+re.sub('\W','_',str(items).lower())+'">'+str(items[0]).upper()+str(items[1:])+'</option>'
    else:
      lista = lista + '<option value = "'+re.sub('\W','_',str(items).lower())+'">'+str(items[0]).upper()+str(items[1:])+'</option>'
  else:
    lista = lista + '<option value = "'+re.sub('\W','_',str(items).lower())+'">'+str(items[0]).upper()+str(items[1:])+'</option>'

mycursor.execute("select id,nombre_variable from variable where plantilla_id="+str(id_plantilla[0][0])+" and tipo like '%\_ipv4%';")
var_con_ip = mycursor.fetchall()

if len(var_con_ip)>0:
  lista_sum = lista_sum + '<select name = "'+str(id_plantilla[0][0])+'_variable_suma_ipv4">'
  for elemn in var_con_ip:
    lista_sum = lista_sum + '<option value = "'+str(elemn[1])+'">'+str(elemn[1])+'</option>'
  lista_sum = lista_sum + '</select>&nbsp;&nbsp;&nbsp;<span style="font-size:16px"><b>+</b></span>&nbsp;&nbsp;'
  cuanto = '<input type="text" id="campo_cuanto_ipv4" name="'+str(id_plantilla[0][0])+'_variable_cuanto_ipv4" pattern="^[1-9]$" title="Numero del 1 al 9" size="25"/><br><span style="color:'+informativo+';font-size:11px">*Indica la cantidad que se sumara a la variable seleccionada.</span></span>'
else:
  lista_sum = lista_sum + 'Esta plantilla no tiene variables de tipo IPv4.<span id="campo_cuanto_ipv4" style="display:none"></span>'
  cuanto = ''

print '<td><select id="tipo_de_variable" name = "'+str(id_plantilla[0][0])+'_variable_tipo">'+lista+'</select>'
print '''<br><span style="color:white;font-size:11px">
      a</span>'''
print '</td>'
print '<td><span id="tipo_suma_ipv4" style="display:none">'+lista_sum
print '''<br><span style="color:white;font-size:11px">
      a</span></span>'''
print '</td>'
print '<td><span id="tipo_cuanto_ipv4" style="display:none">'+cuanto
print '</td>'
print '<td><span id="tipo_custom" style="display:none"><input type="text" id="campo_tipo_custom" name="'+str(id_plantilla[0][0])+'_variable_regex" size="25"/>'
print '''<br><span style="color:'''+informativo+''';font-size:11px">
      *Sera considerado si variable es tipo "Personalizado"</span></span>'''
print '</td>'
print '<td><span id="tipo_lista" style="display:none"><input type="text" id="campo_tipo_lista" name="'+str(id_plantilla[0][0])+'_variable_items" size="25"/>'
print '''<br><span style="color:'''+informativo+''';font-size:11px">
      *Escribe los items separados por comas.</span></span>'''
#print '<td><input type="checkbox" name="requerido" value="requerido"> Var. Obligatoria<br><br></td>'
print '</td>'
print '</tr>'
print '<tr><td colspan="6">'
print '<span id="tipo_custom_link" style="font-size:11px;display:none">'
print '<a href="https://regex101.com/" target="_blank">Ingresa aquí para testear tu Expresión Regular</a><br><a href="https://regexone.com/lesson/introduction_abcs" target="_blank">Ingresa aquí para aprender a usar Expresiones Regulares</a><br><br>'
print '</span>'
print '</td></tr>'
print '<tr><td><b>Comentario</b></td></tr>'

print '<tr><td><input type="text" name="'+str(id_plantilla[0][0])+'_variable_comentario" size="25"/>'
print '''<br><span style="color:white;font-size:11px">
      a<br>a</span>'''
print '</td></tr>'

print '</table>'

print '''<script>
// Disclaimer: using a library (jquery, ext-core, prototype) to bind events and change 
// styles is safer across browsers
document.getElementById('tipo_de_variable').onchange = function() {
  if (this.options[this.selectedIndex].text == "Lista"){
    var display = "none";
    document.getElementById('tipo_custom').style.display = display;
    document.getElementById('campo_tipo_custom').required = false;
    document.getElementById('texto_custom').style.display = display;
    document.getElementById('tipo_custom_link').style.display = display;
    document.getElementById('texto_suma_ipv4').style.display = display;
    document.getElementById('tipo_suma_ipv4').style.display = display;
    document.getElementById('tipo_cuanto_ipv4').style.display = display;
    document.getElementById('campo_cuanto_ipv4').required = false;
    var display = "inline";
    document.getElementById('tipo_lista').style.display = display;
    document.getElementById('campo_tipo_lista').required = true;
    document.getElementById('texto_lista').style.display = display;
  }else if (this.options[this.selectedIndex].text == "IPv4 Suma"){
    var display = "none";
    document.getElementById('tipo_custom').style.display = display;
    document.getElementById('campo_tipo_custom').required = false;
    document.getElementById('texto_custom').style.display = display;
    document.getElementById('tipo_custom_link').style.display = display;
    var display = "inline";
    document.getElementById('texto_suma_ipv4').style.display = display;
    document.getElementById('tipo_suma_ipv4').style.display = display;
    document.getElementById('campo_cuanto_ipv4').required = true;
    document.getElementById('tipo_cuanto_ipv4').style.display = display;
  } else if (this.options[this.selectedIndex].text == "Personalizado"){
    var display = "none";
    document.getElementById('tipo_lista').style.display = display;
    document.getElementById('campo_tipo_lista').required = false;
    document.getElementById('texto_lista').style.display = display;
    document.getElementById('texto_suma_ipv4').style.display = display;
    document.getElementById('tipo_suma_ipv4').style.display = display;
    document.getElementById('tipo_cuanto_ipv4').style.display = display;
    document.getElementById('campo_cuanto_ipv4').required = false;
    var display = "inline";
    document.getElementById('tipo_custom_link').style.display = display;
    document.getElementById('tipo_custom').style.display = display;
    document.getElementById('campo_tipo_custom').required = true;
    document.getElementById('texto_custom').style.display = display;
  } else {
    var display = "none";
    document.getElementById('tipo_custom_link').style.display = display;
    document.getElementById('tipo_lista').style.display = display;
    document.getElementById('campo_tipo_lista').required = false;
    document.getElementById('texto_lista').style.display = display;
    document.getElementById('tipo_custom').style.display = display;
    document.getElementById('campo_tipo_custom').required = false;
    document.getElementById('texto_custom').style.display = display;
    document.getElementById('texto_suma_ipv4').style.display = display;
    document.getElementById('tipo_suma_ipv4').style.display = display;
    document.getElementById('tipo_cuanto_ipv4').style.display = display;
    document.getElementById('campo_cuanto_ipv4').required = false;
 }
}
</script>'''

################################

#ancho = 480
#ancho2 = 270

#if len(match_plantilla_var)>-1:
  #texto1 = '<td style="border-bottom:0px solid white ; border-right:6px solid rgba(255, 255, 255, 0);width:'+str(ancho2)+'"><br>Click en <b>Finalizar</b> para salir del editor de variables.</br>Recuerda que puedes agregar más variable después.</td>'
  #texto2 = '<td style="border-top:0px solid white ; border-right:6px solid rgba(255, 255, 255, 0);width:'+str(ancho2)+'"><form action = "pri_menu.php" method = "post">'
  #<input type = "radio" name = "plantilla" value = "plantilla_'''+ruta_num+'_'+str(id_plantilla[0][0])+'''" checked="checked"/>Asociar plantillas y variables<br><br>
  #texto2 = texto2 + '<br><br><input style="width:100px; height:20px;" type="submit" value = "Finalizar"/></form><br></td>'

#border-collapse: collapse;

'''
print '<br><br>'
print '<table style="border:20px solid white;width:100%;font-size:14px;">'
print '<tr align="center" style="border:0px solid white;background-color: rgba(225, 231, 242, 0.8)">'
print '<td style="border-bottom:0px solid white ; border-right:6px solid rgba(255, 255, 255, 0);width:'+str(ancho2)+'">'
print '<br>Click en <b>Aplicar</b><br>para continuar con la edición de variables</td>'
print '<td style="border-bottom:0px solid white ; border-right:6px solid rgba(255, 255, 255, 0);width:'+str(ancho2)+'"><br>Click en <b>Finalizar</b> para salir del editor de variables.</br>Recuerda que puedes agregar más variable después.</td>'
print '</tr>'
print '<tr align="center" style="border:0px solid white;background-color: rgba(225, 231, 242, 0.8)">'
print '<td style="border-top:0px solid white ; border-right:6px solid rgba(255, 255, 255, 0);width:'+str(ancho2)+'">'
print '<input style="width:100px; height:20px;" type = "submit" value = "Aplicar"/>'
print '</form><br></td>'
print '<td style="border-top:0px solid white ; border-right:6px solid rgba(255, 255, 255, 0);width:'+str(ancho2)+'"><form action = "pri_menu.php" method = "post"><br><br><input style="width:100px; height:20px;" type="submit" value = "Finalizar"/></form><br></td>'
print '</tr>'
print '</table>'

print "</body>"
print "</html>"
'''
print '<br><br>'
print '<table style="width:100%; font-size:14px">'
print '<tr>'
print '<td style="border: 5px solid rgba(255,255,255,0);background-color:rgba(255,255,255,0);width:50%">'
print '<div style="height:140px;color:white;border-radius:5px;text-align:center;background-color:rgba(0, 0, 0,0.6);"><br><br>Click en <b>Aplicar</b><br>para continuar con la edición de variables<br><br><form action = "agrega_variable.py" method = "post"><input style="width:100px; height:20px;" type = "submit" value = "Aplicar"/></form><br><br><br></div></td>'
print '<td style="border: 5px solid rgba(255,255,255,0);background-color:rgba(255,255,255,0);width:50%">'
print '<div style="height:140px;color:white;border-radius:5px;text-align:center;background-color:rgba(0, 0, 0,0.6);"><br><br>Click en <b>Finalizar</b> para salir del editor de variables.<br>Recuerda que puedes agregar más variable después.<br><br><form action = "pri_menu.php" method = "post"><input style="width:100px; height:20px;" type="submit" value = "Finalizar"/></form><br></div></td>'
print '</tr>'
print '</table>'

print "</body>"
print "</html>"
