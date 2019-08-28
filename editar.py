#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import re
import sys
import os

import aa_cabecera

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

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

#print form

# Get data from fields
if len(temp)>0:
  ii = 0

  if '_' in temp[0]:
    tabla = temp[1]
    newname = temp[0]
  else:
    tabla = temp[0]
    newname = temp[1]

  opcion = re.sub(r'\s+|-','-',form.getvalue(tabla))
  opcion = re.sub(r'_+','_',opcion)
  opcion = re.sub(r'-','hola1fer2jotache',opcion)
  opcion = re.sub(r'_','hola1fer2subjotache',opcion)
  opcion = re.sub(r'\W','',opcion)
  opcion = re.sub(r'hola1fer2jotache','-',opcion)  
  opcion = re.sub(r'hola1fer2subjotache','_',opcion)

  nuevo = re.sub(r'\s+|-','-',form.getvalue(newname))
  nuevo = re.sub(r'_+','_',nuevo)
  nuevo = re.sub(r'-','hola1fer2jotache',nuevo)
  nuevo = re.sub(r'_','hola1fer2subjotache',nuevo)
  nuevo = re.sub(r'\W','',nuevo)
  nuevo = re.sub(r'hola1fer2jotache','-',nuevo)
  nuevo = re.sub(r'hola1fer2subjotache','_',nuevo)
  
  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )

  mycursor = mydb.cursor()
  mycursor.execute("select nombre_"+str(tabla)+" from "+str(tabla)+";")
  myresult = mycursor.fetchall()

  mycursor.execute("select * from "+str(tabla)+" where nombre_"+str(tabla)+"='"+str(opcion)+"';")
  datospl = mycursor.fetchall()
  
  j = 0

  for valor in myresult:
    if valor[0] == nuevo:
      j+=1  
 
  if j>0:
    print "Ya existe un item con el nombre <b>"+str(nuevo)+"</b>.<br><br>"
  else:
    mycursor.execute("select nombre_"+str(tabla)+" from "+str(tabla)+" where nombre_"+str(tabla)+"='"+str(opcion)+"';")
    resultados = mycursor.fetchall()
    if len(resultados)==0:
      print "No existe el item <b>"+str(opcion)+"</b>!<br><br>"
    else:
      mycursor.execute("update "+str(tabla)+" set nombre_"+str(tabla)+"='"+str(nuevo)+"' where nombre_"+str(tabla)+"='"+str(opcion)+"';")
      mydb.commit()
      print "El item <b>"+str(opcion)+"</b> ha sido renombrado como <b>"+str(nuevo)+"</b>.<br><br>" 

    print '''<form action = "pri_menu.php" method = "post">
          <input type = "submit" value = "Inicio"/>
          </form>'''
  
  if tabla == 'plantilla':
    #print datospl    

    rutaold = "/var/www/gestion_plantillas/area_"+str(datospl[0][7])+"/despliegue_"+str(datospl[0][6])+"/servicio_"+str(datospl[0][2])+"/vendor_"+str(datospl[0][3])+"/modelo_"+str(datospl[0][4])+"/original_"+str(datospl[0][0])+"_"+str(datospl[0][5])+"_"+str(datospl[0][7])+"_"+str(datospl[0][6])+"_"+str(datospl[0][2])+"_"+str(datospl[0][3])+"_"+str(datospl[0][4])+".txt"

    rutanew = "/var/www/gestion_plantillas/area_"+str(datospl[0][7])+"/despliegue_"+str(datospl[0][6])+"/servicio_"+str(datospl[0][2])+"/vendor_"+str(datospl[0][3])+"/modelo_"+str(datospl[0][4])+"/original_"+str(datospl[0][0])+"_"+str(nuevo)+"_"+str(datospl[0][7])+"_"+str(datospl[0][6])+"_"+str(datospl[0][2])+"_"+str(datospl[0][3])+"_"+str(datospl[0][4])+".txt"

    #print rutaold + "\n\n" + rutanew

    os.rename(rutaold,rutanew)

print '</div>'
print "</body>"
print "</html>"
