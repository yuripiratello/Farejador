#!/usr/bin/env python

import os, psycopg2, sys
from os.path import join, getsize

if len(sys.argv)>1:
    nomeProjeto = sys.argv[1]
    print "Criando projeto ' %s ' " % (nomeProjeto)
else:
    print "Sete um nome para o projeto"
    sys.exit(0)

con = psycopg2.connect(host="localhost",user="docs",password="123mudar",database="docs")
cur = con.cursor()

cur.execute("select * from recursos_recurso where recurso = '" + nomeProjeto + "' and pai_id = 2")
result = cur.fetchall()

if cur.rowcount:
    print "Projeto ja existente"
    print "Atualizando..."
else:
    cur.execute("insert into recursos_recurso (\"tipoRecurso_id\",recurso,pai_id) values (4,'" + nomeProjeto + "',2)")
    print "Incluindo projeto: %s" % (nomeProjeto)


dirFiles = "/var/www/wiser"
i = 0

for path, dirs, files in os.walk(dirFiles):
    if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories
    atual = path.split('/')[-1]
    pai = path.split('/')[-2]
    #arquivos = files

    #verifica se e a primeira vez que ele passa por aqui, 
    #pois se for ele deve inserir no banco o diretorio raiz
    if i == 0:
        #seleciona o ID do diretorio raiz do projeto
        cur.execute("select * from recursos_recurso where recurso = '" + atual  + "' and \"tipoRecurso_id\"=2")
        if cur.rowcount:
            idPai = cur.fetchone()
            idPai = idPai[0]
        else:
        #caso o rietorio raiz do projeto nao exista no banco, e criado.
            cur.execute("select id from recursos_recurso where recurso = '" + nomeProjeto + "'")
            idProjeto = cur.fetchone()
            cur.execute("insert into recursos_recurso (\"tipoRecurso_id\",recurso,pai_id) values (2,'%s','%s')" % (atual,idProjeto[0]))

    cur.execute("select * from recursos_recurso where recurso = '" + atual  + "'")

    #print "select * from recursos_recurso where recurso = '" + atual  + "'"
    #print "Path: " + path + ""
    if not cur.rowcount:
        cur.execute("insert into recursos_recurso (\"tipoRecurso_id\",recurso,pai_id) values(2,'%s','%s')" % (atual,anterior))
        #print "Incluindo diretorio: %s -> %s \n Path do atual: %s" % (pai,atual,path)

    #print "%s -> %s -> %s " % (pai,atual,arquivos)
    
    cur.execute("select id from recursos_recurso where recurso = '%s'" % (atual))

    if cur.rowcount:
        idAnterior = cur.fetchone()
        idAnterior = idAnterior[0]
    else:
        print "Problema ao selecionar o diretorio atual no banco"
        sys.exit(0)
    
    #print "Diretorio atual: id(%s) %s " % (idAnterior,atual)

    for arquivos in files:
        cur.execute("insert into recursos_recurso (\"tipoRecurso_id\",recurso,pai_id) values(5,'%s','%s')" % (arquivos,idAnterior))
        #print "Incluido arquivo:(id=%s) %s -> %s \n Path do atual: %s" % (idAnterior,atual,arquivos,path)
        if arquivos[-3:] == "php":
            caminhoDoArquivo = "" + path + "/" + arquivos
            #print "Tipo do arquivo: " +  type(caminhoDoArquivo) + ""
            for lin in open(caminhoDoArquivo):
                cur.execute("select id from recursos_recurso where recurso = '%s'" % (arquivos))

                if cur.rowcount:
                    idArquivo = cur.fetchone()
                    idArquivo = idArquivo[0]

                if lin.find("function") >= 0:
                    funcao = ""
                    funcao = lin.strip()[9:]
                    funcao = funcao.split("//")[0]
                    funcao = funcao.replace("'","")
                    funcao = repr(funcao)
                    funcao = funcao.replace("'","")
                    
                    
                    #print "Funcao: "+ funcao +""
                    #print '''SQL:  insert into recursos_recurso ("tipoRecurso_id",recurso,pai_id) values(9,'%s','%s')''' % (funcao,idArquivo)
                    cur.execute('''insert into recursos_recurso ("tipoRecurso_id",recurso,pai_id) values(9,'%s','%s')''' % (funcao,idArquivo))



    anterior = atual


'''for arquivo in os.listdir(dirFiles):
    #print arquivo
    ini = len(arquivo)-3
    #print ini
    tipoArquivo = os.exec("file %s" % (arquivo))
    print tipoArquivo
'''
con.commit()
cur.close()
con.close()
