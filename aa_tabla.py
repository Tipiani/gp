#!/usr/bin/env python

def tabla_2_filas(cabeceras,contenido,nombres):
  cuadro = '<table><tr align = "center" style="font-size:12px">'
  if len(cabeceras) == len(contenido) and len(cabeceras) == len(nombres):
    for cab in cabeceras:
      cuadro = cuadro + '<td><b>' + cab + '</b></td>'
    cuadro = cuadro + '</tr><tr align="center">'

    for ele in range(0,len(contenido)):
      cuadro = cuadro + '<td><input style="text-align: center;" type="text" name="'+str(nombres[ele])+'" value="'+str(contenido[ele])+'" readonly></td>'
    cuadro = cuadro + '</tr><table>'
  else:
    cuadro = cuadro + '<td>La cantidad de elementos por fila no coinciden.</td></tr></table>'

  return cuadro
