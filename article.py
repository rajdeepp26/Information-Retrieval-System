import os
import wikipedia
ths_file = open("top_three_synset.txt", "r+")   # read the synonyms line by line

# Create directory
dirName = 'বাঘ' 					# DIRECTORY NAME IS SPECIFIED
try:
    # Create target Directory
	os.mkdir(dirName)
	print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")	

# READING is done in next 3 lines
for line in range(8):						
	synset = ths_file.readline()
	synset = synset.rstrip('\n')
	line_f_synonym = list(synset.split(","))    # Synset String file is converted to list
	
	
	for i in range(len(line_f_synonym)):

		try:	
			wikipedia.set_lang("as")
		
			syno_word = line_f_synonym[i]				# SYNO_WORD IS SEARCHED IN WIKIPEDIA
			print(syno_word)				  		
			
		
			pg_titles = wikipedia.search(syno_word)      # pg_titles is a list			
			ths_file.write("Keyword Search: " +syno_word +"\n")
			ths_file.write("matched keyword: " + str(pg_titles) + "\n")       # we found multiple pages
		
			# now to extract contents and save it in different different documents.
			for i in range(len(pg_titles)):                          # len(pg_titles) --> too many pages to be displayed so restricted to 3.
				cur_title = pg_titles[i]
				# path for text files to be stored
				path = "বাঘ/"+cur_title+".txt"	# PATH is specified here
				wiki_content = open(path, "w")   
				
				page = wikipedia.page(cur_title )			
				wiki_content.write("Summary of "+ cur_title + ":\n" + str( page.content ) )
				wiki_content.close()
					 
		except:
			print("Not found")
		
ths_file.close()

