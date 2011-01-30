import naphthabase as nb
from update import *
import datetime


rrdata = nb.RandRDatabase()
nbdb = loadSession()
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
    print type(entry.LastUpdated)
    new_material = Material(None,entry.Material, entry.Description, entry.LastUpdated, entry.RecordNo)
    new_material.lastupdated = entry.LastUpdated
    nbdb.add(new_material)

nbdb.commit()
        
