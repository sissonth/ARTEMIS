#!/usr/bin/python

################# CONFIGURE INPUTS ############################

import usb.core
#search for device
if usb.core.find(idVendor=0x0408, idProduct=0x3025) != None:
    from kivy.config import Config
    Config.set('input','mouse','')


##############################################################



from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.logger import Logger
from kivy.uix.layout import Layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

import time

import signal_stuff

#from inventory import ItemData
#from inventory import import_vending_items

from google_inventory_data import ItemData
from google_inventory_data import import_vending_items
from google_inventory_data import record_transaction


from google_user_database_import import import_user_data
from google_user_database_import import retrieve_account_quotas


#from user_database_import import import_user_data

from card_reader import initialize_cardReader
from card_reader import retrieve_data

import numpy as np

global vending_inventory
global cart_items
global cart_need_update
global current_user
global current_user_needs_updating
global selected_account
global update_widgets_flag
global quota_items
global quotas
global loggout_trigger

update_widgets_flag=False

current_user_needs_updating = False
current_user=[]
quota_items=[]
selected_account=[]


loggout_trigger=False
#class ItemData():
#    item_id='idnumber'
#    name='name'
#    description='description'
#    courses='courses'
#    inventory='inventory'
#    cost=5.00
#    in_cart=[]

#item1=ItemData()
#item2=ItemData()
#item3=ItemData()

#item1.name='hahahha'
#item2.courses='MEAM 247'

#vending_inventory=[item1,item2,item3]

#vending_inventory=import_vending_items('inventory_items.csv')

cart_items = []
cart_need_update=False



############################ VENDING ##############################

class VendingInventoryItem(BoxLayout):    
    global cart_items
    
    def __init__(self,**kwargs):
        super(VendingInventoryItem,self).__init__(**kwargs)
        
    def load_item_info(self,item):
        self.ids.item_name_label.text=item.name
        self.ids.item_description_label.text=item.description
        self.ids.course_numbers_label.text=item.courses
        #self.idnumber=item.item_id
        self.idnumber=item
        
    def add_one_to_cart(self,x):
        global cart_items
        global cart_need_update
        x=int(x)
        x=x+1
        self.idnumber.in_cart=x
        x=str(x)
        self.ids.number_in_cart.text=x
        if cart_items.count(self.idnumber) == 0:
            cart_items.append(self.idnumber)
        
        cart_need_update=True

              
    def remove_one_from_cart(self,x):
        global cart_items
        global cart_need_update
        x=int(x)
        if x>0: 
            x=x-1
            self.idnumber.in_cart=x
            x=str(x)
            self.ids.number_in_cart.text=x
            if self.idnumber.in_cart==0:            
                cart_items.remove(self.idnumber)
            cart_need_update=True

    def select_item(self,x):
        global cart_items
        global cart_need_update
        global current_user
        if current_user==[] or quota_items==[]:
            login_first_error=ErrorPopup()
            login_first_error.open()
        else:
            #self.idnumber.in_cart=x
            cart_items=[self.idnumber]
            cart_need_update=True


class VendingInventoryList(GridLayout):
    def __init__(self,**kwargs):
        super(VendingInventoryList,self).__init__(**kwargs)
    
    def generate_inventory_list(self):
        global vending_inventory
        self.clear_widgets()
        #vending_inventory=import_vending_items('inventory_items.csv')
        vending_inventory=import_vending_items()
        for x in xrange(len(vending_inventory)):       
            item_data=vending_inventory[x]
            item=VendingInventoryItem()
            item.load_item_info(item_data)
            self.add_widget(item)
        
    def regenerate_list(self):
        self.clear_widgets()
        self.generate_inventory_list()
        
        
        
        
#################### CHECKOUT AREA #######################################        
class CheckoutItem(BoxLayout):
    global current_user
    global quotas
    global quota_items
    
    def __init__(self,**kwargs):
        super(CheckoutItem,self).__init__(**kwargs)
    
    def load_data(self,item_data):
        global current_user
        global quotas
        global quota_items
        
        self.idnumber=item_data
        #self.ids.number_in_cart.text=str(self.idnumber.in_cart)
        self.ids.item_name.text=self.idnumber.name
        self.ids.item_cost.text='$'+str(self.idnumber.cost)
        self.ids.item_inventory.text=str(self.idnumber.inventory)
        ### add retreiving quota code hereu
        ind=quota_items.index(self.idnumber.name)
        
        self.idnumber.quota=quotas[ind]
        self.ids.quota.text=self.idnumber.quota
        
#        self.ids.quota.text=current_user.
        #self.ids.item_total.text=' $ ' + str((self.idnumber.in_cart)*(self.idnumber.cost))
        
    def update_count(self):
        self.ids.number_in_cart.text=self.idnumber.in_cart



class CheckoutConfirmationItem(BoxLayout):
    def __init__(self,**kwargs):
        super(CheckoutConfirmationItem,self).__init__(**kwargs)
    
    def load_data(self,item_data):
        self.idnumber=item_data
        #self.ids.number_in_cart.text=str(self.idnumber.in_cart)
        self.ids.item_name.text=self.idnumber.name
        self.ids.item_cost.text='$'+str(self.idnumber.cost)
        #self.ids.item_total.text=' $ ' + str((self.idnumber.in_cart)*(self.idnumber.cost))
        
    def update_count(self):
        self.ids.number_in_cart.text=self.idnumber.in_cart


class CheckoutList(GridLayout):
    global cart_items
    def __init__(self,**kwargs):
        super(CheckoutList,self).__init__(**kwargs)
        
    def update_list(self):
        global cart_items
        self.clear_widgets()
        #print cart_items
        if len(cart_items) != 0:
            #print len(cart_items)
            for x in xrange(len(cart_items)):
                item1=CheckoutItem()
                item1.load_data(cart_items[x])
                self.add_widget(item1)
                #print 'ADDING WIDGET'

    def update_confirmation_list(self):
        global cart_items
        self.clear_widgets()
        #print cart_items
        if len(cart_items) != 0:
            #print len(cart_items)
            for x in xrange(len(cart_items)):
                item1=CheckoutConfirmationItem()
                item1.load_data(cart_items[x])
                self.add_widget(item1)


            
        
#        if len(cart_items) == 0:
#            self.clear_widgets()
#        else:
#            update_complete=False
#            s=0
#            while update_complete==False:
#                number_of_widgets=len(self.children)
#                if self.children[s].idnumber.in_cart==0:
#                    self.remove_widget(self.children[s])
#                    s=0
#                else:
#                    s=s+1
#                    
#                end_number_of_widgets=len(self.children)
#                if s==end_number_of_widgets:
#                    update_complete=True
#                    
#            update_complete=False
#            s=0
#            while update_complete==False
#                
#                    
#        for x in xrange(len(self.children)):
#            self.children[x].update_count()
#            




class CheckoutWidget(BoxLayout):
    def __init__(self,**kwargs):
        super(CheckoutWidget,self).__init__(**kwargs)  
        #self.ids.penn_id_button.bind(on_release=self.request_card_swipe)
                       
        
    def update_account(self):
        global selected_account
        global quota_items
        global quotas
        global cart_need_update
        
        cart_need_update=True
        
        selected_account=self.ids.account_selection.text
        if selected_account!='Select Account':
            [quota_items,quotas]=retrieve_account_quotas(selected_account)
        self.test()
        
    def test(self):
        print 'ahahaha'
        
    def checkout(self,penn_id_number,account_selection):
        global current_user
        global selected_account
        global cart_items
#        anim=Animation(x=100,y=100)
#        anim.start(self)
        #root_window=self.get_root_window()
        
        if (current_user==[]) or (selected_account==[]) or cart_items==[]:
            login_first_error=ErrorPopup()
            login_first_error.open()
        else:
            confirmation=ConfirmationScreen()
            confirmation.load_cart(account_selection)
            confirmation.open()        
            #root_window.add_widget(popup)
            print 'Penn ID:', penn_id_number,' Account: ', account_selection
        
    def update_checkout(self,cart_items):
        #self.ids.total_cost.text='$'+str(total_cost)
        self.ids.checkout_list.update_list()
        pass

    def request_card_swipe(self,value):
        inputPopup=SwipePennCard()
        inputPopup.open()
        print 'PLEASE SWIPE PENNCARD TO LOGIN'

    def current_user_updated(self,current_user):
        self.ids.penn_id_button.text=current_user.name
        self.ids.account_selection.values=(current_user.accounts)
        self.ids.penn_id_button.bind(on_release=self.loggout)
        print 'updating current user'
        print current_user.accounts        
        
    def loggout(self,value):
        global current_user
        global selected_account
        global cart_items
        global quotas
        global quota_items
        
        selected_account=[]
        current_user=[]
        cart_items=[]
        quotas=[]
        quota_items=[]
        
        self.update_checkout(cart_items)
        self.ids.penn_id_button.text='Click Here to Login'
        self.ids.account_selection.values=()
        #self.ids.penn_id_button.bind(on_release=self.request_card_swipe)
        self.ids.penn_id_button.unbind(on_release=self.loggout)
        self.ids.account_selection.text='Select Account'
        print 'logging user out'   

class VendingInProcess(Popup):
    def __init__(self,**kwargs):
        super(VendingInProcess,self).__init__(**kwargs)
        Clock.schedule_interval(self.trigger_retract,.1)
        #Clock.schedule_once(self.trigger_update_all_widgets, 1)
        #self.trigger_update_all_widgets()

        
    def vend_command(self,did):
        global current_did
        current_did=did
        signal_stuff.dispense(current_did)
        
        
    def trigger_retract(self,dt):
        global current_did
        if signal_stuff.retrieve_status(current_did)==73:
            Clock.unschedule(self.trigger_retract)
            time.sleep(1)
            signal_stuff.retract(current_did)
            self.trigger_update_all_widgets()
    
    
    def update_databases_command(self):
        global cart_items
        global current_user        
        record_transaction(cart_items,current_user)

    
    def trigger_update_all_widgets(self):
        global update_widgets_flag
        global loggout_trigger        
        self.update_databases_command()
        update_widgets_flag=True
        loggout_trigger=True
        
        
class ConfirmationCheckoutList(GridLayout):
    def __init__(self,**kwargs):
        super(ConfirmationCheckoutList,self).__init__(**kwargs)
        
        
class SwipePennCard(Popup):
    global current_user
    
    def __init__(self,**kwargs):
        super(SwipePennCard,self).__init__(**kwargs)        
        initialize_cardReader()
        Clock.schedule_interval(self.update_user,1.5)
        
    def update_user(self,dt):
        global current_user
        global current_user_needs_updating
        print 'update user called'
        
        [penncard_output,penncard_output_name]=retrieve_data()
        if len(penncard_output)>0:
            current_user_needs_updating = True
            current_user=import_user_data(penncard_output,penncard_output_name)
            Clock.unschedule(self.update_user)
            #self.ids.cw.current_user_updated(current_user)
            self.dismiss()
            print penncard_output
            
    def dismiss_SwipePennCard(self):
        Clock.unschedule(self.update_user)
        self.dismiss()
        
        
class ConfirmationScreen(Popup):
    global cart_items
    def __init__(self,**kwargs):
        super(ConfirmationScreen,self).__init__(**kwargs)    

    def load_cart(self,account_selection):
        global cart_items
        global current_user
        cart=CheckoutList()
        cart.clear_widgets()
        cart.update_confirmation_list()
        self.ids.cart_list.add_widget(cart)
        self.ids.user_label.text=current_user.name
        self.ids.user_pennID.text=str(current_user.PennID)
        self.ids.account_label.text=account_selection
        
        total_cost=0
        total_cost=cart_items[0].cost
#        for x in xrange(len(cart_items)):
#            total_cost=total_cost+(cart_items[x].in_cart*(int(cart_items[x].cost)))
            
        self.ids.charge_total.text='$ ' + str(total_cost)
        #for x in xrange(len(cart_items)):
            #self.ids.cart_list.add_widget(Label(text=str(x)))

    def proceed_to_vend(self):
#        global cart_items
#        global current_user
        
        vendingPopup=VendingInProcess()
        self.dismiss()        
        vendingPopup.open()
        vendingPopup.vend_command(253)
        #record_transaction(cart_items,current_user)        
        
    def cancel_order(self):
        self.dismiss()



class ErrorPopup(Popup):
    def __init__(self,**kwargs):
        super(ErrorPopup,self).__init__(**kwargs)
        
    

############################### Root Widget ##############################
class MyWidget(TabbedPanel):
    global cart_items 
    global vending_inventory
    global cart_need_update
    global current_user
    
    def __init__(self,**kwargs):
        super(MyWidget,self).__init__(**kwargs)
#        item2_data=ItemData()
#        item2=VendingInventoryItem()
#        item2.load_item_info(item2_data)
#        self.ids.vil.add_widget(item2)
        self.ids.vil.generate_inventory_list()
        
        #self.ids.cw.update_checkout()
        Clock.schedule_interval(self.updateCheckout_list, .1)
        Clock.schedule_interval(self.update_user,.2)
        Clock.schedule_interval(self.update_inventory_widgets,.2)
                
    def update_user(self,dt):
        global current_user
        global current_user_needs_updating
        if current_user != [] and (current_user_needs_updating==True):
            self.ids.cw.current_user_updated(current_user)
            #self.ids.cw.loggout()
            current_user_needs_updating = False
            print 'user updated'
        #if current_user == [] and (current_user_needs_updating==True):
        #    self.ids.cw.loggout()
        #    current_user_needs_updating==False            
    
        global loggout_trigger
        if loggout_trigger==True:
            self.ids.cw.loggout(0)
            loggout_trigger=False
    
    
    def update_inventory_widgets(self,dt):
        global update_widgets_flag
        if update_widgets_flag == True:
            self.ids.vil.generate_inventory_list()
            update_widgets_flag = False
        
        
    def updateCheckout_list(self,dt):
        global cart_items
        global vending_inventory
        global cart_need_update
        if cart_need_update == True:
            total_cost=0
            #total_cost=(cart_items[0].in_cart*cart_items.cost)
            #for x in xrange(len(cart_items)):
            #    total_cost=total_cost+(cart_items[x].in_cart*cart_items[x].cost)
            self.ids.cw.update_checkout(cart_items)
            cart_need_update=False
            
                        
            
    def checkingOut(self):
        global cart_items
        print 'Checking Items OUT!! YAYAYAYA'
        
        
        # retreive number of parts selected
        #self.ids.vil.retreive_order()
        #self.ids.cw.update_checkout()
        #print(cart_items)
#    def on_touch_down(self,touch):
#        if touch.is_double_tap:
#            print('Touch is a double tap!')
#        else:
#            print('Touch was not a double tap!')
#            print(touch.id)
        

class artemisApp(App):
    App.title='ARTEMIS v1.0'
    
    def build(self):
        artemis=MyWidget()
        return artemis
        
                
    def on_start(self):
        Logger.info('App: ARTEMIS ALIVE')
        
    def on_stop(self):
        Logger.info('App: ARTEMIS STOPPED')
        
        
        
if __name__ == '__main__':
    artemisApp().run()
