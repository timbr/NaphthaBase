import naphthabase as nb
from update import *
import datetime
import decimal

rrdata = nb.RandRDatabase()
nbdb = loadSession()
Base.metadata.create_all()

def update_material():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Material). \
                            order_by(desc(Material.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Material).all()])
    all_rr_data = rrdata.query(nb.sql.get_material_codes,                           'stock_Formula')
    all_records = set([i.RecordNo for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_material_codes,                           'stock_Formula', lastupdated)
    
    recentmods = set([i.RecordNo for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNo in new_records:
            newmat = Material(id = None, \
                        code = record.Material, \
                        description = record.Description, \
                        lastupdated = record.LastUpdated, \
                        rr_recordno = record.RecordNo, \
                        deleted = False)
            newmat.lastupdated = record.LastUpdated
            nbdb.add(newmat)
        elif record.RecordNo in updated_records:
            lastrecord = nbdb.query(Material). \
             filter(Material.rr_recordno == record.RecordNo).all()[0]
            old = MaterialHistory(id = None, \
                        material_id = lastrecord.id, \
                        code = lastrecord.description, \
                        description = lastrecord.description, \
                        lastupdated = lastrecord.lastupdated, \
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Material(id = None, \
                        code = record.Material, \
                        description = record.Description, \
                        lastupdated = record.LastUpdated, \
                        rr_recordno = record.RecordNo, \
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
            
    nbdb.commit()
    print updated_records


def sanitise(record):
    cont = container()
    columns = [item[0] for item in record.cursor_description]
    for column in columns:
        data = record.__getattribute__(column)
        if type(data) is decimal.Decimal:
            cont.__dict__[column] = str(data)
        elif type(data) is str:
            cont.__dict__[column] = record.__getattribute__(column).replace('\xa3', '&POUND')
        else:
            cont.__dict__[column] = data
    return cont

    
class container(object):
    def __repr__(self):
        contents = self.__dict__.values()
        answer = [str(thing) for thing in contents]
        return '<Record: ' + ', '.join(answer) + '>'