import datetime
import decimal
import rrdb
from translate_table import *
from update import *

rrdata = rrdb.RandRDatabase()
nbdb = loadSession()
Base.metadata.create_all()

def get_customer_id(clientid):
    customer = nbdb.query(Customer).\
                    filter(Customer.\
                    customer_code == clientid).all()
    if len(customer) == 1:
        customerid = customer[0].id
    else:
        customerid = None
    return customerid

def get_supplier_id(clientid):
    supplier = nbdb.query(Supplier).\
                    filter(Supplier.supplier_code == clientid).all()
    if len(supplier) == 1:
        supplierid = supplier[0].id
    else:
        supplierid = None
    return supplierid

def get_carrier_id(WO_Num):
    carrier = nbdb.query(Carrier).\
                   filter(Carrier.won == WO_Num).all()
    if len(carrier) == 1:
        carrierid = carrier[0].id
    elif len(carrier) > 1:
        print 'ARRRRGHHH', carrier
        carrierid = carrier[0].id
    else:
        carrierid = None
    return carrierid
    
def get_purchaseorder_id(PO_Num):
    po = nbdb.query(PurchaseOrder).\
                    filter(PurchaseOrder.pon == PO_Num).all()
    if len(po) == 1:
        poid = po[0].id
    else:
        poid = None
    return poid

def get_purchaseitem_id(PO_Num, Batch):
    query = """
    Select Batch, \"Item Order\" AS ItemOrder from \"Formula Stock Usage\"
    where \"Record Type\" = 'P' or \"Record Type\" = ?
    """
    po_items = rrdata.simplequery(query, 'G')
    po_item_num = {}
    for item in po_items:
        if item.Batch == '15381':
            itemnum = None
        else:
            itemnum = item.ItemOrder
        po_item_num[item.Batch] = itemnum
        
    pi = nbdb.query(PurchaseItem).\
                    filter(PurchaseItem.pon == PO_Num).\
                    filter(PurchaseItem.itemno == po_item_num.get(Batch, None)).all()
    if len(pi) == 1:
        piid = pi[0].id
    else:
        piid = None
    return piid

def get_material_id(material):
    mat = nbdb.query(Material).\
                     filter(Material.code == material).all()
    if len(mat) == 1:
        matid = mat[0].id
    else:
        matid = None
    return matid

def get_salesorder_id(WO_Num):
    so = nbdb.query(SalesOrder).\
                    filter(SalesOrder.won == WO_Num).all()
    if len(so) == 1:
        soid = so[0].id
    else:
        soid = None
    return soid

def get_salesitem_id(WO_Num, material):
    mat = nbdb.query(Material).\
                     filter(Material.code == material).all()
    if len(mat) == 1:
        salesitem = nbdb.query(SalesItem).\
                               filter(SalesItem.won == WO_Num).\
                               filter(SalesItem.deleted == False).\
                               filter(SalesItem.material_id == mat[0].id).all()
        if len(salesitem) == 1:
            salesitemid = salesitem[0].id
        elif len(salesitem) > 1:
            print "UUURRRGGGHH!!", salesitem
        else:
            salesitemid = None
    else:
        salesitemid = None
    return salesitemid

def get_stock_id(Batch):
    stock = nbdb.query(Stock).\
                       filter(Stock.batch == Batch).all()
    if len(stock) == 1:
        stockid = stock[0].id
    else:
        stockid = None
    return stockid

def get_grade_id(Batch):
    stock = nbdb.query(Stock).\
                       filter(Stock.batch == Batch).all()
    if len(stock) == 1:
        gradeid = stock[0].grade_id
    else:
        gradeid = None
    return gradeid
            

def map_and_update(table_mapping):
    """Maps the R&R database to the NaphthaBase
    
    The table_mapping dictionary describes how the NaphthaBase columns
    are mapped to the R&R database columns.
    This function gets the latest data from the R&R database and updates
    the NaphthaBase.
    """
    
    nbtable = eval(table_mapping['nbtable'])
    # This is the specified NaphthaBase table object, eg Material, Customer, Supplier etc.
    last_nb_record = nbdb.query(nbtable).order_by(desc(nbtable.lastupdated)).first()
    if last_nb_record is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = last_nb_record.lastupdated
    # Finds the last updated record in the NaphthaBase and sets lastupdated variable to this date, or defaults to 1982.
    lastnb_records = set([i.rr_recordno for i in nbdb.query(nbtable).filter(nbtable.deleted == False)])
    # Creates a set of all Record Numbers in the Naphthabase table
    all_rr_data = rrdata.query(table_mapping['rrsql'], table_mapping['rrtable'])
    all_records = set([i.RecordNumber for i in all_rr_data])
    # Creates a set of all Record Numbers in the R&R database table
    newdata = rrdata.query(table_mapping['rrsql'], table_mapping['rrtable'], lastupdated)
    recentmods = set([i.RecordNumber for i in newdata])
    # Creates a set of all Record Numbers for entries in the R&R database table since the lastupdated date.
    
    new_records = recentmods.difference(lastnb_records)
    # Set of all new records in the R&R database table that aren't in the NaphthaBase table
    updated_records = recentmods.intersection(lastnb_records)
    # Set of records that exist in the NaphthaBase but need updating
    deletedrecords = lastnb_records.difference(all_records)
    # Set of records that have been deleted from the R&R database and need the deleted flag setting in the NaphthaBase
    
    map = table_mapping['Map']
    # This is the specific column mapping information.
    beginning = '%s(' % (table_mapping['nbtable'])
    args = []
    for column in map.keys():
        rrcolumn = map[column]
        if type(rrcolumn) is list:
            # All records in the list are combined into a single field before writing to the NaphthaBase
            start = '%s = combine(' % column
            middle = []
            for item in rrcolumn:
                middle.append('record.%s' % item)
                rrfield = start + ', '.join(middle) + ')'
            args.append(rrfield)
        elif type(rrcolumn) is dict:
            # The function specified in the dictionary needs to be executed to get the reference id.
            args.append('%s = %s' % (column, rrcolumn['func']))
        else:
            args.append('%s = record.%s' % (column, rrcolumn))
        
    args.append('deleted = False)')
    newinstruction = beginning + 'id = None, ' + ', '.join(args)
    updatedinstruction = ', '.join(args)
    print updatedinstruction + '\n\n'
    
    tablename = table_mapping['nbtable']
    args = ['%sHistory(id = None, %s_id = lastrecord.id' % (tablename, tablename.lower())]
    for column in map.keys():
        args.append('%s = lastrecord.%s' % (column, column))
    oldinstruction = ', '.join(args) + ')'
    print oldinstruction + '\n\n'
    
    global old
    global lastrecord
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            newmat = eval(newinstruction)
            newmat.lastupdated = record.LastUpdated
            nbdb.add(newmat)
        elif record.RecordNumber in updated_records:
            lastrecord = nbdb.query(nbtable).\
                                    filter(nbtable.rr_recordno == record.RecordNumber).all()[0]
            old = eval(oldinstruction)
                        
            old.lastupdated = lastrecord.lastupdated
            nbdb.add(old)
            
            #nbdb.delete(lastrecord)
            for column in map.keys():
                rrcolumn = map[column]
                print rrcolumn
                if type(rrcolumn) is list:
                    # All records in the list are combined into a single field before writing to the NaphthaBase
                    start = 'lastrecord.%s = combine(' % column
                    middle = []
                    for item in rrcolumn:
                        middle.append('record.%s' % item)
                        rrfield = start + ', '.join(middle) + ')'
                    lastrecord.__setattr__(column, eval(rrfield))
                elif type(rrcolumn) is dict:
                    # The function specified in the dictionary needs to be executed to get the reference id.
                    lastrecord.__setattr__(column, eval('record.%s' % rrcolumn['func']))
                else:
                    lastrecord.__setattr__(column, eval('record.%s' % rrcolumn))
                      
            lastrecord.lastupdated = record.LastUpdated
          
            lastrecord.history.append(old)
            #nbdb.add(newrecord)
    for record in deletedrecords:
        recordtodelete = nbdb.query(nbtable).filter(nbtable.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    
    


    
    

def sanitise(record):
    cont = container()
    columns = [item[0] for item in record.cursor_description]
    for column in columns:
        data = record.__getattribute__(column)
        if type(data) is decimal.Decimal:
            cont.__dict__[column] = str(data)
        elif type(data) is str:
            text = record.__getattribute__(column)
            text = text.replace('\xa3', '&POUND').replace('\xd9', '')
            utext = unicode(text, 'utf-8')
            cont.__dict__[column] = utext.replace('&POUND', u'\xa3')
        else:
            cont.__dict__[column] = data
    return cont
    


    

def combine(*args, **kwargs):
    """Combines several dataitems into a single string.
        
    By default, commas are removed from the end of dataitems. The optional
    filter argument can be used to specify other characters to strip.
    By default, a newline character is added to the end of each dataitem
    (apart from the last). The optional separator argument can be used to
    specify other end of line characters.
    """
        
    filter = kwargs.get('filter', ',')
    separator = kwargs.get('separator', '\n')
    output = []
    for line in args:
        output.append(line.strip(filter))
    output = separator.join(output)
    # No new-line character wanted at the end.
    return output

    
class container(object):
    def __repr__(self):
        contents = self.__dict__.values()
        answer = [str(thing) for thing in contents]
        return '<Record: ' + ', '.join(answer) + '>'
        

if __name__ == '__main__':
    map_and_update(material)
    map_and_update(hauliers)
    map_and_update(carrier)
    map_and_update(customer)
    map_and_update(supplier)
    map_and_update(contacts)
    map_and_update(depot)
    map_and_update(p_order)
    map_and_update(po_item)
    map_and_update(stock)
    map_and_update(s_order)
    map_and_update(so_item)
    map_and_update(so_deleted)
    map_and_update(despatch)
    map_and_update(stockmove)