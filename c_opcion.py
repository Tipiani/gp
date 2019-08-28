#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import aa_cabecera
import aa_elementos
import os

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

form = cgi.FieldStorage()

independientes, dependientes = aa_elementos.elementos()
#independientes = ['area','despliegue','servicio','vendor']
#dependientes = ['modelo','plantilla','variable']

# Get data from fields
if form.getvalue('b_opcion'):

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
  print '''<script>
      function confirmar() {
      confirm("Estas seguro de aplicar el cambio?");
      }
      </script>'''
  print "<body>"
  print txt_show_menu

  opcion = form.getvalue('b_opcion')
   
  accion = opcion.split('_')
  hacer = accion[0]
  tabla = accion[1]
  
  print '<div style="height:25px;border-top:1px solid #3fa338; background-color:#3fa338; color:white"><div style="margin-left:11px;margin-top:4px;font-size:14px;font-family: Calibri, sans-serif">'+hacer.capitalize()+'r '+tabla.capitalize()+'</div></div>'
  print '<br><div style="margin:10px;">'

  def consulta2(val0,val1,val2,val3):
    mydb = mysql.connector.connect(
      host="localhost",
      user="fernando",
      passwd="f3rn4nd0",
      database="gestor_plantillas"
    )
    mycursor = mydb.cursor()
    mycursor.execute('select '+val0+' from '+val1+' where '+val2+' = '+str(val3)+';')
    return mycursor.fetchall()

  def consulta(val1):
    mydb = mysql.connector.connect(
      host="localhost",
      user="fernando",
      passwd="f3rn4nd0",
      database="gestor_plantillas"
    )
    mycursor = mydb.cursor()
    mycursor.execute('select * from '+val1+' order by nombre_'+val1+' asc;')
    return mycursor.fetchall()

  def elimina_edita(val1,val2,val3,val4,val5):
    if val4>0:
      print 'Elige el item que deseas '+str(val1)+'r:<br><br>'
      print '<form action = "'+str(val1)+'''r.py" onsubmit="return confirm('Seguro de aplicar el cambio?')" method = "post">
      <select id="brevlist" name = "'''+str(val2)+'''">'''
      print "<option value='defecto'>-- Elige un elemento --</option>"
      print val3
      print '</select>'
      print val5
      print '''<br><br><input type = "submit" value = "Aplicar cambio"/>
      </form>'''
      print '''<form action = "pri_menu.py" method = "post">
      <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
      </form>

<script>
document.getElementById('brevlist').onchange = function() {
  document.getElementById('newname').value = this.options[this.selectedIndex].text;
}
</script>
'''
    else:
      print "La lista de "+val2+"s esta vacia!<br><br><br>"
      print '''<form action = "pri_menu.py" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''
    
  if tabla in independientes:
    myresult = consulta(tabla)
    lista = ''
    lista_2 = ''
    if len(myresult)>0:
      for val in myresult:
        lista = lista + '<option value = "'+str(val[2])+'">'+str(val[2])+'</option>'
        lista_2 = lista_2 + str(val[2]) + '<br>'

    if hacer == 'agrega':
      if len(myresult)==0:
        print "La lista de "+tabla+"s esta vacia!<br><br><br>"
        #print '''<form action = "pri_menu.py" method = "post">
     #<input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     #</form>'''
      else:
        print "Actualmente se tienen los siguientes items registrados:<br><br>" + lista_2 + '<br>'
      print '''Ingresa el nombre del item que vas a agregar:<br><br>
      <form action = "d_agregar.py" method = "post">
      <input type="text" name = "'''+hacer+'_'+tabla+'''"/><br>
      <span style="color:#8c8c8c;font-size:11px">
      *Los subguiones o espacios en blanco seran reemplazados por guiones (-)<br>
      *Los caracteres no-alfanumericos seran omitidos</span><br><br><br>
      <input type = "submit" value = "Agregar" />
      </form>'''
    elif hacer == 'edita' or hacer == 'elimina':
      if hacer == 'edita':
        pedir = '''<br><br>Escribe el nuevo nombre del item seleccionado:<br><br>
        <input id="newname" style="width:400px" type="text" name = "'''+hacer+'_'+tabla+'''"/><br>
        <span style="color:#8c8c8c;font-size:11px">
        *Los subguiones o espacios en blanco seran reemplazados por guiones (-)<br>
        *Los caracteres no-alfanumericos seran omitidos</span><br>'''
      else:
        pedir = ""
      elimina_edita(hacer,tabla,lista,len(myresult),pedir)
  elif tabla == 'modelo':
    if hacer == 'agrega':
      myresult = consulta('vendor')
      if len(myresult)>0:
        lista = ''
        for val in myresult:
          lista = lista + '<option value = "vendor_item_'+str(val[0])+'">'+str(val[2])+'</option>'      
        print 'Elige el <b>Vendor</b> asociado al <b>modelo de equipo</b> que vas a agregar:<br><br>'
        print '''<form action = "agregar_modelo.py" method = "post">
        <select name = "vendor">'''
        print lista
        print '</select>'
        print '''<br><br>Escribe el nombre del <b>modelo de equipo</b> que vas a agregar:<br><br>
        <input type="text" name = "'''+hacer+'_'+tabla+'''"/><br>
      <span style="color:#8c8c8c;font-size:11px">
      *Los subguiones o espacios en blanco seran reemplazados por guiones (-)<br>
      *Los caracteres no-alfanumericos seran omitidos</span><br><br>'''
        print '''<input type = "submit" value = "Agregar"/>
        </form>'''
      else:
        print "La lista de <b>Vendors</b> esta vacia!<br><br><br>"
        print '''<form action = "pri_menu.py" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''
    elif hacer == 'edita' or hacer == 'elimina':
      myresult = consulta(tabla)
      lista = ''
      for val in myresult:
        vend = consulta2('nombre_vendor','vendor','id',val[2])
        lista = lista + '<option value = "'+str(val[3])+'">'+str(vend[0][0])+' / '+str(val[3])+'</option>'
      if hacer == 'edita':
        pedir = '''<br><br>Escribe el <b>nuevo</b> nombre del item seleccionado:<br><br>
        <input id="newname" style="width:400px" type="text" name = "'''+hacer+'_'''+tabla+'''"/><br>
      <span style="color:#8c8c8c;font-size:11px">
      *Los subguiones o espacios en blanco seran reemplazados por guiones (-)<br>
      *Los caracteres no-alfanumericos seran omitidos</span>'''
      else:
        pedir = ""
      elimina_edita(hacer,tabla,lista,len(myresult),pedir)
  elif tabla == 'plantilla':
    if hacer == 'agrega':
      listas = {}
      myresultados = {}
      vacias = []
      for indep in independientes:
        if len(consulta(indep))>0:
          listas['lista_'+str(indep)] = 'Elige el <b>'+str(indep).capitalize()+'</b> asociado a la <b>plantilla</b> que vas a agregar:<br><br><form action = "agregar_plantilla.py" method = "post"><select name = "'+str(indep)+'">'
          for val in consulta(indep):
            listas['lista_'+str(indep)] = listas['lista_'+str(indep)] + '<option value = "'+str(indep)+'_item_'+str(val[0])+'_'+str(val[2])+'">'+str(val[2])+'</option>'
          listas['lista_'+str(indep)] = listas['lista_'+str(indep)] + '</select>'
        else:
          vacias.append(indep)
      if len(vacias)==0:
        parcial = ''
        for indep in independientes:
          parcial = parcial + listas['lista_'+str(indep)] + '<br><br>'
        print parcial
        print '<br><br><input type = "submit" value = "Continuar"/></form>'
      else:
        print "La lista de <b>"+str(vacias[0]).capitalize()+"</b> esta vacia!<br><br><br>"
        print '''<form action = "pri_menu.py" method = "post">
      <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
      </form>'''
    elif hacer == 'elimina':
      myresult = consulta(tabla)
      lista = ''
      pedir = ''
      for val in myresult:
        lista = lista + '<option value = "'+str(val[5])+'">'+str(val[5])+'</option>'
      elimina_edita(hacer,tabla,lista,len(myresult),pedir)
    elif hacer == 'edita':
      myresult = consulta(tabla)
      lista = ''
      pedir = ''
      for val in myresult:
        lista = lista + '<option value = "'+str(val[5])+'">'+str(val[5])+'</option>'
      if hacer == 'edita':
        pedir = '''<br><br>Escribe el <b>nuevo</b> nombre del item seleccionado:<br><br>
        <input id="newname" style="width:400px" type="text" name = "'''+hacer+'_'''+tabla+'''"/><br>
      <span style="color:#8c8c8c;font-size:11px">
      *Los subguiones o espacios en blanco seran reemplazados por guiones (-)<br>
      *Los caracteres no-alfanumericos seran omitidos</span>'''
      else:
        pedir = ""
      elimina_edita(hacer,tabla,lista,len(myresult),pedir) 

  print '</div>'
  print "</body>"
  print "</html>"

else:
  print "Location: pri_menu.py\r\n\r\n"
