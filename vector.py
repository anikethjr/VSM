import nltk
import os
import timeit
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from collections import Counter
import linecache
import numpy as np
import math
from math import *


# globals
docs=[]
linenums=[]
doc_frequencies=[]
Fi_list = []
union_docs = set()
linenum=0
qVector = []
query_terms = []
query_dict = Counter()
stemmer = SnowballStemmer("english")
term_freq_list=[] # will be list of list storing the frequency of each term in the docs of their posting list
term_doc_list=[] # list of list with doc ids for term
univ_dict={}  # main query dictionary


def ENPY():  # used for global weight of query
	global univ_dict
	ENPY_list = []
	for term in univ_dict:
		Fi_term = 0
		for List in univ_dict[term]:
			Fi_term += int(List[1])
		log_N = math.log(100000, 10)
		wtt = 0
		for List in univ_dict[term]:
			wtt = wtt + ((float(List[1]) / Fi_term) * math.log((float(List[1]) / Fi_term), 10) / log_N)
		ENPY_list.append(wtt+1)
	return ENPY_list

		


def LOGG(): # used for local weight of query
	global univ_dict
	LOGG_list=[]
	for term in univ_dict:
		print term
		wt = 0.2 + 0.8 * math.log((query_dict[term] + 1), 10)
		LOGG_list.append(wt)
	return LOGG_list
		


# what if the one of the query terms has a doc frequency of zero?
# to be modified
def queryVector():
	global univ_dict, qVector
	local_wt = LOGG() # should return vector
	print local_wt
	global_wt = ENPY() # should return vector
	print global_wt
	qVector = np.array(local_wt) * np.array(global_wt)
	print qVector
	# sum_of_squares = np.dot(qVector, qVector)
	# qVector = qVector / math.pow(sum_of_squares, 0.5) #normalize
	# print qVector





	# for freq in doc_frequencies:
	# 	if freq == 0:
	# 		qVector.append(0)
	# 		continue
	# 	idf = math.log((100000.0/freq + 1), 10) # N assumed to be this though it will be much much more
	# 	# print idf
	# 	qVector.append(idf)
	# # print qVector
	# qVector = np.array(qVector)
	# # print qVector
	# sum_of_squares = np.dot(qVector, qVector)
	# # print sum_of_squares
	# qVector = qVector / math.pow(sum_of_squares,0.5)
	# # print str(type(qVector))


# function to get the posting list length of the term
def getDocs(term, linenum):
	docs = [] # list of docs for a term to calculate union
	doc_freq=[] # temp list for docs and freqs in which term occurs
	# freqs=[] # Store the frequencies for each doc id
	s=linecache.getline("invindex.txt",(int)(linenum) )
	s=word_tokenize(s.decode("ISO-8859-1"))

	for i in xrange(1, len(s)):
		doc_freq.append(s[i])
		if i%2 == 0:
			if term not in univ_dict:
				univ_dict[term] = [doc_freq]
				doc_freq=[]
			else:
				univ_dict[term].append(doc_freq)
				doc_freq=[]

	for i in univ_dict[term]:
		docs.append(i[0])
	global union_docs
	union_docs = union_docs | (set(docs))  # use this to calculate doc vectors
	# print union_docs


	# for i in xrange(1,len(s)): # break into a module (for returning the union of docs) later
		# if i%2==1:
			# docs.append(s[i])
		# else:
			# freqs.append(s[i]) # to have Fi for every term
	# print docs
	# term_freq_list.append(freqs)
	# term_doc_list.append
	# doc_frequencies.append(len(docs))
	# Fi_list.append(sum(freqs)) # stores the Fi for each term
    
	

		
# kind of main function

indexfile=open("invindex.txt",'rU');
query=raw_input()
query_tokens=word_tokenize(query.decode("ISO-8859-1"))
for qt in query_tokens:    # making a list of query terms which have been stemmed
	term=stemmer.stem(qt).encode('ISO-8859-1')
	query_terms.append(term)
	query_dict[term] += 1
print query_dict
query_terms = set(query_terms) # making it a set to have the membership checking as O(1)
# print query_terms


start = timeit.default_timer()

termsfile=open("terms.txt",'rU');
count = 0
count_limit = len(query_terms)
# print count_limit
for line in termsfile:    # checking in the terms.txt whether the word of the current line matches any term of the query terms list
	pos=word_tokenize(line.decode("ISO-8859-1"))
	if (pos[0] in query_terms) and count < count_limit:
		term = pos[0]
		linenum=pos[1]
		count += 1
		getDocs(term, linenum)
	elif count > count_limit:
		break
#print univ_dict
queryVector()
	#if linenum not in linenums:
	#linenums.append(linenum)
	# print linenum
	# s=linecache.getline("invindex.txt",(int)(linenum) )
	# s=word_tokenize(s.decode("ISO-8859-1")) 
	# #s is the posting list for the "term"
	
	# for i in xrange(1,len(s)): # break into a module (for returning the union of docs) later
	# 	if i%2==1:
	# 		docs.append(s[i])

	# # print docs
	# doc_frequencies.append(len(docs))
	
#    union_docs = union_docs | (set(docs))
	# docs=[]
# print list(union_docs)
stop = timeit.default_timer()
# print doc_frequencies
print stop-start
termsfile.close()
indexfile.close()	
