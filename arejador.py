#!/usr/bin/env python

import os, psycopg2, sys
from os.path import join, getsize

anterior =""
dirFiles = "/var/www/wiser"
i = 0

for path, dirs, files in os.walk(dirFiles):
    if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories
    atual = path.split('/')[-1]
    pai = path.split('/')[-2]
    arquivos = files
    print "Anterior: %s " % (anterior)
    print "%s -> %s -> %s " % (pai,atual,arquivos)

    anterior = atual


'''for arquivo in os.listdir(dirFiles):
    #print arquivo
    ini = len(arquivo)-3
    #print ini
    tipoArquivo = os.exec("file %s" % (arquivo))
    print tipoArquivo
'''

