""" utilities.py  -- Batch routines to help sort and manage the naphthabase.
"""

import naphthabase as nb

def check_haulage_charges():
    """Checks that a handling charge has been added to cost of every purchase.
    
    Compares the price set in stock with the purchase price to make sure that
    45 pounds handling charge has been added to the cost.
    
    The rule is that 45 pounds per tonne is added, or just 45 pounds if the
    quantity is under a tonne.
    """
    
    # Search through Stock
    stock = nb.Stock()
    purchases = nb.Purchases()
    # We're only interested in stock that isn't empty
    instock = filterdata(stock._data, stock._clmn['BatchStatus'], 'E')
    for entry in instock:
        pon = entry[stock._clmn['PONumber']]
        stock_price = entry[stock._clmn['PurchaseCost']]
        purchase_price = purchases.getdict(pon)[purchases._clmn['Price']]
        purchased_quantity = purchases.getdict(pon)[purchases._clmn['Quantity']]
        #convert strings to prince per tonne in pounds
        stock_price = per_tonne_price(stock_price)
        purchase_price = per_tonne_price(purchase_price)
        if stock_price - purchase_price < 45:
            print pon
         
    

def filterdata(dataset, column, criteria):
    """Returns a dataset with all records matching the criteria removed"""
    
    output = []
    for item in dataset:
        if item[column] != criteria:
            output.append(item)
    return output
    
def per_tonne_price(price_as_string):
    """Returns an int representing a price per tonne.
    
    Assumes that price will be to nearest kilo
    """
   
    pounds, pence = price_as_string.split('.')
   
    if pence[3] == '0':
        pence = pence[:3]
        #strip off sub-pence
    else:
        print "found a price that isn't to the nearest kilo"
    price = int(pounds+pence)
    return price
    
    