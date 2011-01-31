import naphthabase as nb
from update import *
import datetime
from populatedb import DataContainer


rrdata = nb.RandRDatabase()
nbdb = loadSession()

#---------------------------------------------------------------------------------------------------------------------------------------
lastrecord = nbdb.query(Material).order_by(desc(Material.lastupdated)).first()
print lastrecord, lastrecord.lastupdated

r_and_r_sql = nb.sql.get_material_codes
r_and_r_table = 'stock_Formula'
dbreply = rrdata.query(r_and_r_sql, r_and_r_table, lastrecord.lastupdated)

for entry in dbreply:
    existing = nbdb.query(Material). \
                    filter(Material.rr_recordno == entry.RecordNo).all()
    if len(existing) > 0:
        print "\n!!! %s (record %s) already exists\n" % (entry.Material, entry.RecordNo)
    print "\n####\n%s, %s\n\n" % (entry.Material, entry.LastUpdated)
    new_material = Material(None, entry.Material, entry.Description, entry.LastUpdated, entry.RecordNo)
    new_material.lastupdated = entry.LastUpdated
    print "\n\n---> Adding %s to Material\n" % (new_material.code)
    nbdb.add(new_material)

#---------------------------------------------------------------------------------------------------------------------------------------

lastrecord = nbdb.query(Hauliers).order_by(desc(Hauliers.lastupdated)).first()
print lastrecord, lastrecord.lastupdated

r_and_r_sql = nb.sql.get_hauliers
r_and_r_table = 'stock_Additional Items'
dbreply = rrdata.query(r_and_r_sql, r_and_r_table, lastrecord.lastupdated)

for entry in dbreply:
    existing = nbdb.query(Hauliers). \
                    filter(Hauliers.rr_recordno == entry.RecordNumber).all()
    if len(existing) > 0:
        print "\n!!! %s (record %s) already exists\n" % (entry.HaulierKey, entry.RecordNumber)
    print "\n####\n%s, %s\n\n" % (entry.HaulierKey, entry.LastUpdated)
    new_haulier = Hauliers(None, entry.HaulierKey, entry.Name, entry.NominalCode, entry.LastUpdated, entry.RecordNumber)
    new_haulier.lastupdated = entry.LastUpdated
    print "\n\n---> Adding %s to Hauliers\n" % (new_haulier.haulierkey)
    nbdb.add(new_haulier)

#---------------------------------------------------------------------------------------------------------------------------------------

lastrecord = nbdb.query(Carrier).order_by(desc(Carrier.lastupdated)).first()
print lastrecord, lastrecord.lastupdated

r_and_r_sql = nb.sql.get_carrier
r_and_r_table = 'stock_Sales Order Additional'
dbreply = rrdata.query(r_and_r_sql, r_and_r_table, lastrecord.lastupdated)

for entry in dbreply:
    existing = nbdb.query(Carrier). \
                    filter(Carrier.rr_recordno == entry.RecordNumber).all()
    if len(existing) > 0:
        print "\n!!! %s (record %s) already exists\n" % (entry.WO_Num, entry.RecordNumber)
    print "\n####\n%s, %s\n\n" % (entry.WO_Num, entry.LastUpdated)
    new_carrier = Carrier(None, entry.WO_Num, entry.Description, entry.LastUpdated, entry.RecordNumber)
    new_carrier.lastupdated = entry.LastUpdated
    print "\n\n---> Adding %s to Carrier\n" % (new_carrier.won)
    nbdb.add(new_carrier)

#---------------------------------------------------------------------------------------------------------------------------------------

lastrecord = nbdb.query(Customer).order_by(desc(Customer.lastupdated)).first()
print lastrecord, lastrecord.lastupdated

r_and_r_sql = nb.sql.get_customer
r_and_r_table = 'accounts_Customer'
dbreply = rrdata.query(r_and_r_sql, r_and_r_table, lastrecord.lastupdated)

for entry in dbreply:
    existing = nbdb.query(Customer). \
                    filter(Customer.rr_recordno == entry.RecordNumber).all()
    if len(existing) > 0:
        print "\n!!! %s (record %s) already exists\n" % (entry.CustomerID, entry.RecordNumber)
    dc = DataContainer()
    address = dc.combine(entry.Address1,
                         entry.Address2,
                         entry.Address3,
                         entry.Address4,
                         entry.Address5)
    print "\n####\n%s, %s\n\n" % (entry.CustomerID, entry.LastUpdated)
    new_customer = Customer(None, entry.CustomerID, entry.Name, address, entry.PostCode, entry.Telephone, entry.Fax, entry.Email, entry.Website, entry.ContactName, entry.VAT, entry.Comment, entry.Memo, entry.CreditLimit, entry.Terms, entry.LastUpdated, entry.RecordNumber)
    new_customer.lastupdated = entry.LastUpdated
    print "\n\n---> Adding %s to Customer\n" % (new_customer.customer_code)
    nbdb.add(new_customer)


nbdb.commit()
        
