#!/usr/bin/env python

import sys
import re
from algoritam import Algoritam
from collections import defaultdict
from array import array
import gc

proracun=Algoritam()

class KreiramIndexe:

    def __init__(self):
        self.index=defaultdict(list)    

    # Ova funkcija eliminira neke rijeci prethodno definirane u fajlu koje nece biti pretrazivane
    def eliminacijaRijeci(self):
        f=open(self.eliminacijaRijeciFajl, 'r')
        stopwords=[linija.rstrip() for linija in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        
    # Ova funkcija stavlja space za non-alfanumeric znakove, eliminira stopwords    
    def proracun(self, linija):
        linija=linija.lower()
        linija=re.sub(r'[^a-z0-9 ]',' ',linija) 
        linija=linija.split()
        linija=[x for x in linija if x not in self.sw]  
        linija=[ proracun.stem(word, 0, len(word)-1) for word in linija]
        return linija

    # Ova funkcija sredjiva id, title i text za sve fajlove uzete u analizu
    def parsamfajlove(self):
        doc=[]
        for linija in self.collFile:
            if linija=='</page>\n':
                break
            doc.append(linija)
        
        curPage=''.join(doc)
        pageid    = re.search('<id>(.*?)</id>', curPage, re.DOTALL)
        pagetitle = re.search('<title>(.*?)</title>', curPage, re.DOTALL)
        pagetext  = re.search('<text>(.*?)</text>', curPage, re.DOTALL)
        
        if pageid==None or pagetitle==None or pagetext==None:
            return {}

        d={}
        d['id']=pageid.group(1)
        d['title']=pagetitle.group(1)
        d['text']=pagetext.group(1)

        return d

    # Ova funkcija zapisuje indexe u fajl
    def zapisujemIndexe(self):
        f=open(self.indexFajl, 'w')
        for term in self.index.iterkeys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            print >> f, ''.join((term,'|',';'.join(postinglist)))
            
        f.close()
        
    # Ova funkcija uzima stopwords, text fajlova, te krajnje indexe
    def parametri(self):
        parametri=sys.argv
        self.eliminacijaRijeciFajl=parametri[1]
        self.kolekcijafajlova=parametri[2]
        self.indexFajl=parametri[3]
        
    # Ovo je glavna funkcija koja kreira indexe
    def kreiranjeIndexa(self):
        self.parametri()
        self.collFile=open(self.kolekcijafajlova,'r')
        self.eliminacijaRijeci()           
        gc.disable()
        
        fajlovidict={}
        fajlovidict=self.parsamfajlove()
        while fajlovidict != {}:                    
            lines='\n'.join((fajlovidict['title'],fajlovidict['text']))
            pageid=int(fajlovidict['id'])
            terms=self.proracun(lines)
            
            tdictfajlovi={}
            for position, term in enumerate(terms):
                try:
                    tdictfajlovi[term][1].append(position)
                except:
                    tdictfajlovi[term]=[pageid, array('I',[position])]
            
            for termpage, postingpage in tdictfajlovi.iteritems():
                self.index[termpage].append(postingpage)
            
            fajlovidict=self.parsamfajlove()


        gc.enable()
            
        self.zapisujemIndexe()
        
    
if __name__=="__main__":
    c=KreiramIndexe()
    c.kreiranjeIndexa()
    

