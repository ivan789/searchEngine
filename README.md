# searchEngine
search engine (Python)

Search engine is the popular term for an information retrieval (IR) system. While researchers and developers take a broader view of IR systems, consumers think of them more in terms of what they want the systems to do — namely search the Web, or an intranet, or a database. Actually consumers would really prefer a finding engine, rather than a search engine.
Search engines match queries against an index that they create. The index consists of the words in each document, plus pointers to their locations within the documents. This is called an inverted file. A search engine or IR system comprises four essential modules:

* A document processor
* A query processor
* A search and matching function
* A ranking capability
* While users focus on "search," the search and matching function is only one of the four modules. Each of these four modules * may cause the expected or unexpected results that consumers get when they use a search engine. 
 

The ability to search a specific web site for the page you are looking for is a very useful feature. However, searching can be complicated and providing a good search experience can require knowledge of multiple programming languages. This project will demonstrate a simple search engine including a sample application you can run in your own site.

Searching is a fundamentally difficult problem. There are many different search algorithms. This program uses linear search, one of the most basic. That means that the program simply opens each file, looks for the terms, and closes the file. This program will not build any type of search index.

A search index is a file or set of data built before the search is performed. The index lists all the possible terms you could search for in a format which is fast to search and often sorted in a useful way like a tree. Building a search index is a requirement for good performance when searching large sets of data. However, linear search can be faster when working with smaller sets. This program demonstrates just one of many possible searching algorithms.

1) First we need to find the required files for analysis and then they should be prepared: 
* sudo python document_handler.py 
(In this script we can change the name of the directory where we want to scan and search)

2) We create indexes for files that we previously identified and prepared 
* python kreirajIndex.py eliminiramRijeci.dat MojaKolekcijaFajlova.dat indexi.dat

3) Finally browsing Our documents per index 
* python upitiIndexi.py eliminiramRijeci.dat indexi.dat

4) If we want words instead Index of document, first prepare Index:
* python kreiranjeIDIndexa.py eliminiramRijeci.dat MojaKolekcijaFajlova.dat Index2option.dat naslovIndex.dat

5) then search your document:
*  python upitiIndexiRank.py eliminiramRijeci.dat Index2option.dat naslovIndex.dat




# Document Processor 
The document processor prepares, processes, and inputs the documents, pages, or sites that users search against. The document processor performs some or all of the following steps:

* Normalizes the document stream to a predefined format.
* Breaks the document stream into desired retrievable units.
* Isolates and metatags subdocument pieces.
* Identifies potential indexable elements in documents.
* Deletes stop words.
* Stems terms.
* Extracts index entries.
* Computes weights.
* Creates and updates the main inverted file against which the search engine searches in order to match queries to documents.



