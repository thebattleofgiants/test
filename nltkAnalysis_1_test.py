import datetime
import nltk
from nltk.tree import Tree
from nltk.corpus import PlaintextCorpusReader
#from nltk.corpus import wordnet as wn #used for synonyms
import csv

grammar = r"""
    CHUNK:
        {<VB.*>*<RB.*>*<JJ.*>+<NN>*<TO>*<RB.*>*}
        {<NN.*><VB.*>}
        {<VB.*>+<.*>*<RB.*>+}
    """
grammar2 = r"""
    CHUNK:
        {<JJ.*>+}
    """

with open('/Users/xiao/Desktop/python_training/naturesPath/files/product_reviews_naturespathWeb_July-12-2018.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == -1:
            print (f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            #parse out relevant information for analysis

            desc = row["desc"]
            date = row["date"]
            url = row["url"]
            url = url[:url.rfind("/")-1] #remove last /
            starRating = row["stars"]

            product = url[url.rfind("path-foods/")+11:]
            #print (product)

            sentences = nltk.sent_tokenize(desc) #break into sentences
            sent_tokens = [nltk.word_tokenize(sent) for sent in sentences]
            sent_tagged = [nltk.pos_tag(sent) for sent in sent_tokens]
            sentences = ""
            adjectives = ""

            for sent in sent_tagged:
                cp = nltk.RegexpParser(grammar)
                tree = cp.parse(sent)
                for subtree in tree.subtrees():
                    #print (subtree)
                    if subtree.label() == 'CHUNK':
                        #temp_list=[] #back into a tagged list sentence without "CHUNK"
                        #temp_list=[(word) for (word) in subtree]
                        #sentences.append(temp_list)
                        words = [word for (word,tag) in subtree]
                        words = " ".join(words)
                        sentences += (words+" - ")
                cp2 = nltk.RegexpParser(grammar2)
                tree2 = cp2.parse(sent)
                for subtree in tree2.subtrees():
                    #print (subtree)
                    if subtree.label() == 'CHUNK':
                        #temp_list=[] #back into a tagged list sentence without "CHUNK"
                        #temp_list=[(word) for (word) in subtree]
                        #sentences.append(temp_list)
                        words = [word for (word,tag) in subtree]
                        words = " ".join(words)
                        adjectives += (words+" - ")
            #print ([sentences])
            row_data = [product,date,starRating,desc,sentences,adjectives]
            with open('naturesPathReview_analysis.csv','a') as csvf:
                writer = csv.writer(csvf)
                writer.writerow(row_data)
            #print (row_data)
            line_count += 1
            csvf.close()
    print(f'Processed {line_count} lines.')

csv_file.close()


            #Formatted string literals (also called f-strings for short) let you include the value of Python expressions inside a string by prefixing the string with f or F and writing expressions as {expression}.
