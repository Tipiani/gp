#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import re
import sys

form = cgi.FieldStorage()

import aa_cabecera

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

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
           font-size: 14px;
         }'''
print "</style>"
print "</head>"
print "<body>"
print txt_show_menu

print '<br><br><div style="margin:10px;">'

temp = []

for elemento in form: 
  temp.append(elemento)

# Get data from fields
if len(temp)>0:
  ii = 0
  var = temp[0]
  accion = var.split('_')
  tabla = accion[1]

  opcion = re.sub('\s+|\_+|-+','-',form.getvalue(var))
  opcion = re.sub('-','hola1fer2jotache',opcion)
  opcion = re.sub('\W','',opcion)
  opcion = re.sub('hola1fer2jotache','-',opcion)

  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )

  mycursor = mydb.cursor()
  mycursor.execute("select nombre_"+tabla+" from "+tabla+";")
  myresult = mycursor.fetchall()
  
  for item in myresult:
    if item[0].lower() == opcion.lower():
      ii+=1
  if ii==0:
    mycursor.execute("insert into "+str(tabla)+" (nombre_"+str(tabla)+") values ('"+str(opcion)+"');")
    mydb.commit()
    print "El item <b>"+str(opcion)+"</b> fue agregado a la lista de <b>"+str(tabla).capitalize()+"s</b> sin problemas!" 
  elif ii>0:
    print "El item <b>"+str(opcion)+"</b> ya existe!"
    
  print '''<br><br><form action = "pri_menu.php" method = "post">
        <input type = "submit" value = "Inicio"/>
        </form>'''

print '</div>'
print "</body>"
print "</html>"
