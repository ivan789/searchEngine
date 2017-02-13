#!/usr/bin/env python

import sys
import re
from algoritam import Algoritam
from collections import defaultdict
import copy

proracun=Algoritam()

class UpitiIndex:

    def __init__(self):
        self.index={}
        self.titleIndex={}
        self.tf={}      
        self.idf={}    


    def intersectLists(self,lists):
        if len(lists)==0:
            return []
        lists.sort(key=len)
        return list(reduce(lambda x,y: set(x)&set(y),lists))
        
    
    def eliminacijaRijeci(self):
        f=open(self.stopwordsFile, 'r')
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def proracun(self, line):
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) 
        line=line.split()
        line=[x for x in line if x not in self.sw]
        line=[ proracun.stem(word, 0, len(word)-1) for word in line]
        return line
        
    
    def listaPost(self, terms):        
        return [ self.index[term] for term in terms ]
    
    
    def elementiPost(self, postings):
        return [ [x[0] for x in p] for p in postings ]


    def citacIndexa(self):
        f=open(self.indexFile, 'r');
        self.numDocuments=int(f.readline().rstrip())
        for line in f:
            line=line.rstrip()
            term, postings, tf, idf = line.split('|')   
            postings=postings.split(';')        
            postings=[x.split(':') for x in postings] 
            postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]  
            self.index[term]=postings
            tf=tf.split(',')
            self.tf[term]=map(float, tf)
            self.idf[term]=float(idf)
        f.close()
        
        f=open(self.titleIndexFile, 'r')
        for line in f:
            pageid, title = line.rstrip().split(' ', 1)
            self.titleIndex[int(pageid)]=title
        f.close()
        
     
    def produkt(self, vec1, vec2):
        if len(vec1)!=len(vec2):
            return 0
        return sum([ x*y for x,y in zip(vec1,vec2) ])
            
        
    def rankDokumenata(self, terms, docs):
        docVectors=defaultdict(lambda: [0]*len(terms))
        queryVector=[0]*len(terms)
        for termIndex, term in enumerate(terms):
            if term not in self.index:
                continue
            
            queryVector[termIndex]=self.idf[term]
            
            for docIndex, (doc, postings) in enumerate(self.index[term]):
                if doc in docs:
                    docVectors[doc][termIndex]=self.tf[term][docIndex]
                    
        #calculate the score of each doc
        docScores=[ [self.produkt(curDocVec, queryVector), doc] for doc, curDocVec in docVectors.iteritems() ]
        docScores.sort(reverse=True)
        resultDocs=[x[1] for x in docScores][:10]
        #print document titles instead if document id's
        resultDocs=[ self.titleIndex[x] for x in resultDocs ]
        print '\n'.join(resultDocs), '\n'


    def tipUpita(self,q):
        if '"' in q:
            return 'PQ'
        elif len(q.split()) > 1:
            return 'FTQ'
        else:
            return 'OWQ'


    def jru(self,q):
        '''Upit jedna rijec'''
        originalQuery=q
        q=self.proracun(q)
        if len(q)==0:
            print ''
            return
        elif len(q)>1:
            self.ftq(originalQuery)
            return
        
        term=q[0]
        if term not in self.index:
            print ''
            return
        else:
            postings=self.index[term]
            docs=[x[0] for x in postings]
            self.rankDokumenata(q, docs)
          

    def ftq(self,q):
        q=self.proracun(q)
        if len(q)==0:
            print ''
            return
        
        li=set()
        for term in q:
            try:
                postings=self.index[term]
                docs=[x[0] for x in postings]
                li=li|set(docs)
            except:
                #term not in index
                pass
        
        li=list(li)
        self.rankDokumenata(q, li)


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
        self.rankDokumenata(q, phraseDocs)
        
        
    def pqDocs(self, q):
        phraseDocs=[]
        length=len(q)
        for term in q:
            if term not in self.index:

                return []
        
        postings=self.listaPost(q)   
        docs=self.elementiPost(postings)
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

        
    def getParams(self):
        param=sys.argv
        self.stopwordsFile=param[1]
        self.indexFile=param[2]
        self.titleIndexFile=param[3]


    def indexUpit(self):
        self.getParams()
        self.citacIndexa()  
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
        
if __name__=='__main__':
    q=UpitiIndex()
    q.indexUpit()
