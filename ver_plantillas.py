#!/usr/bin/env python

import mysql.connector
import cgi, cgitb
import sys
import aa_cabecera
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

txt_in_css, txt_in_head, txt_show_menu = aa_cabecera.mostrar_cabecera()

form = cgi.FieldStorage()

mydb = mysql.connector.connect(
  host="localhost",
  user="fernando",
  passwd="f3rn4nd0",
  database="gestor_plantillas"
)

mycursor = mydb.cursor()
mycursor.execute("select area.nombre_area,despliegue.nombre_despliegue,servicio.nombre_servicio,vendor.nombre_vendor,modelo.nombre_modelo,plantilla.nombre_plantilla from area,despliegue, servicio, vendor, modelo, plantilla where plantilla.area_id = area.id and plantilla.despliegue_id = despliegue.id and plantilla.servicio_id = servicio.id and plantilla.vendor_id = vendor.id and plantilla.modelo_id = modelo.id;")

lista = mycursor.fetchall()

tabla = '<table id="myTable"><thead><tr><th class="cabc" onclick="sortTable(0)">#</th><th class="cabc" onclick="sortTable(1)">Area</th><th class="cabc" onclick="sortTable(2)">Despliegue</th><th class="cabc" onclick="sortTable(3)">Servicio</th><th class="cabc" onclick="sortTable(4)">Vendor</th><th class="cabc" onclick="sortTable(5)">Modelo</th><th class="cabc" onclick="sortTable(6)">Plantilla</th></tr></thead><tbody>'

ikj = 0

for fila in lista:
  ikj += 1
  tabla = tabla + '<tr class="fila-pl">'
  tabla = tabla + '<td><b>' + str(ikj) + '</b></td>'
  for celda in fila:
    tabla = tabla + '<td>' + str(celda) + '</td>'
  tabla = tabla + '</tr>'

tabla = tabla + '</tbody></table>'

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<style>"
print txt_in_css
print '''
body {
  margin: 0px;
  font-family: 'Roboto', sans-serif;
  font-size: 12px;
  }

#myTable tr:nth-child(even){
  background-color: #d7f7d2;
}

#myTable {
  margin: 5px;
  border-collapse: collapse;
  border: 0px solid white;
}

#myTable th {
  font-size:13px;
}

#myTable td {
  font-size:13px;
}

#myTable thead th {
  font-weight: bold;
  background-color:black;
  color: white;
  border: 0px solid white;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 40px;
  padding-right: 40px;
  text-align: center;
}

#myTable tbody td {
  /*background-color:#d7f7d2;*/
  color: #3a3a3a;
  border: 0px solid white;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 40px;
  padding-right: 40px;
  text-align: center;
}

th.cabc:hover {
  background-color:#919191;
  color:black;
}

tr.fila-pl:hover td{
  background-color:#3f8a33;
  color:white;
}

'''
print "</style>"
print txt_in_head
print "</head>"
print "<body>"
print txt_show_menu
print "<br><br><span style='margin-left:5px; font-size:13px'><b>Click en la cabecera de la columna que desees ordenar alfabeticamente.</b></span><br><br><br>"
print tabla

print '''<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc"; 
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;      
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>'''

print "</body>"
print "</html>"
