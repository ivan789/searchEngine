#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ako korisnik ne zeli koristiti web formu prilikom kreiranja indexa, tada moze preko ove skriptice
generirati fajl koji je potreban za kreiranje indexa, no ako se korisnik odlucio da indexe
kreira automatski kroz web formu (koja je napisana u Djangu i prilozena u ovom repozitoriju) 
tako sto jednostavno preda ime direktorija za skeniranje i kreiranje indexa,tada 
nije potrebo koristiti ovu skripticu!
Ovo je skriptica koja priprema željene fajlove za pretraživanje,a gleda željeni direktorij
te prolazi kroz njega i hvata sve fajlove, te ih sprema u jedan veliki fajl sa XML tagovima, a ovaj
veliki fajl će kasnije biti korišten u kreiranju indexa i na posljetku za search dokumenata!
"""

import os
from fnmatch import fnmatch
try:
    root = '/'
    pattern = "*.txt"
    i = 0
    for path, subdirs, files in os.walk(root):

        for name in files:
            if fnmatch(name, pattern):
                print os.path.join(path, name)
                #print name
                
                with open(os.path.join(path, name)) as f:
                    i += 1
                    with open("MojaKolekcijaFajlova.dat", "a") as f1:

                        f1.write("<page>\n")
                        f1.write("<id>" + str(i) + "</id>\n")
                        f1.write("<title>" + str(name) + "</title>\n")
                        f1.write("<text>\n")
                        for line in f:

                            f1.write(line)
                        f1.write("</text>\n")
                        f1.write("</page>\n")
except:
    print "xml tag notification" 


