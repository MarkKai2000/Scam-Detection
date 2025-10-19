import os, sys, traceback

vowel = ['a', 'e', 'o', 'i', 'u', 'y']
common_letter_replace_dic = {'b':'p','i':'1,l',"l":'i,1',"o":'0','c':'k','k':'c','p':'b','m':'n','n':'m','s':'5'}
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
double_characters = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']


digits = []
for i in range(1000):
    digits.append(i)
    

def main():
    extract_userNames_and_create_squatting_usernames()

def extract_userNames_and_create_squatting_usernames():
    numberOfUsers = 1
    lenght_of_strings = 16

    print("### Creating squatted Usernames ###")
    try:
        print("Argument List:", str(sys.argv))
        
       # name = str(sys.argv[1])
       # name = name.replace('@','')
        
        f = open('usernames.txt', 'r')
        users = f.readlines()
        f.close()
        
        path_general = ('content/general/')
        if not os.path.exists(path_general):
            os.makedirs(path_general)
        f_general = open(path_general + 'generated_usernames_all.txt', 'w', encoding = 'utf-8')
        
        for name in users:
            name = name.replace('@','').lower().strip()
            
            word = name + '\n'
            
            # gia to e2e gia na doylepsei 8eloyme '/content/@ kai oxi 'content/@'
            path = 'content/@' + name.strip() + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            f = open('content/@' + name.strip() + '/' + 'generated_usernames.txt', 'w', encoding = 'utf-8')
            dic = dict()
                
            apply_gen_models(word,dic,lenght_of_strings)
                    
            print('The length of the dictionairy is: ' + str(len(dic)))

            for item in dic:

                if (len(item.replace('\n','')) < 16):
                    if item != word:
                    #    print(item)
                        f.write('@' + item.lower().replace(',', ''))
                        f.flush()
                        f_general.write('@' + item.lower())

            f.close()
            print("### Creating squatted names program has finished ###")
            
            
            ############################## fixing the @absd@adv@sda words for earch each file
            f = open('content/@' + name.strip() + '/' + 'generated_usernames.txt', 'r', encoding = 'utf-8')
            users = f.readlines()
            f.close()
            
            
            f = open('content/@' + name.strip() + '/' + 'generated_usernames.txt', 'w', encoding = 'utf-8')
            
            temp_counter = 0
            for user in users:
                for character in user:
                    if '@' in character:
                        temp_counter += 1
                    #    print('aaaaaaaaaaaaaaaaaaaaaaaaa')
                if temp_counter < 2:
                    if user != '':
                        f.write(user)
                else:
                    result = user.split('@')[1:]
              #      print(result)
                    for item in result:
                        if item != '':
                            f.write('@' + item.strip() + '\n')
                
            f.close()
            
            ###########################################################
        
        f_general.close()
        
        
        ############################## fixing the @absd@adv@sda words for earch each file
        f_general = open(path_general + 'generated_usernames_all.txt', 'r', encoding = 'utf-8')
        users = f_general.readlines()
        f_general.close()
        
        f_general = open(path_general + 'generated_usernames_all.txt', 'w', encoding = 'utf-8')
        temp_counter = 0
        for user in users:
            for character in user:
                if '@' in character:
                    temp_counter += 1
            if temp_counter < 2:
                if user != '':
                    f_general.write(user)
            else:
                result = user.split('@')[1:]
                # print(result)
                for item in result:
                    if item != '':
                        f_general.write('@' + item.strip() + '\n')
        f_general.close()

        ###########################################################

        
    except Exception:
        print(traceback.print_exc())
        print("Something went wrong when creating a specific Username")      
    except FileExistsError:
        print("Something wrong is happending with the file")

    f = open(path_general + 'generated_usernames_all.txt', 'r', encoding = 'utf-8')
    data = f.readlines()
    f.close()
    print('Total :', len(data))

def apply_gen_models(word,dic,lenght_of_strings):

    # Vowel character insertion
    vowel_character_insertion(word,dic,lenght_of_strings) 

    # # Vowel character deletion
    vowel_character_deletion(word,dic)
                
    # # Double character insertion
    double_character_insertion(word,dic)

    # # Double character deletion
    double_character_deletion(word,dic)

    # # Vowel character substitution
    vowel_character_substitution(word,dic)

    # # Common misspelling
    common_misspelling_mistakes_substition(word,dic)
              
    # # Punctuation addition
    punctuation_addition(word,dic)

    # # Punctuation deletion
    punctuation_deletion(word,dic)

    # add digits
    add_digits(word,dic)
    
    #remove digits
    number_deletion(word,dic)


###################################################
############   Character Insertion   ##############
###################################################

def vowel_character_insertion(word,dic,lenght_of_strings):
    words_list = []
    i = 0
    newWord = ""
    while (i < len(word)):
        
        if word[i] in vowel: #and word[i] != word[i+1]:
            newWord = word[0:i] + word[i] + word[i:]
            words_list.append(newWord)
           
            while True: # get all the possible vowel insertions until the limit (e.g. baaarackobama, baaaarackobama, baaaaarack)
                if (int(len(newWord.replace('\n',''))) < lenght_of_strings):
                    newWord = newWord[0:i] + newWord[i] + newWord[i:]
                    words_list.append(newWord)
                else:
                    break
        i += 1
   
   # all vowels doubled
    i = 0
    newWord = ""
    while (i < len(word)):
        if word[i] in vowel and word[i] != word[i+1]:
            newWord += word[i] + word[i]
        elif word[i] in vowel and word[i] == word[i+1]:
            newWord += word[i] + word[i]
            i += 1
        else:
            newWord += word[i]
        i += 1
    words_list.append(newWord)

    for i in words_list:
        vowel_character_substitution(i,dic)
        common_misspelling_mistakes_substition(i,dic)
        punctuation_addition(i,dic)
        punctuation_deletion(i,dic)

    for i in words_list:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] += 1

    

def double_character_insertion(word,dic):
    words_list = []

    for i in range(0,len(word)):
        if (i+1) < len(word):  # i + 2 
            if word[i] == word[i+1]:
                if word[i] == word[i-1]:
                    continue
                if word[i] not in vowel:
                    newWord = word[0:i] + word[i] + word[i] + word[i+1:]
                    words_list.append(newWord)
             #   print(newWord)


    newWord = "" #the last case all the double characters must be deleted
    

    for i in range(0,len(word)):

        if (i+1) < len(word):  # i + 2 

            if word[i] == word[i+1]:
                if word[i] == word[i-1]:
                    continue
                if word[i] not in vowel:
                    newWord += word[i] + word[i] 
            else:
                if word[i] not in vowel:
                    newWord += word[i]
              #  words_list.append(newWord)
        else:
            newWord += word[i]
    
    #from Jimmyfallon to Jimmmyfalllon
    helping_word = ''
    for i in range(0,len(word)):
        if (i+1) < len(word):  # i + 2 
            temp =  word[i] + word[i+1]
            helping_word += word[i]
            if temp in double_characters:
              #  print('Double :', temp)
                helping_word += word[i]
        else:
            helping_word += word[i]
    newWord = helping_word

    words_list.append(newWord)


    for i in words_list:
        vowel_character_substitution(i,dic)
        common_misspelling_mistakes_substition(i,dic)
        punctuation_addition(i,dic)
        punctuation_deletion(i,dic)
        number_deletion(i,dic)
    for i in words_list:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] += 1



###################################################
############   Character Deletion   ###############
###################################################

def vowel_character_deletion(word,dic):
    words_list = []
    
    for i in range(len(word)):
        if word[i] in vowel:
            newWord = word[0:i] + word[i+1:]
            if newWord not in words_list:
                words_list.append(newWord)

    newWord = "" 
   # the last case all the vowels must be deleted
    for i in range(len(word)):
        if word[i] in vowel:
            None
        else:
            newWord += word[i]
 
    if newWord not in words_list and newWord != word:
        words_list.append(newWord)

    for i in words_list:
        vowel_character_substitution(i,dic)
        common_misspelling_mistakes_substition(i,dic)
        punctuation_addition(i,dic)
        number_deletion(i,dic)
        punctuation_deletion(i,dic)

    for i in words_list:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] += 1

def double_character_deletion(word,dic):
    words_list = []
    
    counter = 0 #checks if there is only one double character to remove duplicates
    for i in range(0,len(word)):
        if (i+1) < len(word):  # i + 2 
            if word[i] == word[i+1]:
                newWord = word[0:i]  + word[i+2:]
                words_list.append(newWord)
                counter +=1
              #  print(newWord)

    newWord = "" #the last case all the double characters must be deleted
    
    if counter == 0: # Ellen must be Een only one time in txt
        i = 0
        while i < len(word):
            if (i+1) < len(word):
                if i==0:
                    if (word[i] == word[i+1]):
                        None # do not delete this
                    else:
                        newWord += word[i]
                else:
                    if (word[i] == word[i+1]) or (word[i] == word[i-1]):
                        None # do not delete this
                    else:
                        newWord += word[i]
            else:
                if word[i] != word[i-1]:
                    newWord += word[i]
            i +=1


        if newWord != word and newWord not in words_list:
            words_list.append(newWord)


    #from Jimmyfallon to Jiyfaon
    helping_word = ''
    helping_boolean = False # for checking whether we are currently working with a double character
    for i in range(0,len(word)):
        if (i+1) < len(word):  # i + 2 
            temp =  word[i] + word[i+1]


            if helping_boolean == True: #checks if we have read a double character
                helping_boolean = False
                continue
            if temp in double_characters:
                helping_boolean = True # enable the double character check

            else:
                helping_word += word[i]
                helping_boolean = False

        else:
            if word[i-1] != word[i]:
                helping_word += word[i]
    newWord = helping_word

    words_list.append(newWord)

    # delete this to see changes!!
    for i in words_list:
        vowel_character_substitution(i,dic)
        common_misspelling_mistakes_substition(i,dic)
        punctuation_addition(i,dic)
        number_deletion(i,dic)
        punctuation_deletion(i,dic)
        
    for i in words_list:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] += 1

def punctuation_deletion(word,dic):
    if '_' in word:
        words_list = []
        for i in range(0,len(word)):
            if word[i] == "_":
                newWord = word[0:i] + word[i+1:]

                words_list.append(newWord)

        #delete all punctuations
        newWord = ""
        for i in range(0,len(word)):
            if word[i] != "-":
                newWord += word[i]

        if newWord not in words_list and newWord != word:
            words_list.append(newWord)

        for i in words_list:
            if i not in dic:
                dic[i] = 0
            else:
                dic[i] += 1


###################################################
############   Character Substitution   ###########
###################################################    

def vowel_character_substitution(word,dic):
    words_list = []

    for i in range(0,len(word)):
        if word[i] in vowel:
            for letter in vowel:
                if letter != word[i]:
                    newWord = word[0:i] + letter + word[i+1:]
                   # print (newWord)
                    words_list.append(newWord)
   
   # the case that all vowels will change was not implemented

    for i in words_list:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] += 1

def common_misspelling_mistakes_substition(word,dic):
    words_list = []
    for i in range(0,len(word)):
        for key in common_letter_replace_dic.keys():
            word = word.lower()
            if word[i] == key:
                
                values = common_letter_replace_dic.get(key)
                if ',' in values:

                    value = values.split(',')
                    for val in value:
                        newWord = word[0:i] + val + word[i+1:]

                        words_list.append(newWord)


                else:
                    newWord = word[0:i] + values + word[i+1:]

                    words_list.append(newWord)


    #The case that all the letters change has not been implemented
            if word[i] == word[i-1] == key:   
                values = common_letter_replace_dic.get(key)
                newWord = word[0:i-1] + values + values + word[i+1:]
                if newWord not in words_list:
                    words_list.append(newWord)
    
    for i in words_list:
        i = i + '\n'
        vowel_character_insertion(i,dic)
        vowel_character_substitution(i,dic)
        punctuation_addition(i,dic)
        punctuation_deletion(i,dic)

    for i in words_list:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] += 1


###################################################
###############  Number deletion   ################
################################################### 

def number_deletion(word,dic):

    position_of_numbers = []
    
    words_list = []
    
    for character in range(0, len(word)):
        if word[character] in numbers:
            newWord = word[0:character] + word[character + 1: ]
         #   tempWord = newWord
            position_of_numbers
            words_list.append(newWord)
            tempWord = newWord
            tempWord = tempWord[0:character] + tempWord[character + 1: ]
            words_list.append(tempWord)       
        
    
    newWord = ''.join([i for i in word if not i.isdigit()])
    words_list.append(newWord)
    
    
    ##helping code
    word_into_characters = []
    for i in range(0,len(word)):
        word_into_characters.append(word[i].strip())

    # for covering aekara9
    newWord = ''  
    for i in range(0,len(word)):
        if word_into_characters[i].isdigit():
            word_into_characters[i] = ''
          #  print(word_into_characters)
            for i in range(0,len(word)):
                newWord += word_into_characters[i].strip()
          #  print(newWord)
            words_list.append(newWord)
            newWord = ''

    ##helping code
    word_into_characters = []
    word = word[::-1] # reversing the string
    for i in range(0,len(word)):
        word_into_characters.append(word[i].strip())

    # for covering aekara1
    newWord = ''  
    for i in range(0,len(word)):
        if word_into_characters[i].isdigit():
            word_into_characters[i] = ''
            #print(word_into_characters)
            for i in range(0,len(word)):
                newWord += word_into_characters[i].strip()
            #print(newWord[::-1])
            words_list.append(newWord)
            newWord = ''
    
    # delete this to see changes!!
    for i in words_list:
    #  vowel_character_insertion(i,dic)
        vowel_character_substitution(i,dic)
        punctuation_addition(i,dic)
        common_misspelling_mistakes_substition(i,dic)
        punctuation_deletion(i,dic)
    #    double_character_deletion(i,dic)
        
    #######
    
    for i in words_list:
        if i not in dic:
           dic[i] = 0
        else:
           dic[i] += 1



###################################################
###############  String expansion  ################
################################################### 

def add_digits(word,dic):
    words_list = []
    for i in digits:
        l_word = word.replace('\n', '')
        r_word = str(i).replace('\n','')
        newWord = ''.join([l_word,r_word]) + '\n'
        words_list.append(newWord)
        newWord = ''.join([r_word,l_word]) + '\n'
        words_list.append(newWord)
        
    for i in words_list:
        if i not in dic:
           dic[i] = 0
        else:
           dic[i] += 1

def punctuation_addition(word,dic):
    #add punctuation in the front and in the end of the word
    # the space ' ' is not covered because it is useless (especially for usernames)
    words_list = []

    if (len(word.replace('\n','')) < 16):
        newWord = ''.join([word.rstrip(),'_']) + '\n'
        words_list.append(newWord)
        while True:
            if (len(newWord.replace('\n','')) < 16):
                newWord = ''.join([newWord.rstrip(),'_']) + '\n'
                words_list.append(newWord)
            else:
                break
        word  = word.replace('@','') # remove the @ from front
        newWord = ''.join(['_',word.rstrip()]) + '\n'
        words_list.append(newWord)
        while True:
            if (len(newWord.replace('\n','')) < 16):
                newWord = ''.join(['_',newWord.rstrip()]) + '\n'
                words_list.append(newWord)
            else:
                break
    
    for i in words_list:
        punctuation_deletion(i,dic)

    for i in words_list:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] +=1

###################################################
###############  Check_Duplicates  ################
################################################### 

def check_for_duplicates(name):
    print ("\n### Checking for actual duplicates inside the file ###")
    try:
        counter = 0
        f = open('content/@' + name.strip() + '/' + 'generated_usernames.txt', 'r', encoding = 'utf-8')
        Lines = f.readlines()
        f.close()
        for i in range(len(Lines)-1):
            for j in range(len(Lines)-1):
                if Lines[i] == Lines[j] and i !=j :
                    print (Lines[i])
                    counter +=1        
        print ("Dublicates for Usernames are : " + str(counter))
    except Exception:
        print(traceback.print_exc())
        print ("Something went wrong in reading a file")


if __name__ == "__main__":
    main()