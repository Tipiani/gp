#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

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

msg_f = []

tablas = ['despliegue','modelo','plantilla','servicio','variable','vendor']
relaciones = {'area':['plantilla'],'despliegue':['plantilla'],'modelo':['plantilla'],'plantilla':['variable'],'servicio':['plantilla'],'variable':[],'vendor':['modelo','plantilla']}

def check_id(nom_tabla, nom_item):
  match_item = 1
  mycursor.execute("select id from "+str(nom_tabla)+" where nombre_"+str(nom_tabla)+" = '"+str(nom_item)+"';")
  myresult = mycursor.fetchall()
  if len(myresult) == 0:
    match_item = 0
    myresult = [[None]]
  eleid = myresult[0][0]
  eliminar_rel(eleid, match_item, nom_tabla, nom_item)
  return match_item

def eliminar_item(table, eleid, nombit):
  mycursor.execute("delete from "+str(table)+" where id = '"+str(eleid)+"';")
  mydb.commit()
  msg_f.append("Del grupo <b>"+str(table)+"s</b> se ha eliminiado el item "+str(nombit)+".<br>")

def eliminar_rel(indice, match_item, nom_tabla, nom_item):
  if len(relaciones[nom_tabla])>0 and match_item == 1:
    relacionados = relaciones[nom_tabla]
    for tabla_rel in relacionados:
      mycursor.execute("select id, nombre_"+str(tabla_rel)+" from "+str(tabla_rel)+" where "+str(nom_tabla)+"_id='"+str(indice)+"';")
      temp_result = mycursor.fetchall()
      for result_line in temp_result:
        check_id(tabla_rel, result_line[1])
        eliminar_item(tabla_rel, result_line[0], "<b>" + result_line[1] + "</b> asociado al item <b>" + nom_item + "</b> del grupo <b>" + nom_tabla + "s.</b>")
    eliminar_item(nom_tabla, indice, "<b>" + nom_item + "</b>")
  return match_item

for elemento in form: 
  temp.append(elemento)

# Get data from fields
if len(temp)>0:
  ii = 0
  var = temp[0]
  tabla = var
  
  nombre_item = form.getvalue(var)
   
  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )

  mycursor = mydb.cursor()
  
  val_res = check_id(tabla, nombre_item)
  
  if val_res == 1:
    print "El item <b>"+str(nombre_item)+"</b> ha sido eliminado de la lista de <b>"+str(tabla)+"s.</b><br><br>"
    print '<div class= "lista-ele" style="width:600px;">'
    print '<div class = "lista-cont"><br>'
    print '<br>'.join(msg_f)
    print '<br><br></div></div>'
    print "<br><br>" 
    print '''<form action = "pri_menu.php" method = "post">
      <input type = "submit" value = "Inicio"/>
      </form>'''
  elif val_res == 0:
    print '<div class= "lista-ele" style="width:600px;">'
    print '<div class = "lista-cont"><br>'
    print "El item <b>"+str(nombre_item)+"</b> no existe.<br>"
    print '<br></div></div>'
    print "<br><br>"
    print '''<form action = "pri_menu.php" method = "post">
      <input type = "submit" value = "Inicio"/>
      </form>'''

print '</div>'
print "</body>"
print "</html>"
