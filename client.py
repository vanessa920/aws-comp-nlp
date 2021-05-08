from datetime import datetime

defaultLogics = {
    'hasDollar':None,
    'hasItem':None,
    'hasSection':None,
    
}

def userInput():
    keywords = []
    keyword = ''
    while(keyword != 'NEXT'):
        keyword = input('please enter the keyword (type NEXT to move on): ')
        
        if keyword == 'NEXT':
            continue
        # some validation here
        elif False:
            pass
        else:
            keywords.append(keyword)
            
    date = []
    while(date == []):
        entries = []
        entries.append(input('please enter the start date (yyyy-mm-dd):'))
        entries.append(input('please enter the end date (yyyy-mm-dd):'))
        try:
            for e in entries:
                date.append(datetime.strptime(date,'%Y-%m-%d'))
        except:
            date = []
            print('Invalidate date format. Please try again.')
    
    user_logics = {}
    for k,c in defaultLogics.items():
        tempholder = input(f'Do you need a {k} value (True/False):')
        
        if tempholder =='True':
            logic = True
        else:
            logic = False
        
        user_logics[k] = logic
    
    return keywords, date, user_logics

def userSearch(keywords,date = datetime.today(),logics = defaultLogics):
    pass
    #time
    
if __name__ == '__main__':
    print(userInput())