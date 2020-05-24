# Ask a question to wordnet database
import re
import os
import re
import nltk
from nltk.util import ngrams



def detect_main_words(question):
    print("question asked",question)
     
    word_list=[] # create list
    #word_list.append(0) # add number
    start=0
    index = 0
    while index < len(question):
        index = question.find(' ', index)   #initial value of index is -1        
        if index == -1:
            index += 1
        else:
            #print(question[start :index + 0])
            word_list.append(question[start :index + 0])
            start=index + 1
            index += 1

    return word_list
    #print(word_list)
    
#______________________________________________________________
def get_main_words(word_list):
    main_word_list=[] # create list
    file1 = open("as/assamese_stop_words.txt","r+")			# reading STOP_WORDS from assamese_stop_words.txt
    #file1 = open("as/sample.txt","r+")
    c=-1
    for i in range(len(word_list)):                   
        file1.seek(0)                                                   # Start reading the file from the begining
        for r in range(264):
            stop_word = file1.readline()
            stop_word = stop_word.rstrip('\n')
            stop_word = stop_word.rstrip(' ')
            
            if (word_list[i] == stop_word):
                c=i
        if (c != i):            
            main_word_list.append(word_list[i])
            c=-1        
    file1.close()

    return main_word_list

#______________________________________________________________   
def  get_expanded_list(main_word_list):
     
     expand_word_list= [] 
     space_added = []
     ff=open("jout.txt", "r+")     			              # READ the stemmed word
     
     for i in range(len(main_word_list)):
         stri="java AssameseStemmer " + main_word_list[i]             # using command line we passed the keyword to the javafile         
         os.system(stri)
         
        # expand_word_list.append(main_word_list[i])                   # write codes to read output of stemmer and store it in the expanded list
         stemmed = ff.readline()
         stemmed = stemmed.rstrip('\n')
         stemmed = stemmed.rstrip(' ')         
         expand_word_list.append(stemmed)
     print("expand_word_list", expand_word_list)
     
     # Add the space at Start of the string in Python
     for s in range(len(expand_word_list)):
         space_add = expand_word_list[s]
         string_length = len(space_add) + 1    # will be adding 1 extra space
         string_revised = space_add.rjust(string_length)         
         space_added.append(string_revised) 

     print("Space_added", space_added)
     ff.close()
     return space_added

#______________________________________________________________
def synset_to_list(input_file,keyword, concept, example):
    position = -1
    counter=0
    start=0
    stop=0    
    ff=open("final_file.txt", "a+")				# appending the matched keyword into final file
    syno = open("matched_syno.txt","a+")
    synset_index_list = []
    printed_once = 0
    
    input_file = list(input_file.split(","))    # Synset String file is converted to list
    keyword_length = len(keyword)
    
    synset_index = -1
    for i in range(len(input_file)):
        list_var = input_file[i]
        
        input_length   = len(list_var)             
        limit = int(keyword_length / 2)                    

        if (keyword_length > input_length):
            return synset_index_list             # return should be -1 not 0 because list will return 0 if elmnt is found in 0th position    
        for c in range(input_length - limit):    # -1 was done               
            e = c
            position = e  
            index = c        
        
            for d in range(keyword_length):           #this loop will match every every single char with the input || but c= R||
                if (keyword[d] == list_var[e]):            
                    e=e+1
                else:
                    break
                if (d == keyword_length - 1):      #-1
                    counter=counter+1
                    ff.write("-->Keyword is: "+keyword)     
                    ff.write("\n Matched keyword from synset: " + input_file[i])       
                    ff.write("\nText from Synset: " + str(input_file) )
                    
                    if(printed_once == 0):
                        syno.write(str(input_file) + "\n" )   # printing Synset to file matched_syno.txt
                        printed_once = 1
                    
                    synset_index = i                
                    if(synset_index >= 0 and synset_index <=2):  
                        synset_index_list.append(synset_index)                                     
                    ff.write("\n Index= " + str(synset_index) + "\n") 
                           
    if(counter==0):       
        return synset_index_list                                 # return should be -1 not 0 because list will return 0 if elmnt is found in 0th position
    else:
        ff.write("\nKeyword occurence: " + str(counter))
        printed_once = 0
        ff.write("\n________________________________\n")
    syno.close()    
    ff.close()    
    return synset_index_list

#______________________________________________________________
def wordnet_reader(var):
    
    keyword = var
    keyword_length = len(keyword)
    print(keyword)
    #main_word_list=1			# <MW11 MW12 MW21 MW22...>     
    
    file1 = open("Assamese.syns","r+")	# READ Wordnet DATABASE	
    id_list = []
    occurence_list = []
    present_synset_list = []
 

    for i in range(1):         # HAVE TO USE LEN
        file1.seek(0)                                                   # Start reading the file from the begining
        for r in range(0,70908,6):
            ID = file1.readline()
            ID = ID.rstrip('\n')
                                 
            ID = ID[8:]                                   
            file1.readline()				# CAT
            
            concept = file1.readline()
            concept = concept.rstrip('\n')                        
            concept = concept[12:]         
                        
            example = file1.readline() 
            example = example.rstrip('\n')            
            example = example[12:]
            
            synset = file1.readline()
            synset = synset.rstrip('\n')
            synset = synset[18:]
            present_synset_list = synset_to_list(synset,keyword, concept, example)            # a list of indexes will be returned
            
            file1.readline() 			       # For empty line                                
            past_value = 0
            if (len(present_synset_list) != 0):
                for l in range(len(present_synset_list)):
                    if(past_value != ID):
                        id_list.append(ID)  
                        occurence_list.append(present_synset_list[l])    
                    
                        past_value = ID       
                         
           
    file1.close()

    print("Program Executed")
    ff=open("final_file.txt", "a+")     			# WRITE on final output file
    if (len(id_list) != 0):        
        ff.write("\n-->matched IDs: "+str(id_list))
        ff.write("\n-->Synset index under this ids: "+ str(occurence_list))
        ff.write("\n___________________________________________________\n")
    else:
        ff.write("\n-->matched IDs: "+str(id_list))
        ff.write("\n-->Synset index under this ids: "+ str(occurence_list))
        ff.write("\n___________________________________________________\n")

    ff.close()
    print(id_list)    
    
    get_concept_example(id_list)       # This fx will print the reqd sentences for wiki extraction
    ff=open("output_concept_example.txt","a+")        # Here we are adding three sentences in between the [concept + example] output of two main words
    #ff.write("\n\n")        
    ff.close() 
    return 1
    
#___________________________________________________________
def get_concept_example(id_list):

    file1 = open("Assamese.syns","r+")	# READ Wordnet DATABASE
    occurence_list = []
    present_synset_list = []
    two_space = 0
 

    for i in range(len(id_list)):         # HAVE TO USE LEN
        file1.seek(0)  
                                                         # Start reading the file from the begining
        for r in range(0,70908,6):
            ID = file1.readline() 
            ID = ID.rstrip('\n')
            ID = ID[8:]                                              
            
            file1.readline()				# CAT
            
            concept = file1.readline()
            concept = concept.rstrip('\n')                        
            concept = concept[12:]         
                        
            example = file1.readline() 
            example = example.rstrip('\n')            
            example = example.rstrip('"')             
            example = example[13:]
            
            synset = file1.readline()  
            synset = synset.rstrip('\n')            
            synset = synset[18:]
            synset = list(synset.split(",")) 
            for s in range(len(synset)):
                synset[s] = synset[s].lstrip(' ')
            del synset[3:]           
            
            file1.readline() 
            			       # For empty line 
            if (ID == id_list[i]):
                ff = open("output_concept_example.txt","a+")
                top_syn = open("top_three_synset.txt","a+")
              
                ff.write("Concept: " + concept)     #for different different IDs we are printing concept and examples
                ff.write("\nExample: " + example)
            
                if ( len(synset) == 3 ):
             
                    ff.write("\nSynsets: " + str(synset[0]) ) 
                    ff.write("," + str(synset[1]) + "\n\n")
                 
                    top_syn.write(str(synset[0])) 			# printing at max 3 synset to top_three_synset.txt
                    top_syn.write("," + str(synset[1]))
                    top_syn.write("," + str(synset[2]) + "\n")
                  
                elif ( len(synset) == 2 ):
            
                    ff.write( str(synset[0]) ) 
                    ff.write("," + str(synset[1]) + "\n\n")
                
                    top_syn.write(str(synset[0])) 			# printing at max 3 synset to top_three_synset.txt
                    top_syn.write("," + str(synset[1]) + "\n")
                    
                else:
                    ff.write("\nSynsets: " + str(synset[0]) + "\n\n")
                
                    top_syn.write(str(synset[0]) + "\n")
             
                ff.close()  
                top_syn.close()                    
        
           
    file1.close()
    return 1
#___________________________________________________________

#___________________________________________________________ can detect 0 word or multiple words in a single sentence
def main():
    question = "বাঘ "## Make sure we have 1 space at the end to get individual words and remove . or ?
    ff=open("final_file.txt","a+")
    ff.write("Question is: "+question +"\n_____________________________________________________________\n")
    #ff.close() 
    
    word_list = [] 
    main_word_list = []
    expand_word_list = []
    concept_example_list = []
    temp = []
    
    # FUNCTION CALL 1: returns list of words
    word_list = detect_main_words(question)   
    ff.write("The word list contains: "+ str(word_list) + "\n")
    
    # FUNCTION CALL 2: returns list of main words
    main_word_list = get_main_words(word_list)
    ff.write("The Main word list contains: "+ str(main_word_list)+ "\n")
    
    # FUNCTION CALL 3: returns list of expanded words
    expand_word_list = get_expanded_list(main_word_list)
    ff.write("After Stemming main word list contains: "+ str(expand_word_list)+ "\n")
    ff.write("______________________________________________________________\n")
    
    ff.close()
    
    for i in range(len(expand_word_list)):
        wordnet_reader(expand_word_list[i])
    
    # Now trigrams
    
    #get_trigram()
    
    
#_____________________________________________________________    
if __name__== '__main__':
    main()


