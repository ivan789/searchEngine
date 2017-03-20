#!/usr/bin/env python

import sys
import re
from algoritam import Algoritam
import copy

proracun=Algoritam()

class UpitIndeXi:

    def __init__(self):
        self.index={}

    def intersectLists(self,lists):
        if len(lists)==0:
            return []
        lists.sort(key=len)
        return list(reduce(lambda x,y: set(x)&set(y),lists))        
    
    def eliminacijaRijeci(self):
        fajl=open(self.stopwordsFile, 'r')
        stopwords=[linije.rstrip() for linije in fajl]
        self.sw=dict.fromkeys(stopwords)
        fajl.close()        

    def proracun(self, linije):
        linije=linije.lower()
        linije=re.sub(r'[^a-z0-9 ]',' ',linije) # stavljam space umjesto non-alphanumeric characters
        linije=linije.split()
        linije=[x for x in linije if x not in self.sw]
        linije=[ proracun.stem(word, 0, len(word)-1) for word in linije]
        return linije        
    
    def PostLista(self, terms):
        return [ self.index[term] for term in terms ]
       
    def dokumentiPost(self, postings):
        return [ [x[0] for x in p] for p in postings ]

    def citamIndexe(self):
        fajl=open(self.indexFile, 'r');
        for linije in fajl:
            linije=linije.rstrip()
            term, postings = linije.split('|')   
            postings=postings.split(';')        
            postings=[x.split(':') for x in postings] 
            postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]   
            self.index[term]=postings
        fajl.close()


    def tipUpita(self,q):
        if '"' in q:
            return 'PQ'
        elif len(q.split()) > 1:
            return 'FTQ'
        else:
            return 'OWQ'

    def jru(self,q):
        '''upit jedna rijec'''
        originalQuery=q
        q=self.proracun(q)
        if len(q)==0:
            print ''
            return
        elif len(q)>1:
            self.ftq(originalQuery)
            return        
        q=q[0]
        if q not in self.index:
            print ''
            return
        else:
            p=self.index[q]
            p=[x[0] for x in p]
            p=' '.join(map(str,p))  
            print p
          
    def ftq(self,q):
        q=self.proracun(q)
        if len(q)==0:
            print ''
            return
        
        li=set()
        for term in q:
            try:
                p=self.index[term]
                p=[x[0] for x in p]
                li=li|set(p)
            except:
                pass
        
        li=list(li)
        li.sort()
        print ' '.join(map(str,li))

    def pq(self,q):
        originalQuery=q
        q=self.proracun(q)
        if len(q)==0:
            print ''
            return
        elif len(q)==1:
            self.jru(originalQuery)
            return

        phraseDocs=self.pqDocs(q)

        print ' '.join(map(str, phraseDocs)) 
                
    def pqDocs(self, q):
        phraseDocs=[]
        length=len(q)
        for term in q:
            if term not in self.index:
                return []
        
        postings=self.PostLista(q)    
        docs=self.dokumentiPost(postings)
        docs=self.intersectLists(docs)
        for i in xrange(len(postings)):
            postings[i]=[x for x in postings[i] if x[0] in docs]        
        
        postings=copy.deepcopy(postings)  
        
        for i in xrange(len(postings)):
            for j in xrange(len(postings[i])):
                postings[i][j][1]=[x-i for x in postings[i][j][1]]
        
        result=[]
        for i in xrange(len(postings[0])):
            li=self.intersectLists( [x[i][1] for x in postings] )
            if li==[]:
                continue
            else:
                result.append(postings[0][i][0])    
        return result
        
    def parametri(self):
        param=sys.argv
        self.stopwordsFile=param[1]
        self.indexFile=param[2]

    def UpitIndexi(self):
        self.parametri()
        self.citamIndexe()  
        self.eliminacijaRijeci() 

        while True:
            q=sys.stdin.readline()
            if q=='':
                break
            qt=self.tipUpita(q)
            if qt=='OWQ':
                self.jru(q)
            elif qt=='FTQ':
                self.ftq(q)
            elif qt=='PQ':
                self.pq(q)   
        
if __name__=="__main__":
    q=UpitIndeXi()
    q.UpitIndexi()
