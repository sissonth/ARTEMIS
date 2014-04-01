#!/usr/bin/python

import csv

class UserData():
    PennID='pennID'
    name='name'
    purchase_history='purchase_history'
    accounts=[]
    
def import_user_data(penn_id):
    with open('user_database.csv','rb') as f:
        reader = csv.reader(f,delimiter='\t')
        title_row=True
        for row in reader:
            #print row
            if title_row==True:
                possible_accounts= row[2::]
                title_row=False
                #print possible_accounts
            if row[0]==str(penn_id):
                person=UserData()
                person.name=row[1]
                person.PennID=penn_id
                class_array=row[2::]
                
                accounts_list=[]
                for x in xrange(len(possible_accounts)):                
                    if class_array[x]=='1':
                        accounts_list.append(possible_accounts[x])

                person.accounts=accounts_list
                print 'user found'
                break
            else:
                person='not found'
    return person
    