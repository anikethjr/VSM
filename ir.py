# function to populate the inverted index

inverted_index = {}
def addToInvertedIndex(token_list, prod_ID):
    i = 0
    flag = 0
    list_len = len(token_list)
    for token in token_list:
#         flag2 = 0
        """ inverted_index[token_list[i]] will be a list of lists """
        if token not in inverted_index: # token not in inverted index
            inverted_index[token] = [[str(prod_ID), 1]]
        else:
            List_of_Lists = inverted_index[token]
#             print "LOL " + str(type(List_of_Lists))
            for List in List_of_Lists:
#                 print List
                if List[0] == str(prod_ID):
                    List[1] += 1
                    flag = 1
#                   
            if(not flag):
                inverted_index[token].append([str(prod_ID), 1])






# Extracting each review for tokenization and normalization
import timeit
import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
f = open('foods.txt', 'rU')
g = open('invindex.txt','w')

count = 0
review = ""
start = timeit.default_timer()
for line in f:
    if line[:18].strip() == 'product/productId:':
        prod_ID = line[19:-1]
    if line[:13].strip() == 'review/text:': # Checking for the whether review line or not
        review = line[13:-1]
        reg_tokenizer = RegexpTokenizer('[(A-Z)+|(a-z)+|0-9]\w*') # Using a '+' will eliminate all single letter words
        tokens = reg_tokenizer.tokenize(review)
#         print len(review)
#         print prod_ID
#         print tokens

        """ Creating inverted index """
        
        addToInvertedIndex(tokens, prod_ID)
        
        count += 1
    review = ""
    if count == 100000:
        break
stop = timeit.default_timer()
# print inverted_index

                
