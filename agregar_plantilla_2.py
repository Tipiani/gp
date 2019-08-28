#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import os
import re
import subprocess as sub
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

for elemento in form: 
  temp.append(elemento)

if len(temp)==7:
  
  for valval in temp:
    if 'contenido' in  valval:
      contenido_ini = valval
    elif 'modelo' in valval:
      modelo_ini = valval
    elif 'plantilla' in valval:
      plantilla_ini = valval

  nombre_plantilla = re.sub('\s+|\_+|-+','-',form.getvalue(plantilla_ini))
  nombre_plantilla = re.sub('-','hola1fer2jotache',nombre_plantilla)
  #nombre_plantilla = re.sub('\W','',nombre_plantilla)
  nombre_plantilla = re.sub('hola1fer2jotache','-',nombre_plantilla)

  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )

  mycursor = mydb.cursor()
  mycursor.execute("select nombre_plantilla from plantilla where nombre_plantilla='"+nombre_plantilla+"';")
  repetida = mycursor.fetchall()

  if len(repetida) == 0:
    datos = plantilla_ini.split('_')
    numeros = {}
    nombres = {}
    ins_part = ''
    ins_ruta = ''
    ins_val = ''
    ruta_p = ''
    for ixxj in range(1,len(datos)):
      numeros['num_'+str(independientes[ixxj-1])] = datos[ixxj]
      ins_part = ins_part + str(independientes[ixxj-1]) + '_id,'
      ins_val = ins_val + str(datos[ixxj]) + ','
      ins_ruta = ins_ruta + str(independientes[ixxj-1]) + '_' + str(datos[ixxj]) + '/'
      ruta_p = ruta_p + '_' + str(datos[ixxj])
      mycursor.execute("select nombre_"+str(independientes[ixxj-1])+" from "+str(independientes[ixxj-1])+" where id="+str(datos[ixxj])+";")
      myresult_4 = mycursor.fetchall()
      nombres['nom_'+str(independientes[ixxj-1])] = myresult_4[0][0]
 
    nombres['nom_modelo'] = form.getvalue(modelo_ini)
    mycursor.execute("select id from modelo where nombre_modelo='"+nombres['nom_modelo']+"';")
    numeros['num_modelo'] = mycursor.fetchall()[0][0]

    text_content = str(form.getvalue('contenido'))

    text_content = re.sub(r'\n+','\n',text_content)
    text_content = re.sub(r'\n\s+\n','\n',text_content)
    text_content = re.sub(r'\s+\n','\n',text_content)
  
    html_text = re.sub(r'\n','<br>',text_content)
    html_text = re.sub(r' ','&nbsp;',html_text) 

    mycursor = mydb.cursor()
    #print "insert into plantilla ("+ins_part+"modelo_id,nombre_plantilla) values ("+ins_val+","+str(numeros['num_modelo'])+",'"+nombre_plantilla+"');"
    mycursor.execute("insert into plantilla ("+ins_part+"modelo_id,nombre_plantilla,ruta) values ("+ins_val+str(numeros['num_modelo'])+",'"+nombre_plantilla+"','"+ins_ruta+"modelo_"+str(numeros['num_modelo'])+"');")
    mydb.commit()
  
    mycursor.execute("select id from plantilla where nombre_plantilla='"+str(nombre_plantilla)+"';")
    myresult_1 = mycursor.fetchall()
    numeros['num_plantilla'] = myresult_1[0][0]
 
    rutas = []
    
    rutas.append('/var/www/gestion_plantillas')

    if os.path.isdir(rutas[0]) == False:
      sub.Popen(['mkdir','/var/www/gestion_plantillas'],stdout=sub.PIPE,stderr=sub.PIPE)
      sub.Popen(['chown','apache:apache','/var/www/gestion_plantillas'],stdout=sub.PIPE,stderr=sub.PIPE)
      sub.Popen(['chmod','660','/var/www/gestion_plantillas'],stdout=sub.PIPE,stderr=sub.PIPE)
    
    mostrar = ''
    nombr = []
    contnd = []
    for eleme in independientes:
      rutas.append(rutas[len(rutas)-1]+'/'+str(eleme)+'_'+str(numeros['num_'+eleme]))
      nombr.append(eleme+'_item_'+str(numeros['num_'+eleme])+'_'+nombres['nom_'+eleme])
      contnd.append(nombres['nom_'+eleme])
      #mostrar = mostrar + '<b>'+eleme.capitalize()+':</b><br><input type="text" name="despliegue_'+nombres['nom_'+eleme]+'_'+str(numeros['num_'+eleme])+'" value="'+nombres['nom_'+eleme]+'" readonly><br><br>'
       
    rutas.append(rutas[len(rutas)-1]+'/modelo_'+str(numeros['num_modelo']))
  
    arch_plantilla = 'original_'+str(numeros['num_plantilla'])+'_'+str(nombre_plantilla)+str(ruta_p)+'_'+str(numeros['num_modelo'])+'.txt'
    
    for parte in rutas:
      if os.path.isdir(parte) == False:
        os.mkdir(parte)
  
    nueva_plantilla = open(rutas[len(rutas)-1]+'/'+arch_plantilla,'w',0)
    nueva_plantilla.write(text_content);
    nueva_plantilla.close()
  
    print 'Se ha agregado la plantilla con los siguientes datos:<br><br>'
    print '<form action = "agrega_variable.py" method = "post">'

    cabcr = ['Area','Despliegue','Servicio','Vendor','Modelo de Equipo','Nombre de Plantilla']
    nombr = nombr + ['modelo_item_'+str(numeros['num_modelo'])+'_'+nombres['nom_modelo'],'plantilla_'+nombre_plantilla]
    contnd = contnd + [nombres['nom_modelo'],nombre_plantilla]
    
    print aa_tabla.tabla_2_filas(cabcr,contnd,nombr)

    #print mostrar
    #print '<b>Modelo de Equipo:</b><br><input type="text" name="modelo_'+nombres['nom_modelo']+'_'+str(numeros['num_modelo'])+'" value="'+nombres['nom_modelo']+'" readonly>'
    #print '<br><br><b>Nombre de Plantilla:</b><br><input type="text" name="plantilla_'+nombre_plantilla+'" value="'+nombre_plantilla+'" readonly>'
    print '<br><br><b>Contenido:</b><br><br>'
    print '''<div style="height:240px;width:1000px;border:1px solid #ccc;overflow-y:scroll;overflow-x:scroll;">'''
    print html_text
    print "</div>"
    print "<br><br>"
    print '<input type = "submit" value = "Add Variables"/></form>'
    print '&nbsp;&nbsp;&nbsp;<form action = "pri_menu.py" method = "post"><input type = "submit" value = "Inicio"/></form>'

  else:
    print 'Ya existe la plantilla <b>"'+nombre_plantilla+'"</b>!'
else:
  print 'Los datos ingresados no son validos!'  

print '</div>'
print "</body>"
print "</html>"
