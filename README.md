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

Steps 1-3: Preprocessing. While essential and potentially important in affecting the outcome of a search, these first three steps simply standardize the multiple formats encountered when deriving documents from various providers or handling various Web sites. The steps serve to merge all the data into a single consistent data structure that all the downstream processes can handle. The need for a well-formed, consistent format is of relative importance in direct proportion to the sophistication of later steps of document processing. Step two is important because the pointers stored in the inverted file will enable a system to retrieve various sized units — either site, page, document, section, paragraph, or sentence.

Step 4: Identify elements to index. Identifying potential indexable elements in documents dramatically affects the nature and quality of the document representation that the engine will search against. In designing the system, we must define the word "term." Is it the alpha-numeric characters between blank spaces or punctuation? If so, what about non-compositional phrases (phrases in which the separate words do not convey the meaning of the phrase, like "skunk works" or "hot dog"), multi-word proper names, or inter-word symbols such as hyphens or apostrophes that can denote the difference between "small business men" versus small-business men." Each search engine depends on a set of rules that its document processor must execute to determine what action is to be taken by the "tokenizer," i.e. the software used to define a term suitable for indexing.

Step 5: Deleting stop words. This step helps save system resources by eliminating from further processing, as well as potential matching, those terms that have little value in finding useful documents in response to a customer's query. This step used to matter much more than it does now when memory has become so much cheaper and systems so much faster, but since stop words may comprise up to 40 percent of text words in a document, it still has some significance. A stop word list typically consists of those word classes known to convey little substantive meaning, such as articles (a, the), conjunctions (and, but), interjections (oh, but), prepositions (in, over), pronouns (he, it), and forms of the "to be" verb (is, are). To delete stop words, an algorithm compares index term candidates in the documents against a stop word list and eliminates certain terms from inclusion in the index for searching.

Step 6: Term Stemming. Stemming removes word suffixes, perhaps recursively in layer after layer of processing. The process has two goals. In terms of efficiency, stemming reduces the number of unique words in the index, which in turn reduces the storage space required for the index and speeds up the search process. In terms of effectiveness, stemming improves recall by reducing all forms of the word to a base or stemmed form. For example, if a user asks for analyze, they may also want documents which contain analysis, analyzing, analyzer, analyzes, and analyzed. Therefore, the document processor stems document terms to analy- so that documents which include various forms of analy- will have equal likelihood of being retrieved; this would not occur if the engine only indexed variant forms separately and required the user to enter all. Of course, stemming does have a downside. It may negatively affect precision in that all forms of a stem will match, when, in fact, a successful query for the user would have come from matching only the word form actually used in the query.

Systems may implement either a strong stemming algorithm or a weak stemming algorithm. A strong stemming algorithm will strip off both inflectional suffixes (-s, -es, -ed) and derivational suffixes (-able, -aciousness, -ability), while a weak stemming algorithm will strip off only the inflectional suffixes (-s, -es, -ed).

Step 7: Extract index entries. Having completed steps 1 through 6, the document processor extracts the remaining entries from the original document. For example, the following paragraph shows the full text sent to a search engine for processing:


Step 8: Term weight assignment. Weights are assigned to terms in the index file. The simplest of search engines just assign a binary weight: 1 for presence and 0 for absence. The more sophisticated the search engine, the more complex the weighting scheme. Measuring the frequency of occurrence of a term in the document creates more sophisticated weighting, with length-normalization of frequencies still more sophisticated. Extensive experience in information retrieval research over many years has clearly demonstrated that the optimal weighting comes from use of "tf/idf." This algorithm measures the frequency of occurrence of each term within a document. Then it compares that frequency against the frequency of occurrence in the entire database.

Not all terms are good "discriminators" — that is, all terms do not single out one document from another very well. A simple example would be the word "the." This word appears in too many documents to help distinguish one from another. A less obvious example would be the word "antibiotic." In a sports database when we compare each document to the database as a whole, the term "antibiotic" would probably be a good discriminator among documents, and therefore would be assigned a high weight. Conversely, in a database devoted to health or medicine, "antibiotic" would probably be a poor discriminator, since it occurs very often. The TF/IDF weighting scheme assigns higher weights to those terms that really distinguish one document from the others.

Step 9: Create index. The index or inverted file is the internal data structure that stores the index information and that will be searched for each query. Inverted files range from a simple listing of every alpha-numeric sequence in a set of documents/pages being indexed along with the overall identifying numbers of the documents in which the sequence occurs, to a more linguistically complex list of entries, the tf/idf weights, and pointers to where inside each document the term occurs. The more complete the information in the index, the better the search results. 
 

Query Processor 
Query processing has seven possible steps, though a system can cut these steps short and proceed to match the query to the inverted file at any of a number of places during the processing. Document processing shares many steps with query processing. More steps and more documents make the process more expensive for processing in terms of computational resources and responsiveness. However, the longer the wait for results, the higher the quality of results. Thus, search system designers must choose what is most important to their users — time or quality. Publicly available search engines usually choose time over very high quality, having too many documents to search against.

