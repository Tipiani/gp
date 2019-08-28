#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import re
import aa_cabecera
import sys

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

form = cgi.FieldStorage()

if len(form) > 0:
  print "Content-type:text/html\r\n\r\n"
else:
  print "Location: pri_menu.py\r\n\r\n"
  sys.exit()

print "<html>"
print "<head>"
print "<style>"
print txt_in_css
print '''body {
           margin: 0px;
           font-family: 'Roboto', sans-serif;
           font-size: 14px;
         }'''
print "</style>"
print txt_in_head
print "</head>"
print "<body>"
print txt_show_menu

temp = {}

for elemento in form: 
  if 'agrega_modelo' in elemento:
    temp['modelo'] = elemento
  elif 'vendor' == elemento:
    temp['vendor'] = elemento

# Get data from fields
if len(temp)>0:
  ii = 0
  var = temp['modelo']
  item_vendor = temp['vendor']
  accion = var.split('_')
  tabla = accion[1]
 
  opcion = re.sub('\s+|\_+|-+','-',form.getvalue(var))
  opcion = re.sub('-','hola1fer2jotache',opcion)
  opcion = re.sub('\W','',opcion)
  opcion = re.sub('hola1fer2jotache','-',opcion)

  num_vendor = form.getvalue(item_vendor).split('_')[2]
  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )

  mycursor = mydb.cursor()
  
  mycursor.execute("select nombre_"+tabla+" from "+tabla+" where vendor_id = '"+str(num_vendor)+"';")
  myresult = mycursor.fetchall()
  
 
  for item in myresult:
    if item[0].lower() == opcion.lower():
      ii+=1
  if ii==0:
    mycursor.execute("insert into "+str(tabla)+" (vendor_id, nombre_"+str(tabla)+") values ("+str(num_vendor)+", '"+str(opcion)+"');")
    mydb.commit()
    print '<br><br>'
    print '<div style="margin:10px;">'
    print "El item <b>"+str(opcion)+"</b> fue agregado a la lista de <b>"+str(tabla)+"s</b> sin problemas!" 
  elif ii>0:
    print '<br><br>'
    print '<div style="margin:10px;">'
    print "El item <b>"+str(opcion)+"</b> ya existe!"

  print '''<br><br><br>'''
  print '''<form action = "pri_menu.py" method = "post">
        <input type = "submit" value = "Inicio"/>
        </form>'''

print '</div>'
print "</body>"
print "</html>"
