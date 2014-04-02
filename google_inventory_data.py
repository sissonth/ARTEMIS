
import gspread

class ItemData():
    item_id='idnumber'
    name='name'
    description='description'
    courses='courses'
    inventory='inventory'
    cost=6.00
    in_cart=[]


def import_vending_items():
    vending_inventory=[]
    # Login with your Google account
    gc = gspread.login("meam.artemis@gmail.com","artemis1234")
    # Open a worksheet from spreadsheet with one shot
    inventoryWKS = gc.open("VendmoGM").sheet1
    inventory=inventoryWKS.get_all_values()
    for row in inventory:
        if row != inventory[0]:
            item=ItemData()
            item.item_id=row[0]
            item.name=row[0]
            item.inventory=row[1]
            item.cost=float(row[2])
            item.description=row[3]
            
            vending_inventory.append(item)
            
    return vending_inventory
    

