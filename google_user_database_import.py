#!/usr/bin/python

import gspread
import numpy as np

class UserData():
    PennID='pennID'
    name='name'
    purchase_history='purchase_history'
    accounts=[]
    account_part_quotas=[]
    
    
def import_user_data(penn_id,penncard_output_name):
    # Login with your Google account
    gc = gspread.login("meam.artemis@gmail.com","artemis1234")
    # Open a worksheet from spreadsheet with one shot
    sh=gc.open("VendmoGM")
    user_wks=sh.worksheet('Users')
    user_list=user_wks.get_all_values()
    
    first_row=user_list[0]
    possible_accounts=first_row[2::]
    
    person=[]    
    
    for row in user_list:
        if row[1] == str(penn_id):
            person=UserData()
            person.name=row[0]
            person.PennID=penn_id
            
            accounts_access=row[2::]
            account_array=[]
            
            i=0
            for x in accounts_access:
                if x == 'Yes':
                    account_array.append(possible_accounts[i])
                i=i+1
                    
            
            person.accounts=account_array
            
            
            account_quotas_wks=sh.worksheet('Account Quotas')
            account_quotas=account_quotas_wks.get_all_values()
            person.account_part_quotas=account_quotas
    
            
            
            print 'user found'
            break
    ########### ADD USERS NOT IN DATABASE FOR DEMO PURPOSES ############
        
    if person == []:
        person=UserData()
        person.PennID=penn_id
        person.accounts=[possible_accounts[0],possible_accounts[2],possible_accounts[3]]
        person.name=penncard_output_name        
        
        
        account_quotas_wks=sh.worksheet('Account Quotas')
        account_quotas=account_quotas_wks.get_all_values()
        person.account_part_quotas=account_quotas
        
        user_wks.append_row([person.name,person.PennID,'Yes','','Yes','Yes'])
        
        print 'user given default access'
        
#    ## now retrieve quota data ##        
#    quota_wks=sh.worksheet('Account Quotas')
#    m=quota_wks.find(account)
#    quotas=quota_wks.row_values(m.row)
#    
#    t=quota_wks.row_values(1)
    
    
    
    ################ retrieve person's transaction history #############3
    transactions_wks=sh.worksheet('Transaction History')
    penn_ids=transactions_wks.col_values(4)
    items=transactions_wks.col_values(5)
    accounts=transactions_wks.col_values(6)      
    
    
    item_history=[]
    accounts_history=[]
    
    count=0
    
    for row in penn_ids:
        if row==penn_id:
            item_history.append(items[count])
            accounts_history.append(accounts[count])
        count=count+1


    from collections import Counter

    account_transaction_dict={}
    
    for row in person.accounts:
        count2=0
        this_acct_item_history=[]        
        for v in accounts_history:        
            if v==row:
                this_acct_item_history.append(item_history[count2])
            count2=count2+1


        account_transaction_dict[row]=Counter(this_acct_item_history)

        
    print account_transaction_dict

    
    
    person.purchase_history=account_transaction_dict 
    
    
    
    
    
    
    
    
    
    
    ######## retrieve master list of quotas ##################
    quota_wks=sh.worksheet('Account Quotas')
    quota_matrix=np.matrix(quota_wks.get_all_values())
    
    
    
    
    
    
    return person, quota_matrix
            

def retrieve_account_quotas(account):
    # Login with your Google account
    gc = gspread.login("meam.artemis@gmail.com","artemis1234")
    # Open a worksheet from spreadsheet with one shot
    sh=gc.open("VendmoGM")
    
    quota_wks=sh.worksheet('Account Quotas')
    m=quota_wks.find(account)
    quotas=quota_wks.row_values(m.row)
    
    t=quota_wks.row_values(1)
    
    return t, quotas

def retrieve_account_quotas_from_matrix(quota_matrix,account):
    item_row=quota_matrix[0].tolist()
    t=item_row[0]
    
    d=quota_matrix.tolist()
    
    for row in d:
        if row[0]==account:
            quotas=row
        
    return t, quotas
        

def retrieve_transaction_history(penn_card_number):
    # Login with your Google account
    gc = gspread.login("meam.artemis@gmail.com","artemis1234")
    # Open a worksheet from spreadsheet with one shot
    sh=gc.open("VendmoGM")
    
    transactions_wks=sh.worksheet('Transaction History')
    penn_ids=transactions_wks.col_values(4)
    items=transactions_wks.col_values(5)
    accounts=transactions_wks.col_values(6)    
    
    
    item_history=[]
    accounts_history=[]
    
    count=0
    
    for row in penn_ids:
        if row==penn_card_number:
            item_history.append(items[count])
            accounts_history.append(accounts[count])
        count=count+1

    from collections import Counter

    account_transaction_dict={}
    
    for row in person.accounts:
        count2=0        
        for v in accounts_history:        
            if v==row:
                this_acct_item_history.append(item_history[count2])
            count2=count2+1
        account_transaction_dict[row:Counter(this_acct_item_history)]
        
    print account_transaction_dict
            
            ##################### STILL WORKING ON THIS
        
        
        
    c=Counter(item_history)
    

    return c
  
#def import_user_data(penn_id):
#    with open('user_database.csv','rb') as f:
#        reader = csv.reader(f,delimiter='\t')
#        title_row=True
#        for row in reader:
#            #print row
#            if title_row==True:
#                possible_accounts= row[2::]
#                title_row=False
#                #print possible_accounts
#            if row[0]==str(penn_id):
#                person=UserData()
#                person.name=row[1]
#                person.PennID=penn_id
#                class_array=row[2::]
#                
#                accounts_list=[]
#                for x in xrange(len(possible_accounts)):                
#                    if class_array[x]=='1':
#                        accounts_list.append(possible_accounts[x])
#
#                person.accounts=accounts_list
#                print 'user found'
#                break
#            else:
#                person='not found'
#    return person
#    
#def import_vending_items():
#    vending_inventory=[]
#    # Login with your Google account
#    gc = gspread.login("meam.artemis@gmail.com","artemis1234")
#    # Open a worksheet from spreadsheet with one shot
#    inventoryWKS = gc.open("VendmoGM").sheet1
#    inventory=inventoryWKS.get_all_values()
#    for row in inventory:
#        if row != inventory[0]:
#            item=ItemData()
#            item.item_id=row[0]
#            item.name=row[0]
#            item.inventory=row[1]
#            item.cost=float(row[2])
#            item.description=row[3]
#            
#            vending_inventory.append(item)
#            
#    return vending_inventory