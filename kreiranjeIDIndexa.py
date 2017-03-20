#!/usr/bin/env python

import sys
import re
from algoritam import Algoritam
from collections import defaultdict
from array import array
import gc
import math

proracun=Algoritam()

class kreirajIndex:

    def __init__(self):
        self.index=defaultdict(list)   
        self.titleIndex={}
        self.tf=defaultdict(list)                                         
        self.df=defaultdict(int)        
        self.numDocuments=0

    
    def eliminacijaRijeci(self):
        f=open(self.stopwordsFile, 'r')
        stopwords=[linija.rstrip() for linija in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def proracun(self, linija):
        linija=linija.lower()
        linija=re.sub(r'[^a-z0-9 ]',' ',linija) 
        linija=linija.split()
        linija=[x for x in linija if x not in self.sw]  
        linija=[ proracun.stem(word, 0, len(word)-1) for word in linija]
        return linija


    def parsam(self):
        doc=[]
        for linija in self.collFile:
            if linija=='</page>\n':
                break
            doc.append(linija)
        
        curPage=''.join(doc)
        pageid=re.search('<id>(.*?)</id>', curPage, re.DOTALL)
        pagetitle=re.search('<title>(.*?)</title>', curPage, re.DOTALL)
        pagetext=re.search('<text>(.*?)</text>', curPage, re.DOTALL)
        
        if pageid==None or pagetitle==None or pagetext==None:
            return {}

        d={}
        d['id']=pageid.group(1)
        d['title']=pagetitle.group(1)
        d['text']=pagetext.group(1)

        return d

    def zapisujemIndexe(self):
        f=open(self.indexFile, 'w')
        print >>f, self.numDocuments
        self.numDocuments=float(self.numDocuments)
        for term in self.index.iterkeys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            postingData=';'.join(postinglist)
            tfData=','.join(map(str,self.tf[term]))
            idfData='%.4f' % (self.numDocuments/self.df[term])
            print >> f, '|'.join((term, postingData, tfData, idfData))
        f.close()        
        f=open(self.titleIndexFile,'w')
        for pageid, title in self.titleIndex.iteritems():
            print >> f, pageid, title
        f.close()
        

    def parametri(self):
        param=sys.argv
        self.stopwordsFile=param[1]
        self.collectionFile=param[2]
        self.indexFile=param[3]
        self.titleIndexFile=param[4]
        

    def kreiramIndexe(self):
        self.parametri()
        self.collFile=open(self.collectionFile,'r')
        self.eliminacijaRijeci()                
        gc.disable()
        
        pagedict={}
        pagedict=self.parsam()
        while pagedict != {}:                    
            lines='\n'.join((pagedict['title'],pagedict['text']))
            pageid=int(pagedict['id'])
            terms=self.proracun(lines)
            
            self.titleIndex[pagedict['id']]=pagedict['title']
            
            self.numDocuments+=1
            
            termdictPage={}
            for position, term in enumerate(terms):
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[pageid, array('I',[position])]
            
            norm=0
            for term, posting in termdictPage.iteritems():
                norm+=len(posting[1])**2
            norm=math.sqrt(norm)
            
            for term, posting in termdictPage.iteritems():
                self.tf[term].append('%.4f' % (len(posting[1])/norm))
                self.df[term]+=1            
            for termPage, postingPage in termdictPage.iteritems():
                self.index[termPage].append(postingPage)
            
            pagedict=self.parsam()
        gc.enable()            
        self.zapisujemIndexe()        
    
if __name__=="__main__":
    c=kreirajIndex()
    c.kreiramIndexe()
    

