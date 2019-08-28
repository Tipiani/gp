#!/usr/bin/env python
# encoding: utf-8

import mysql.connector
import cgi, cgitb
import re
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from datetime import datetime
import aa_cabecera
import aa_elementos
import aa_tabla

independientes, dependientes = aa_elementos.elementos()
txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

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
           color: #404040;
         }'''
print "</style>"
print "</head>"
print "<body>"
print txt_show_menu
print '<div style="border-top:1px solid #3fa338;height:25px;background-color: #3fa338; color:white"><div style="margin-left:11px;margin-top:4px;font-size:14px;font-family: Calibri, sans-serif">'+u'Generar Configuración'+'</div></div>'
print '<div style="margin:10px;">'
print '<br><div style="margin:10px;">'
form = cgi.FieldStorage()

listado_items = independientes + ['modelo','plantilla']

camposdict = {}

#print form
#print '<br><br>'

var_form = []

for campo in form:
  if 'var_var_var_' in campo:
    var_form.append(campo)
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

def insertar(val1):
  mydb = mysql.connector.connect(
    host="localhost",
    user="fernando",
    passwd="f3rn4nd0",
    database="gestor_plantillas"
  )
  mycursor = mydb.cursor()
  mycursor.execute(val1)
  mydb.commit()
  return

mensaje_pri = '''<div style="padding:5px;width:730px;border:1px solid #ccc;">
      <b>Importante:</b><br>
      <ul>
      <li>Solo se muestran los despliegues, servicios, vendors y modelos asociados a plantillas.</li>
      </ul></div><br>
      <div style="padding:5px;width:730px;border:1px solid #ccc;">
      <a href="ver_plantillas.py" target="_blank">Ver lista de plantillas existentes</a>
      </div><br><br>
      '''

def genera_config():
  primera_parte = ''
  for ruta_item in listado_items:
    if ruta_item == 'plantilla':
      det_plantilla = consulta('select * from plantilla where id='+str(camposdict[ruta_item+'_item_'].split('_')[2])+';')
      comp_plantilla = 'original_'+str(det_plantilla[0][0])+'_'+det_plantilla[0][5]+'_'+str(det_plantilla[0][7])+'_'+str(det_plantilla[0][6])+'_'+str(det_plantilla[0][2])+'_'+str(det_plantilla[0][3])+'_'+str(det_plantilla[0][4])+'.txt'
    elif ruta_item+'_item_' in camposdict:
      primera_parte = primera_parte + '/' + camposdict[ruta_item+'_item_'].split('_')[0] + '_' + camposdict[ruta_item+'_item_'].split('_')[2]

  ruta_plant = '/var/www/gestion_plantillas' + primera_parte + '/' + comp_plantilla

  log = "insert into gp_log (inicio,fin,accion,nombre_elemento,tipo_elemento,detalle) values('"+str(form.getvalue('timestart'))+"','"+str(datetime.now())+"','Generar Config','"+str(det_plantilla[0][5])+"','plantilla','"

  open_plant = open(ruta_plant,'r',0)
  plantilla_reempl = open_plant.read()
  open_plant.close()

  fin_config = plantilla_reempl.replace('\n','<br>')
  fin_config = fin_config.replace(' ','&nbsp;')
  mensajeadv = ''
  abcd = 0
  #var_form = ['var_var_var_IP-WAN_15_32', 'var_var_var_NUM-CIR_15_30', 'var_var_var_LAN-MASK_15_33', 'var_var_var_IP-WAN-GW_15_31'] 
  for varvar1 in var_form:
    log = log + varvar1.split('_')[3] + ':' + form.getvalue(varvar1) + ';' 
    var_fijo = varvar1.split('_')[3]
    var_dato = consulta('select * from variable where id='+str(varvar1.split('_')[5])+';')
    if re.search(var_dato[0][5],form.getvalue(varvar1)) == None and var_dato[0][4] != "ipv4_suma" and var_dato[0][4] != "lista":
      mensajeadv = "<b>Operacion Cancelada:</b><br><br>Has alterado la estructura del formulario?<br><br>El dato ingresado para la variable <b>"+var_dato[0][3]+"</b> no coincide con el formato que tiene definido <b>"+var_dato[0][5]+"</b>."
      break
    else:
      fin_config = fin_config.replace(str(var_dato[0][6].replace(' ','&nbsp;')),'<span title="var: '+str(varvar1.split('_')[3])+'" style="background-color:rgba('+str(var_dato[0][7])+')">'+str(form.getvalue(varvar1).replace(' ','&nbsp;'))+'</span>')
  
  log = log + "');"
  
  insertar(log)

  if len(mensajeadv) == 0:
    print '<span style="font-size:14px"><b>'+u'Configuracion'+' lista!</b></span><br><br>'
    print fin_config
  else:
    print mensajeadv

def show_formulario(plantilla):
  #print '<div style="text-align:center;border:1px solid black;border-top-left-radius:4px;border-top-right-radius:4px;height:30px;width:300px"><div style="margin-top:5px">Ruta de la plantilla seleccionada</div></div><br><br>'

  print '<form action = "generar_config.py" method = "post">'

  fila_1 = ''
  fila_2 = ''
  
  colorhead = '#032945'
  colorform ='#f0f0f0'
  border = '3px'

  for l_items in listado_items:
    ancho_input = ''
    if l_items == 'plantilla':
      #ancho_input = 'width:'+str(len(camposdict[l_items+'_item_'].split('_')[3])*8)+'px;'
      ancho_input = 'width:179px;'
    fila_1 = fila_1 + '<td><b>'+l_items.capitalize()+'</b></td>'
    fila_2 = fila_2 + '<td><input style="'+ancho_input+'text-align: center;" type="text" name="'+str(camposdict[l_items+'_item_'])+'" value="'+str(camposdict[l_items+'_item_'].split('_')[3])+'" readonly></td>'
  print '<div style="color:white;background-color:'+str(colorhead)+';text-align:center;border:1px solid '+str(colorhead)+';border-top-left-radius:'+border+';border-top-right-radius:'+border+';height:30px;width:300px"><div style="margin-top:7px"><b>Ruta de la plantilla seleccionada</b></div></div>'
  print '<div style="background-color:'+str(colorform)+';width:1200px;border-radius:'+border+';border-top-left-radius:0px;border:1px solid '+str(colorform)+'"><br>' 
  print '<table style="margin-left:8px">'
  print '<tr align = "center" style="font-size:14px">' + fila_1 + '</tr>'
  print '<tr align="center">' + fila_2 + '</tr>'
  print '</table>'
  print '<br><br></div>'  
 
  prev_variables = consulta('select * from variable where plantilla_id='+str(plantilla)+';')
  variables = unico(prev_variables)
  
  var_como_list = consulta('select var_lista from plantilla where id='+str(plantilla)+';')
  if var_como_list[0][0] == 'si':
    camp_lista_var = '<b><span style="font-size:12px">Lista de variables y valores</span></b><br><input id="var_plantilla" type="text" name="lista_de_var" size="100" required><br><br>'
    estilo = 'style="background-color:#eeeeee"'
  else:
    camp_lista_var = '<input style="display:none" id="var_plantilla" type="text" name="lista_de_var" size="100">'
    estilo = ''

  formulario = '' 
  sumados = ''
  
  #print '<br><br>Datos para generar configuracion<br><br>' 
  #print camp_lista_var
  print '<br><br>'
  print '<div style="color:white;background-color:'+str(colorhead)+';text-align:center;border:1px solid '+str(colorhead)+';border-top-left-radius:'+border+';border-top-right-radius:'+border+';height:30px;width:300px"><div style="margin-top:7px"><b>Datos para generar configuracion</b></div></div>'
  print '<div style="background-color:'+str(colorform)+';width:1200px;border-radius:'+border+';border-top-left-radius:0px;border:1px solid '+str(colorform)+'"><br>'
  print '<table style="margin-left:8px">'
  print '<tr><td colspan="2">'
  print camp_lista_var
  print '</td></tr>'
 
  sumados_d = {}
  sumados = ''
  listafuncempty = ''

  #if len(variables) == 0:
  #  print "La plantilla seleccionada no existe. Es posible que haya sido eliminada justo antes de ser seleccionada."
  #  sys.exit()

  for campo_form in variables:
    var_id = campo_form[0]
    plant_id = campo_form[2]
    nombre = campo_form[3]
    tipo = campo_form[4]
    comentario = re.sub(' ','&nbsp;',campo_form[8])
    referencia = consulta('select relacion_palabra,contenido from variable where id='+str(var_id)+';')
    formulario = formulario+'<tr><td><span style="font-size:12px"><b>'+str(nombre)+'</b></span>'+'<br><span style="font-size:10px">(<b>Tipo:</b> '+str(tipo)+', <b>Ejm:</b> '+referencia[0][0]+')<br><br></span></td><td>'
    if tipo == 'lista':
      formulario = formulario+'&nbsp;&nbsp;<select name = "var_var_var_'+str(nombre)+'_'+str(plant_id)+'_'+str(var_id)+'">'
      lista_items = campo_form[5].split(',')
      for itemsss in lista_items:
        formulario = formulario + '<option value = "'+str(itemsss)+'">'+str(itemsss)+'</option>'
      formulario = formulario+'</select>'
    elif tipo == 'ipv4_suma':
      formulario = formulario+'&nbsp;&nbsp;<input style="background-color:#eeeeee" id="'+str(nombre)+'" type="text" name="var_var_var_'+str(nombre)+'_'+str(plant_id)+'_'+str(var_id)+'" title="Tipo: '+str(tipo)+'" size="30" readonly>'
      suma_ref = campo_form[5].split('&nbsp;+&nbsp;')[0]
      a_sumar = campo_form[5].split('&nbsp;+&nbsp;')[1]
      
      if suma_ref in sumados_d:
        sumados_d[suma_ref] = str(sumados_d[suma_ref]) + ',' + str(nombre) +'_-_-_' + str(a_sumar)
      else:
        sumados_d[suma_ref] = str(nombre) +'_-_-_' + str(a_sumar)

    else:
      formulario = formulario+'&nbsp;&nbsp;<input '+estilo+' id="'+str(nombre)+'" type="text" name="var_var_var_'+str(nombre)+'_'+str(plant_id)+'_'+str(var_id)+'" pattern="'+referencia[0][1]+'" title="Tipo: '+str(tipo)+'" size="30" required>'
    formulario = formulario + '&nbsp;&nbsp;<span style="font-size:13px;"><b>'+str(comentario)+'</b></span><span style="font-size:10px"><br><br></span></td></tr>'
  print formulario
  print '</table>'
  print '<br>'
  print '</div>'
 
  for campo_form in variables:
    if campo_form[3] not in sumados_d:
      listafuncempty = listafuncempty + 'function ' + re.sub(r'\-','_',str(campo_form[3]))+ '''(){
  axxi = 1;
}'''
 
  listafunc = ''

  for elesum in sumados_d:
    listafunc = listafunc + re.sub(r'\-','_',str(elesum))+ '();'

    sumados = sumados + '''
document.getElementById("'''+str(elesum)+'''").onchange = '''+re.sub(r'\-','_',str(elesum))+''';
function '''+re.sub(r'\-','_',str(elesum))+'''() {'''
    var_sum = sumados_d[elesum].split(',')
    for parpar in var_sum:
      sumados = sumados + '''
  evaluar("'''+str(elesum)+'''", "'''+str(parpar.split('_-_-_')[0])+'''", '''+str(parpar.split('_-_-_')[1])+''')'''
    sumados = sumados + '''
}
'''
  #print '<input type="text" name="timestart" style="display:none" value="'+str(form.getvalue('timestart'))+'"/>'
  print '<input type="text" name="timestart" style="display:none" value="'+str(datetime.now())+'"/>'
  print '''<br><br><input type = "submit" value = "Continuar" style="width:100px; height:20px;"/></form><form action = "pri_menu.py" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''
  print '<br><br><br><br><br><br><br><br><br><br>'
  print '''<script>

var partes1, partes, temptxt, plen, i;

document.getElementById("var_plantilla").onchange = function() {
  var listavar = document.getElementById("var_plantilla").value.replace(/\"/g, "").split(";");
 
  for (i = 0; i < listavar.length; i++){
    if (listavar[i] != ""){
      var tempparte = listavar[i].split(":");
      if (document.getElementById(tempparte[0]) !== null) {
        document.getElementById(tempparte[0]).value = tempparte[1];    
      }
    }
  }
  '''+listafunc+'''
}

var axxi;

'''+listafuncempty+'''

function evaluar(original, sumado, cuanto){
  var soloip = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/g;
  var ipmask = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\/| )(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\d{1,2})$/g;
  var separador = /\//g;

  var test1 = soloip.test(document.getElementById(original).value);
  var test2 = ipmask.test(document.getElementById(original).value);
   
  if (test1 === true){
    partes = document.getElementById(original).value.split(".");
    plen = partes.length;
    temptxt = ''
      for (i = 0; i < plen-1; i++) {
        temptxt += partes[i] + ".";
      }
    temptxt += partes[plen-1]*1 + cuanto;
    document.getElementById(sumado).value = temptxt;
  }
  else if (test2 === true){
    partes1 = document.getElementById(original).value.split(/(\/| )/);
    partes = partes1[0].split(".");
    plen = partes.length;
    temptxt = '';
      for (i = 0; i < plen-1; i++) {
        temptxt += partes[i] + ".";
      }
    temptxt += partes[plen-1]*1 + cuanto;
    if (separador.test(document.getElementById(original).value) === true){
      document.getElementById(sumado).value = temptxt.concat("/",partes1[2]);
    }
    else {
      document.getElementById(sumado).value = temptxt.concat(" ",partes1[2]);
    }
  }
  else {
    document.getElementById(sumado).value = "?";
  }
}

'''+str(sumados)+'''

  </script>'''

def revision(item_gen):
  inicial_1 = ''
  inicial_2 = ''

  cabcr = []
  contn = []
  nombr = []

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

  prevresult_1 = consulta('select distinct '+ itemstabla +' from '+inicial_1+'plantilla, variable where '+inicial_2+'plantilla.id = variable.plantilla_id;') 

  myresult_1 = unico(prevresult_1)

  if len(item_gen)>1:
    for numitem in range(0,len(item_gen)-1):
      for x,y in camposdict.items():
        if item_gen[numitem] in x:
          aparece_item = y.split('_')[3] 
          cabcr.append(item_gen[numitem].capitalize())
          contn.append(str(aparece_item))
          nombr.append(str(y))
    
    estatico = aa_tabla.tabla_2_filas(cabcr,contn,nombr) + '<br><br>'

  else:
    estatico = ''

  lista_1 = ''

  if len(myresult_1)>0:
    for val in myresult_1:
      lista_1 = lista_1 + '<option value = "'+item_gen[len(item_gen)-1]+'_item_'+str(val[0])+'_'+str(val[2])+'">'+str(val[2])+'</option>'
    print mensaje_pri
    print '''<form action = "generar_config.py" method = "post">'''
    print estatico
    print '<b>'+item_gen[len(item_gen)-1].capitalize()+'</b> asociado(a) a la <b>configuracion</[3]b> que vas a generar:<br><br>'
    print '<select name = "'+item_gen[len(item_gen)-1]+'_item_">'
    print lista_1
    print '</select>'
    #print '<input type="text" name="timestart" style="display:none" value="'+str(datetime.now())+'"/>'
    print '<br><br><br><input type = "submit" value = "Continuar" style="width:100px; height:20px;"/></form>'
    print '''&nbsp;&nbsp;&nbsp;<form action = "pri_menu.py" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''
  elif len(myresult_1)==0:
    print "La lista de <b>"+item_gen[len(item_gen)-1].capitalize()+"s</b> esta vacia!<br><br>"
    print '''<form action = "pri_menu.py" method = "post">
     <input type = "submit" value = "Inicio" style="width:100px; height:20px;"/>
     </form>'''

# Get data from fields

if len(var_form)>0:
  genera_config()
elif len(camposdict)<len(listado_items):
  if len(camposdict) == 0:
    revision([listado_items[0]])
  else:
    revision(listado_items[0:len(camposdict)+1])
elif len(camposdict)>len(listado_items)-2:
  id_plantilla = camposdict["plantilla_item_"].split('_')[2]
  show_formulario(id_plantilla)

print '</div>'
print "</body>"
print "</html>"
