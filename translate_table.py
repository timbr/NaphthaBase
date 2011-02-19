"""translate_table.py

A dictionary describing the translation of data from the R&R DB to the NaphthaBase
"""

import sql

material = {'rrtable'              :   'stock_Formula',
            'rrsql'                :    sql.get_material_codes,
            'nbtable'              :   'Material',
            
    'Map' : {
            'code'                 :   'Material',
            'description'          :   'Description',
            'minimumstock'         :   'MinimumStock',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

hauliers = {'rrtable'              :   'stock_Additional Items',
            'rrsql'                :    sql.get_hauliers,
            'nbtable'              :   'Hauliers',
            
    'Map' : {
            'haulierkey'           :   'HaulierKey',
            'name'                 :   'Name',
            'nominalcode'          :   'NominalCode',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

carrier  = {'rrtable'              :   'stock_Sales Order Additional',
            'rrsql'                :    sql.get_carrier,
            'nbtable'              :   'Carrier',
            
    'Map' : {
            'won'                  :   'WO_Num',
            'description'          :   'Description',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }
            
          
customer = {'rrtable'              :   'accounts_Customer',
            'rrsql'                :    sql.get_customer,
            'nbtable'              :   'Customer',
            
    'Map' : {
            'customer_code'        :   'CustomerID',
            'name'                 :   'Name',
            'address'              :  ['Address1',
                                       'Address2',
                                       'Address3',
                                       'Address4',
                                       'Address5'],
            'postcode'             :   'PostCode',
            'phone'                :   'Telephone',
            'fax'                  :   'Fax',
            'email'                :   'Email',
            'website'              :   'Website',
            'contactname'          :   'ContactName',
            'vat'                  :   'VAT',
            'comment'              :   'Comment',
            'memo'                 :   'Memo',
            'creditlimit'          :   'CreditLimit',
            'terms'                :   'Terms',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

supplier = {'rrtable'              :   'accounts_Supplier',
            'rrsql'                :    sql.get_supplier,
            'nbtable'              :   'Supplier',
            
    'Map' : {
            'supplier_code'        :   'SupplierID',
            'name'                 :   'Name',
            'address'              :  ['Address1',
                                       'Address2',
                                       'Address3',
                                       'Address4',
                                       'Address5'],
            'postcode'             :   'PostCode',
            'phone'                :   'Telephone',
            'fax'                  :   'Fax',
            'email'                :   'Email',
            'website'              :   'Website',
            'contactname'          :   'ContactName',
            'vat'                  :   'VAT',
            'comment'              :   'Comment',
            'memo'                 :   'Memo',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

contacts = {'rrtable'              :   'accounts_Contact',
            'rrsql'                :    sql.get_contact,
            'nbtable'              :   'Contact',
            
    'Map' : {
            'clientcode'           :   'ClientID',
            'title'                :   'Title',
            'forename'             :   'Forename',
            'surname'              :   'Surname',
            'phone'                :   'Phone',
            'department'           :   'Department',
            'customer_id'          :  {'func':
                                       'get_customer_id(record.ClientID)'},
            'supplier_id'          :  {'func':
                                       'get_supplier_id(record.ClientID)'},
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

depot    = {'rrtable'              :   'accounts_Depot',
            'rrsql'                :    sql.get_depot,
            'nbtable'              :   'Depot',
            
    'Map' : {
            'clientid'             :   'ClientID',
            'clientname'           :   'Name',
            'address'              :  ['Address1',
                                       'Address2',
                                       'Address3',
                                       'Address4',
                                       'Address5'],
            'postcode'             :   'PostCode',
            'phone'                :   'Telephone',
            'fax'                  :   'Fax',
            'email'                :   'Email',
            'comment'              :   'Comment',
            'customer_id'          :  {'func':
                                       'get_customer_id(record.ClientID)'},
            'supplier_id'          :  {'func':
                                       'get_supplier_id(record.ClientID)'},
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }
            
p_order =  {'rrtable'              :   'stock_Purchase Order',
            'rrsql'                :    sql.get_purchaseorder,
            'nbtable'              :   'PurchaseOrder',
            
    'Map' : {
            'pon'                  :   'PO_Num',
            'ordervalue'           :   'OrderValue',
            'supplier_id'          :  {'func':
                                       'get_supplier_id(record.Supplier)'},
            'orderref'             :   'OrderReference',
            'orderdate'            :   'OrderDate',
            'placedby'             :   'PlacedBy',
            'printedcomment'       :   'PrintedComment',
            'deliverycomment'      :   'DeliveryComment',
            'status'               :   'Status',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }
            
po_item  = {'rrtable'              :   'stock_Purchase Item',
            'rrsql'                :    sql.get_purchaseitem,
            'nbtable'              :   'PurchaseItem',
            
    'Map' : {
            'pon'                  :   'PO_Num',
            'itemno'               :   'Index',
            'purchaseorder_id'     :  {'func':
                                       'get_purchaseorder_id(record.PO_Num)'},
            'material_id'          :  {'func':
                                       'get_material_id(record.Material)'},
            'quantity'             :   'Quantity',
            'price'                :   'Price',
            'duedate'              :   'DueDate',
            'delivered_quantity'   :   'DeliveredQuantity',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

stock   =  {'rrtable'              :   'stock_Formula Stock',
            'rrsql'                :    sql.get_stock,
            'nbtable'              :   'Stock',
            
    'Map' : {
            'batch'                :   'Batch',
            'material_id'          :  {'func':
                                       'get_material_id(record.Material)'},
            'stockinfo'            :   'StockInfo',
            'status'               :   'BatchStatus',
            'supplier_id'          :  {'func':
                                       'get_supplier_id(record.Supplier)'},
            'purchaseitem_id'      :  {'func':
                          'get_purchaseitem_id(record.PO_Num, record.Batch)'},
            
            'costprice'            :   'PurchaseCost',
            'batchup_quantity'     :   'OriginalDeliveredQuantity',
            'batchup_date'         :   'BatchUp_Date',
            'stockquantity'        :   'QuantityNow',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

s_order =  {'rrtable'              :   'stock_Sales Order',
            'rrsql'                :    sql.get_salesorder,
            'nbtable'              :   'SalesOrder',
            
    'Map' : {
            'won'                  :   'WO_Num',
            'followon_link'        :   'Link',
            'customer_id'          :  {'func':
                                       'get_customer_id(record.CustomerKey)'},
            'customer_orderno'     :   'CustomerOrderNumber',
            'picklist_comment'     :   'DespatchNotes',
            'ordervalue'           :   'OrderValue',
            'status'               :   'Status',
            'orderdate'            :   'OrderDate',
            'despatchdate'         :   'DespatchDate',
            'invoicedate'          :   'InvoiceDate',
            'operator'             :   'Operator',
            'delivery_name'        :   'DespatchCompanyName',
            'delivery_address'     :  ['DespatchAddress1',
                                       'DespatchAddress2',
                                       'DespatchAddress3',
                                       'DespatchAddress4'],
            'delivery_postcode'    :   'DespatchPostCode',
            'printed_comments'     :  ['DeliveryNoteComment1',
                                       'DeliveryNoteComment2',
                                       'DeliveryNoteComment3',
                                       'DeliveryNoteComment4',
                                       'DeliveryNoteComment5'],
            'invoice_comments'     :  ['InvoiceComment1',
                                       'InvoiceComment2',
                                       'InvoiceComment3',
                                       'InvoiceComment4',
                                       'InvoiceComment5',
                                       'InvoiceComment6'],
            'invoice_terms'        :   'InvoiceTerms',
            'item_count'           :   'ItemCount',
            'carrier_id'           :  {'func':
                                       'get_carrier_id(record.WO_Num)'},
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

so_item  = {'rrtable'              :   'stock_Sales Order Item',
            'rrsql'                :    sql.get_salesitem,
            'nbtable'              :   'SalesItem',
            
    'Map' : {
            'won'                  :   'WO_Num',
            'salesorder_id'        :  {'func':
                                       'get_salesorder_id(record.WO_Num)'},
            'material_id'          :  {'func':
                                       'get_material_id(record.Material)'},
            'quantity'             :   'OrderQuantity',
            'price'                :   'Price',
            'required_date'        :   'RequiredDate',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

so_deleted = {'rrtable'            :   'stock_Missing Order Number',
            'rrsql'                :    sql.get_deleted_sales,
            'nbtable'              :   'DeletedSales',
            
    'Map' : {
            'won'                  :   'WO_Num',
            'salesorder_id'        :  {'func':
                                       'get_salesorder_id(record.WO_Num)'},
            'operator'             :   'UserID',
            'reason'               :   'Reason',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

despatch = {'rrtable'              :   'stock_Sales Order Despatch',
            'rrsql'                :    sql.get_despatch,
            'nbtable'              :   'Despatch',
            
    'Map' : {
            'won'                  :   'WO_Num',
            'materialcode'         :   'Material',
            'stock_id'             :  {'func':
                                      'get_stock_id(record.BatchDespatched)'},
            'salesitem_id'         :  {'func':
                                       'get_salesitem_id(record.WO_Num, record.Material)'},
            'batch'                :   'BatchDespatched',
            'quantity'             :   'DespatchedQuantity',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }

stockmove = {'rrtable'             :   'stock_Formula Stock Usage',
            'rrsql'                :    sql.get_stockusage,
            'nbtable'              :   'StockMovement',
            
    'Map' : {
            'stock_id'             :  {'func':
                                       'get_stock_id(record.Batch)'},
            'action'               :   'Action',
            'customer_id'          :  {'func':
                                       'get_customer_id(record.Customer)'},
            'salesitem_id'         :  {'func':
                                       'get_salesitem_id(record.WO_Num, record.Material)'},
            'salesprice'           :   'Price',
            'pon'                  :   'PO_Num',
            'movement_description' :   'UsageRef',
            'movement_quantity'    :   'Quantity',
            'item_order'           :   'ItemOrder',
            'user_id'              :   'UserID',
            'lastupdated'          :   'LastUpdated',
            'rr_recordno'          :   'RecordNumber'
            }
            }