#!/usr/bin/env python

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def elementos():
  lista_indep = ['area','despliegue','servicio','vendor']
  lista_dep = ['modelo','plantilla','variable']

  return lista_indep, lista_dep
