#Lindsay Dickson


file_n="crime_in_vancouver.csv"

file_nj="crime_codes.json"
 
#TYPE YEAR MONTH DAY HOUR MINUTE BLOCK NEIGHBOURHOOD X Y

# returns a 2D list containing the statistics in that file
def read_stats(filename):
    filein=open(filename, "r")
    
    l=filein.readline().strip()
    lists=filein.readlines()

    result = []
    for item in lists:
        data = item.split(',')
       
        type = data[0].strip()
        year = data[1].strip()
        month = data[2].strip()     #could probably make more effiecent                                  
        day = data[3].strip()       #using for loop? 
        hour = data[4].strip()
        minute = data[5].strip()
        block = data[6].strip()
        neighbourhood = data[7].strip()
        x = data[8].strip()
        y = data[9].strip()
        
        result.append([type, year, month, day, hour, minute, block, neighbourhood, x, y])
   
    return result
      
stats_database = read_stats(file_n)
#________________________________________________________________________

#takes a json filename as an argument and returns a dictionary containing the statistics in that file.
def read_codes(filename):
    filein=open(filename,"r")
    
    string=filein.readline()   
    
    string=string.strip('{}')
    list= string.split(',')
    
    result = []
    for item in list:
        data = item.split(':')
        key = data[0].strip('" ')
        value = data[1].strip('" ')
        result.append([key, value])
    
    dictt={}
    
    for item in result:
        key=int(item[0])
        value=item[1]
        dictt[key]=value
    
    return dictt
   
dict_c = read_codes(file_nj)

#__________________________________________________________________________

# takes an integer value code and a dictionary dict containing the statistics in the crime codes as arguments
#This function returns a list of all the crimes with the given code that have occurred in the database
def crimes_by_code(code,dict):
    
    crimes_by_cod=[]
    for i in range(len(stats_database)):

        if stats_database[i][0]==dict[code]:
            stat=stats_database[i]
            crimes_by_cod.append(stat)
            
    return crimes_by_cod
    


#crimes_by_code(110,dict_c)



#________________________________________________________________________

#to sort in descending order - 
def sort_alg(list2Sort):
    
    listSort=list2Sort[:]
    new_list = []

    while listSort:
        max = listSort[0]  
        for x in listSort: 
            if x > max:
                max = x
        new_list.append(max)
        listSort.remove(max)    

    return new_list

#
# takes a 2D list of stats as argument andreturns it sorted in descending order by the YEAR column
def sort_by_years(stats): #sorted w bubble sort
    new_list=stats[:]
    l = len(stats) 
    for i in range(0, l): 
        for j in range(0, l-i-1): 
            if (new_list[j][1] < new_list[j + 1][1]): 
                n = new_list[j] 
                new_list[j]= new_list[j + 1] 
                new_list[j + 1]= n 
    

    return new_list 
  

#sort_by_years(stats_database)

#________________________________________________________________________


# returns the 2D list of crime stats containing the
#crime type, year, month, day, and neighbourhood of all crimes reported between the start value and the end value of the {YEAR/MONTH/DAY}

def filter_crime_stats(stats,param,x,y):
    found_entries=[]
    #____ Evaluating param ____
    if param.lower() == "year":
        for i in range(len(stats)):

            if int(stats[i][1])>=x and int(stats[i][1])<=y:
                stat=stats[i]
                found_entries.append(stat)      
        
    elif param.lower() == "month": 
         for i in range(len(stats)):

            if int(stats[i][2])>=x and int(stats[i][2])<=y:
                stat=stats[i]
                found_entries.append(stat)      
    elif param.lower() == "day":
        for i in range(len(stats)):

            if int(stats[i][3])>=x and int(stats[i][3])<=y:
                stat=stats[i]
                found_entries.append(stat)     
    else:
        return "Invalid parameter"
   
    return found_entries
    

#IF USER INPUT REQUIRED 
# parameter=input("Enter a parameter: ") 
# x=int(input("Enter an starting value(x): "))
# y=int(input("Enter an end value(y): "))   



#filter_crime_stats(stats_database,parameter,x,y)


#________________________________________________________________________


#returns a list of all the crime codes that include all the keywords in their description/type
#if code not found: return empty list 
def code_from_keywords(keywords,dict):
    codes=[]
    for key in dict:
        #print(dict[key])
        for i in range(len(keywords)):
           if keywords[i].capitalize() in dict[key]:
                m=keywords[i].capitalize()
            # v=str.find()
            # if v>=0:
                codes.append(key)
                

    return codes



#keyword_list=['break','homicide']

#code_from_keywords(keyword_list,dict_c)





#________________________________________________________________________

#returns a list of crimes that occurred within 1000 points around a given search location (x, y). 
# The function should first provide the users with the information of the minimum and maximum values
#for both X and Y- coordinates of all crimes reported in the 2-D list. Then it should ask the user for the x and y values of the search location 
def crime_by_location(stats):
    # x=500000
    # y=5200000
   #____ x parameters_________
    x_list=[]
    for i in range(len(stats)):
        x_range=stats[i][8]
        x_list.append(x_range)
    
   # print(x_list)
    x_max_list=sort_alg(x_list)
    max_x=x_max_list[0]
    max_len=len(x_max_list)
    min_x=x_max_list[max_len-1]
    
    #____ y parameters ____
    y_list=[]
    for i in range(len(stats)):
        y_range=stats[i][9]
        y_list.append(y_range)
        
    y_max_list=sort_alg(y_list)
    max_y=y_max_list[0]
    max_len=len(y_max_list)
    min_y=y_max_list[max_len-1]
    
    #print("min x value: {}".format(min_x))
    #print("max x value: {}".format(max_x))
    #print("min y value: {}".format(min_y))
    #print("max y value: {}".format(max_y))
    
    #IF USER INPUT IS REQUIRED
    x=int(input("Enter an x coordinate between {} and {}: ".format(min_x,max_x)))
    y=int(input("Enter an y coordinate between {} and {}: ".format(min_y,max_y)))
    #____ searching by parameters ____
    min_xi=x-1000
    max_xi=x+1000
    min_yi=y-1000
    max_yi=y+1000
    foundd=[]   
    for i in range(len(stats)):

        if (int(stats[i][8])>=int(min_xi) and int(stats[i][8])<=int(max_xi)) and (int(stats[i][9])>=int(min_yi) and int(stats[i][9])<=int(max_yi)):
            stat=stats[i]
            foundd.append(stat)        

        
    return foundd


#crime_by_location(stats_database)

#________________________________________________________________________


#returns another dictionary having the following structure:
#{code: [frequency, type]}
def code_and_freq(stats,dict):
    dic={}
    lengths=[]
    for key in dict:
        
        c_key=key
        t_crimes=crimes_by_code(key,dict)
        freq_v=len(t_crimes)
        crime=dict[key]
        dic[c_key]= freq_v, crime
    
    return dic
    
#code_and_freq(stats_database, dict_c)




