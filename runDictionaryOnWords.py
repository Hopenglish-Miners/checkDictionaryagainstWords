""""
expected imput is jason file with the following format:
"cat1":[word1,2,3,4,5,6,.....]
"cat2":[woed1,2,3,4,5,6......]
......etc
we want to output the following:
number of words being categorized in total and words not categorized.
we also need to generate a word frequency key value pair so we can generate graphs.
"""""
import json

# Directories Needed to run the Script
DIR_FILTERED_WORDS = 'in/filteredWords.json'
DIR_STUDENT_FILTEREDWORDS = 'in/student_filteredWords.json'
DIR_DICTIONARY = 'in/myvocabulary_categories.json'

def getWordsFromVideoFile (videotxtfile):
        for i in range(0, len(videotxtfile)):
            for v in videotxtfile[i]['wordList']:
                w = v
                wordlist.append(w)

def getWordsFromUserFile (userWordstxtfile):
    for i in range (0,len(userWordstxtfile)):
        for v in userWordstxtfile[i]['lemmatization_filtered']:
            w=v
            #strip whitespace just in case
            w = w.strip()
            if w in userwordslist:
                continue #woed is duplicated
            else :
                userwordslist.append(w)

def compareVideoWordsWithDict (videowords,dictionary,foundWords):
    listofdictwords=[]
    for i in range (0,len(dictionary)):
        category = dictionary[i]
        for label,words in category.items():
            #label is the label of each categories
            #words is the list of words in the dictionary
            arg=0
            foundWords[label]=0#add label to found words and set it to 0
            for word in words:#iterate over each word in the category list
                listofdictwords.append(word)
                if word in videowords:
                    #wordoccurances is the location of each occurance of the word in question
                    wordoccurances=[a for a,b in enumerate(videowords) if b==word]
                    for x in wordoccurances:
                        #for each location of our word we will add to the category found times
                        foundWords[label]=foundWords[label]+1
                        global foundcount
                        foundcount += 1
    #pass through everything to find how many words we coundnt match.
    missed = [item for item in videowords  if item not in listofdictwords]
    global missedcount
    missedcount = len(missed)

def compareUserWordsWithDict (userwords,dictionary,foundUWords):
    listofdictwords=[]
    for i in range (0,len(dictionary)):
        category = dictionary[i]
        for label,words in category.items():
            #label is the label of each categories
            #words is the list of words in the dictionary
            arg=0
            foundUWords[label]=0#add label to found words and set it to 0
            for word in words:#iterate over each word in the category list
                listofdictwords.append(word)
                if word in userwords:
                    #wordoccurances is the location of each occurance of the word in question
                    wordoccurances=[a for a,b in enumerate(userwords) if b==word]
                    for x in wordoccurances:
                        #for each location of our word we will add to the category found times
                        foundUWords[label]=foundUWords[label]+1
                        global foundUcount
                        foundUcount += 1
    #pass through everything to find how many words we coundnt match.
    missed = [item for item in userwords  if item not in listofdictwords]
    global missedUcount
    missedUcount = len(missed)

def outputuserjson (usrtxt,missedUcount,foundUcount,foundUWords):
    usrtxt['foundwords']=foundUcount
    usrtxt['missedwords']=missedUcount
    usrtxt['categorieswithcount']=foundUWords

def outputvideojson (videotxt,missedcount,foundcount,foundWords):
    videotxt['foundwords']=foundcount
    videotxt['missedwords']=missedcount
    videotxt['categorieswithcount']=foundWords


wordListFile = open(DIR_FILTERED_WORDS)
wordJson     = json.load(wordListFile)
userListFile = open(DIR_STUDENT_FILTEREDWORDS)
userWordsJson= json.load(userListFile)
dictionaryFile = open(DIR_DICTIONARY)
dictionary     = json.load(dictionaryFile)

wordlist    =   [] #words from video files
missedcount =   0  #count of how many words we coundnt match
foundcount  =   0  #count of how many words we found
foundWords  =   {} #list of categories and how many times they were found,
                   #needed to genrate distribution of words.
videotxt    =   {}
userwordslist=  [] #words from user dictionaries all amalgamated
missedUcount =   0  #User count of how many words we coundnt match
foundUcount  =   0  #User count of how many words we found
foundUWords  =  {} #User list of categories and how many times they were found,
                   #needed to genrate distribution of words.
usrtxt       =  {}

getWordsFromVideoFile(wordJson)
getWordsFromUserFile(userWordsJson) #takes long to execute, may need to enable multi threading
compareVideoWordsWithDict(wordlist,dictionary,foundWords)
compareUserWordsWithDict(userwordslist,dictionary,foundUWords)
outputvideojson(videotxt,missedcount,foundcount,foundWords)
outputuserjson(usrtxt,missedUcount,foundUcount,foundUWords)
print("information based on video words: ")
print(videotxt)
print("information based on user dictionaries: ")
print(usrtxt)
videostats = open('out/videostats.json','w')
userstats = open('out/userstats.json','w')
json.dump(videotxt,videostats)
json.dump(usrtxt,userstats)
videostats.close()
userstats.close()