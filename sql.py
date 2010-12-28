""" sql.py  -- Contains Sql queries for R&R Access DB and NaphthaBase.
"""

#----------------------------------------------------------------------------#
# NaphthaBase Table Creation
#----------------------------------------------------------------------------#

create_purchaseorder_table = """
    CREATE TABLE purchaseorder (
    id integer NOT NULL PRIMARY KEY,
    pon varchar(10),
    ordervalue varchar(15),
    supplier_id varchar(10) REFERENCES supplier (id),
    orderref varchar(20) NOT NULL,
    orderdate datetime NOT NULL,
    placedby varchar(50) NOT NULL,
    printedcomment varchar(100),
    deliverycomment varchar(100),
    status integer,
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_purchaseitem_table = """
    CREATE TABLE purchaseitem (
    id integer NOT NULL PRIMARY KEY,
    pon varchar(10),
    purchaseorder_id integer REFERENCES purchaseorder (id),
    material_id integer REFERENCES material (id),
    quantity varchar(15) NOT NULL,
    price varchar(15) NOT NULL,
    duedate datetime NOT NULL,
    delivered_quantity varchar(15) NOT NULL,
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_material_table = """
    CREATE TABLE material (
    id integer NOT NULL PRIMARY KEY,
    code varchar(10) NOT NULL,
    description varchar(50) NOT NULL,
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_stock_table = """
    CREATE TABLE stock (
    id integer NOT NULL PRIMARY KEY,
    batch varchar(10) NOT NULL,
    material_id integer REFERENCES material (id),
    stockinfo varchar(200),
    status varchar(1) NOT NULL,
    supplier_id integer REFERENCES supplier (id),
    purchaseitem_id integer REFERENCES purchaseitem (id),
    costprice varchar(20),
    batchup_quantity varchar(20) NOT NULL,
    batchup_date datetime NOT NULL,
    stockquantity varchar(20) NOT NULL,
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_stockmovement_table = """
    CREATE TABLE stockmovement (
    id integer NOT NULL PRIMARY KEY,
    stock_id integer REFERENCES stock (id),
    action varchar(10),
    customer_id integer REFERENCES customer (id),
    salesitem_id integer REFERENCES salesitem (id),
    salesprice varchar(20),
    movement_description varchar(100),
    movement_quantity varchar(20),
    item_order integer,
    user_id varchar(20),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_salesorder_table = """
    CREATE TABLE salesorder (
    id integer NOT NULL PRIMARY KEY,
    won varchar(10) NOT NULL,
    followon_link varchar(10),
    customer_id integer REFERENCES customer (id),
    customer_orderno varchar(20),
    picklist_comment varchar(200),
    ordervalue varchar(15) NOT NULL,
    status integer,
    orderdate datetime NOT NULL,
    despatchdate datetime NOT NULL,
    invoicedate datetime NOT NULL,
    operator varchar(20) NOT NULL,
    delivery_name varchar(100),
    delivery_address varchar(200),
    delivery_postcode varchar(20),
    printed_comments varchar(200),
    invoice_comments varchar(200),
    invoice_terms varchar(100),
    item_count integer,
    carrier_id integer REFERENCES carrier (id),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_salesitem_table = """
    CREATE TABLE salesitem (
    id integer NOT NULL PRIMARY KEY,
    won varchar(10),
    salesorder_id integer references salesorder (id),
    material_id integer references material (id),
    quantity varchar(15) NOT NULL,
    price varchar(15) NOT NULL,
    required_date datetime NOT NULL,
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """
    
create_despatch_table = """
    CREATE TABLE despatch (
    id integer NOT NULL PRIMARY KEY,
    won varchar(10),
    materialcode varchar(20) NOT NULL,
    stock_id integer REFERENCES stock (id),
    salesitem_id REFERENCES salesitem (id),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_carrier_table = """
    CREATE TABLE carrier (
    id integer NOT NULL PRIMARY KEY,
    won varchar(10),
    description varchar(50),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_deletedsales_table = """
    CREATE TABLE deletedsales (
    id integer NOT NULL PRIMARY KEY,
    won integer,
    operator varchar(20) NOT NULL,
    reason varchar(50),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_hauliers_table = """
    CREATE TABLE hauliers (
    id integer NOT NULL PRIMARY KEY,
    haulierkey varchar(20) NOT NULL,
    name varchar(50) NOT NULL,
    nominalcode varchar(10),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_customer_table = """
    CREATE TABLE customer (
    id integer NOT NULL PRIMARY KEY,
    customer_code varchar(10) NOT NULL,
    name varchar(50),
    address varchar(200),
    postcode varchar(10),
    phone varchar(20),
    fax varchar(20),
    email varchar(50),
    website varchar(50),
    contactname varchar(30),
    vat varchar(20),
    comment varchar(100),
    memo varchar(100),
    creditlimit varchar(15),
    terms varchar(20),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_supplier_table = """
    CREATE TABLE supplier (
    id integer NOT NULL PRIMARY KEY,
    supplier_code varchar(10) NOT NULL,
    name varchar(50),
    address varchar(200),
    postcode varchar(10),
    phone varchar(20),
    fax varchar(20),
    email varchar(50),
    website varchar(50),
    contactname varchar(30),
    vat varchar(20),
    comment varchar(100),
    memo varchar(100),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_contact_table = """
    CREATE TABLE contact (
    id integer NOT NULL PRIMARY KEY,
    clientcode varchar(10) NOT NULL,
    title varchar(10),
    forename varchar(20),
    surname varchar(20),
    phone varchar(20),
    department varchar(50),
    customer_id integer REFERENCES customer (id),
    supplier_id integer REFERENCES supplier (id),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """

create_depot_table = """
    CREATE TABLE depot (
    id integer NOT NULL PRIMARY KEY,
    clientid varchar(10) NOT NULL,
    clientname varchar(20),
    address varchar(200),
    postcode varchar(10),
    phone varchar(20),
    fax varchar(20),
    email varchar(50),
    comment varchar(100),
    customer_id integer REFERENCES customer (id),
    supplier_id integer REFERENCES supplier (id),
    lastupdated datetime NOT NULL,
    rr_recordno integer NOT NULL
    )
    """




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#----------------------------------------------------------------------------#
# Material Selection (R&R Database)
#----------------------------------------------------------------------------#
material_codes = """
    SELECT
    Formula.Key AS Code,
    Formula.Description,
    Formula.\"Last Updated\" AS LastUpdated,
    Formula.\"Record Number\" AS RecordNo
    FROM Formula
    WHERE (Formula.\"Customer Key\"='ANY')
    AND Formula.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Formula.Key
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Purchase Item Selection (R&R Database)
#----------------------------------------------------------------------------#
get_purchaseitem = """
    SELECT
    \"Purchase Item\".\"Order Number\" AS PO_Num,
    \"Purchase Item\".\"Component Code\" AS Code,
    \"Purchase Item\".Quantity,
    \"Purchase Item\".Price,
    \"Purchase Item\".\"Due Date\" AS DueDate,
    \"Purchase Item\".\"Delivered Quantity\" AS DeliveredQuantity,
    \"Purchase Item\".\"Last Updated\" AS LastUpdated,
    \"Purchase Item\".\"Record Number\" AS RecordNumber
    FROM \"Purchase Item\"
    WHERE \"Purchase Item\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Purchase Order Selection (R&R Database)
#----------------------------------------------------------------------------#
get_purchaseorder = """
    SELECT
    \"Purchase Order\".\"Order Number\" AS PO_Num,
    \"Purchase Order\".\"Order Value\" AS OrderValue,
    \"Purchase Order\".Supplier,
    \"Purchase Order\".\"Order Reference\" AS OrderReference,
    \"Purchase Order\".\"Order Date\" AS OrderDate,
    \"Purchase Order\".\"Placed By\" AS PlacedBy,
    \"Purchase Order\".\"Printed Comment\" AS PrintedComment,
    \"Purchase Order\".\"Delivery Comment\" As DeliveryComment,
    \"Purchase Order\".Status,
    \"Purchase Order\".\"Last Updated\" AS LastUpdated,
    \"Purchase Order\".\"Record Number\" AS RecordNumber     
    FROM \"Purchase Order\"
    WHERE \"Purchase Order\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Purchase Order Selection (NaphthaBase)
#----------------------------------------------------------------------------#
purchase_orders = """
    SELECT
    pon,
    Code,
    Batch,
    Quantity,
    Price,
    OrderValue,
    Supplier,
    OrderReference,
    OrderDate,
    DueDate,
    PlacedBy,
    DeliveredQuantity,
    PrintedComment,
    DeliveryComment,
    Status,
    LastUpdated
    FROM Purchases,
    (SELECT
        MAX(LastUpdated) AS latest from Purchases WHERE
        PO_Num = %(query)s)
    WHERE PO_Num = %(query)s and LastUpdated = latest
    ORDER BY Code
    """             

#****************************************************************************#

#----------------------------------------------------------------------------#
# Stock Selection (R&R Database)
#----------------------------------------------------------------------------#
get_stock = """
    SELECT
    \"Formula Stock\".Batch,
    \"Formula Stock\".Key AS Code,
    \"Formula Stock\".Location AS StockInfo,
    \"Formula Stock\".Type AS BatchStatus,
    \"Formula Stock\".Supplier,
    \"Formula Stock\".PON AS PONumber,
    \"Formula Stock\".Cost AS PurchaseCost,
    \"Formula Stock\".\"Original Quantity\" AS OriginalDeliveredQuantity,
    \"Formula Stock\".\"Production Date\" AS BatchUp_Date,
    \"Formula Stock\".Quantity AS QuantityNow,
    \"Formula Stock\".\"Last Updated\" AS LastUpdated,
    \"Formula Stock\".\"Record Number\" AS RecordNumber
    FROM \"Formula Stock\"
    WHERE \"Formula Stock\".\"Last Updated\" > #%(lastupdate)s#
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Stock Usage Selection (R&R Database)
#----------------------------------------------------------------------------#
get_stockusage = """
    SELECT
    \"Formula Stock Usage\".Batch,
    \"Formula Stock Usage\".\"Record Type\" AS Action,
    \"Formula Stock Usage\".Customer,
    \"Formula Stock Usage\".\"Works Order Number\" AS WON,
    \"Formula Stock Usage\".Formula,
    \"Formula Stock Usage\".Price,
    \"Formula Stock Usage\".\"Usage Reference\" AS UsageRef,
    \"Formula Stock Usage\".Quantity,
    \"Formula Stock Usage\".\"Item Order\" AS ItemOrder,
    \"Formula Stock Usage\".\"User ID\" AS UserID,
    \"Formula Stock Usage\".\"Last Updated\" AS LastUpdated,
    \"Formula Stock Usage\".\"Record Number\" AS RecordNumber
    FROM \"Formula Stock Usage\"
    WHERE \"Formula Stock Usage\".\"Last Updated\" > #%(lastupdate)s#
    """    


#----------------------------------------------------------------------------#
# Stock Selection (NaphthaBase)
#----------------------------------------------------------------------------#
get_batch = """
    SELECT
    Batch,
    Code,
    Revision,
    BatchStatus,
    QuantityNow,
    OriginalDeliveredQuantity,
    StockInfo,
    Supplier,
    PONumber,
    PurchaseCost,
    Customer,
    WONumber,
    Price,
    UsageReference,
    StockAction,
    ItemOrder,
    QuantityMovement,
    UserID,
    LastUpdated,
    InvoiceDate,
    BatchUp_Date
    FROM Stock
    WHERE Batch = %(query)s
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Sales Order Selection (R&R Database)
#----------------------------------------------------------------------------#
get_despatch = """
    SELECT
    \"Sales Order Despatch\".Key AS WON,
    \"Sales Order Despatch\".\"Stock Code\" AS Material,
    \"Sales Order Despatch\".Batch AS BatchDespatched,
    \"Sales Order Despatch\".Quantity AS DespatchedQuantity,
    \"Sales Order Despatch\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Despatch\".\"Record Number\" AS RecordNumber
    FROM \"Sales Order Despatch\"
    WHERE \"Sales Order Despatch\".\"Last Updated\" > #%(lastupdate)s#
    """


#----------------------------------------------------------------------------#
# Sales Order Selection (R&R Database)
#----------------------------------------------------------------------------#
get_salesitem = """
    SELECT
    \"Sales Order Item\".Parent AS WO_Num,
    \"Sales Order Item\".\"Stock Code\" AS StockCode,
    \"Sales Order Item\".Quantity AS OrderQuantity,
    \"Sales Order Item\".Price,
    \"Sales Order Item\".\"Required Date\" AS RequiredDate,
    \"Sales Order Item\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Item\".\"Record Number\" AS RecordNumber
    FROM \"Sales Order Item\"
    WHERE \"Sales Order Item\".\"Last Updated\" > #%(lastupdate)s#
    """
    
    
#----------------------------------------------------------------------------#
# Sales Order Selection (R&R Database)
#----------------------------------------------------------------------------#
get_salesorder = """
    SELECT
    \"Sales Order\".Key AS WO_Num,
    \"Sales Order\".Link,
    \"Sales Order\".CustomerKey,
    \"Sales Order\".\"Customer Order Number\" AS CustomerOrderNumber,
    \"Sales Order\".Comment AS DespatchNotes,
    \"Sales Order\".\"Order Value\" AS OrderValue,
    \"Sales Order\".Status,
    \"Sales Order\".\"Order Date\" AS OrderDate,
    \"Sales Order\".\"Despatch Date\" AS DespatchDate,
    \"Sales Order\".\"Invoice Date\" AS InvoiceDate,
    \"Sales Order\".Operator,
    \"Sales Order\".Name AS DespatchCompanyName,
    \"Sales Order\".Address1 AS DespatchAddress1,
    \"Sales Order\".Address2 AS DespatchAddress2,
    \"Sales Order\".Address3 AS DespatchAddress3,
    \"Sales Order\".Address4 AS DespatchAddress4,
    \"Sales Order\".\"Post Code\" AS DespatchPostCode,
    \"Sales Order\".\"Printed Comment1\" AS DeliveryNoteComment1,
    \"Sales Order\".\"Printed Comment2\" AS DeliveryNoteComment2,
    \"Sales Order\".\"Printed Comment3\" AS DeliveryNoteComment3,
    \"Sales Order\".\"Printed Comment4\" AS DeliveryNoteComment4,
    \"Sales Order\".\"Printed Comment5\" AS DeliveryNoteComment5,
    \"Sales Order\".\"Invoice Comment1\" AS InvoiceComment1,
    \"Sales Order\".\"Invoice Comment2\" AS InvoiceComment2,
    \"Sales Order\".\"Invoice Comment3\" AS InvoiceComment3,
    \"Sales Order\".\"Invoice Comment4\" AS InvoiceComment4,
    \"Sales Order\".\"Invoice Comment5\" AS InvoiceComment5,
    \"Sales Order\".\"Invoice Comment6\" AS InvoiceComment6,
    \"Sales Order\".\"Invoice terms\" AS InvoiceTerms,
    \"Sales Order\".\"Item Count\" AS ItemCount,
    \"Sales Order\".\"Last Updated\" AS LastUpdated,
    \"Sales Order\".\"Record Number\" AS RecordNumber
    FROM \"Sales Order\"
    WHERE \"Sales Order\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Sales Order Selection (NaphthaBase)
#----------------------------------------------------------------------------#
sales_orders = """
    SELECT
    WO_Num,
    Link,
    StockCode,
    CustomerKey,
    CustomerOrderNumber,
    DespatchNotes,
    OrderQuantity,
    Price,
    OrderValue,
    Status,
    OrderDate,
    RequiredDate,
    DespatchDate,
    InvoiceDate,
    Operator,
    DespatchCompanyName,
    DespatchAddress1,
    DespatchAddress2,
    DespatchAddress3,
    DespatchPostCode,
    DeliveryNoteComment1,
    DeliveryNoteComment2,
    DeliveryNoteComment3,
    DeliveryNoteComment4,
    DeliveryNoteComment5,
    InvoiceComment1,
    InvoiceComment2,
    InvoiceComment3,
    InvoiceComment4,
    InvoiceComment5,
    InvoiceComment6,
    InvoiceTerms,
    ItemCount,
    Haulier,
    BatchDespatched,
    DespatchedQuantity,
    LastUpdated
    FROM Sales,
    (SELECT
        MAX(LastUpdated) AS latest from Sales WHERE
        WO_Num = %(query)s)
    WHERE WO_Num = %(query)s and LastUpdated = latest
    ORDER BY WO_Num
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Sales Order Additional(R&R Database)
#----------------------------------------------------------------------------#
get_carrier = """
    SELECT
    \"Sales Order Additional\".Parent AS WO_Num,
    \"Sales Order Additional\".Description AS Description,
    \"Sales Order Additional\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Additional\".\"Record Number\" AS RecordNumber
    FROM \"Sales Order Additional\"
    WHERE \"Sales Order Additional\".\"Last Updated\" > #%(lastupdate)s#
    """    

#****************************************************************************#

#----------------------------------------------------------------------------#
# Deleted Sales Orders(R&R Database)
#----------------------------------------------------------------------------#
get_deleted_sales = """
    SELECT
    \"Missing Order Number\".Key AS WO_Num,
    \"Missing Order Number\".\"User ID\" AS UserID,
    \"Missing Order Number\".Reason AS Reason,
    \"Missing Order Number\".DateTime AS LastUpdated
    FROM \"Missing Order Number\"
    WHERE \"Missing Order Number\".Key > '1'
    """

#----------------------------------------------------------------------------#
# Deleted Sales Selection (NaphthaBase)
#----------------------------------------------------------------------------#
deleted_sales_orders = """
    SELECT
    WO_Num,
    UserID,
    Reason,
    LastUpdated
    FROM DeletedSales
    WHERE WO_Num = %(query)s
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Hauliers Selection (R&R Database)
#----------------------------------------------------------------------------#
get_hauliers = """
    SELECT
    \"Additional Items\".Key AS HaulierKey,
    \"Additional Items\".Name,
    \"Additional Items\".\"Nominal Code\" AS NominalCode,
    \"Additional Items\".\"Last Updated\" AS LastUpdated,
    \"Additional Items\".\"Record Number\" AS RecordNumber
    FROM \"Additional Items\"
    WHERE \"Additional Items\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Additional Items\".\"Record Number\"
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Customer Selection (R&R Database)
#----------------------------------------------------------------------------#
get_customer = """
    SELECT
    Customer.ID AS CustomerID,
    Customer.Name,
    Customer.Address1,
    Customer.Address2,
    Customer.Address3,
    Customer.Address4,
    Customer.Address5,
    Customer.\"Post Code\" AS PostCode,
    Customer.Telephone,
    Customer.Fax,
    Customer.Email,
    Customer.\"Web Site\" AS Website,
    Customer.\"Contact Name\" AS ContactName,
    Customer.\"Vat Registration Number\" AS VAT,
    Customer.Comment,
    Customer.Memo,
    Customer.\"Credit Limit\" AS CreditLimit,
    Customer.Terms,
    Customer.\"Last Updated\" AS LastUpdated,
    Customer.\"Record Number\" AS RecordNumber
    FROM Customer
    WHERE Customer.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Customer.ID
    """

#----------------------------------------------------------------------------#
# Customer Selection (NaphthaBase)
#----------------------------------------------------------------------------#
customer = """
    SELECT
    CustomerID,
    Name,
    Address1,
    Address2,
    Address3,
    Address4,
    Address5,
    PostCode,
    Telephone,
    Fax,
    Email,
    Website,
    ContactName,
    VAT,
    Comment,
    Memo,
    CreditLimit,
    Terms,
    LastUpdated
    FROM Customer
    WHERE CustomerID like '%(query)s' OR
    Name like '%(query)s'
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Depot Selection (R&R Database)
#----------------------------------------------------------------------------#
get_depot = """
    SELECT
    Depot.\"Client ID\" AS ClientID,
    Depot.Name,
    Depot.Address1,
    Depot.Address2,
    Depot.Address3,
    Depot.Address4,
    Depot.Address5,
    Depot.\"Post code\" AS PostCode,
    Depot.Telephone,
    Depot.Fax,
    Depot.Email,
    Depot.Comment,
    Depot.\"Last Updated\" AS LastUpdated,
    Depot.\"Record Number\" AS RecordNo
    FROM Depot
    WHERE Depot.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Depot.\"Client ID\"
    """

#----------------------------------------------------------------------------#
# Depot Selection (NaphthaBase)
#----------------------------------------------------------------------------#
depot = """
    SELECT
    ClientID,
    Name,
    Address1,
    Address2,
    Address3,
    Address4,
    Address5,
    PostCode,
    Telephone,
    Fax,
    Email,
    Comment,
    LastUpdated
    FROM Depot
    WHERE ClientID like '%(query)s'
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Contact Selection (R&R Database)
#----------------------------------------------------------------------------#
get_contact = """
    SELECT
    Contact.\"Client ID\" AS ClientID,
    Contact.Title,
    Contact.Forename,
    Contact.Surname,
    Contact.Phone,
    Contact.Department,
    Contact.\"Last Updated\" AS LastUpdated,
    Contact.\"Record Number\" AS RecordNumber
    FROM Contact
    WHERE Contact.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Contact.\"Client ID\"
    """

#----------------------------------------------------------------------------#
# Contact Selection (NaphthaBase)
#----------------------------------------------------------------------------#
contact = """
    SELECT
    ClientID,
    Title,
    Forename,
    Surname,
    Phone,
    Department,
    LastUpdated
    FROM Contact
    WHERE ClientID like '%(query)s'
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Supplier Selection (R&R Database)
#----------------------------------------------------------------------------#
get_supplier = """
    SELECT
    Supplier.ID AS SupplierID,
    Supplier.Name,
    Supplier.Address1,
    Supplier.Address2,
    Supplier.Address3,
    Supplier.Address4,
    Supplier.Address5,
    Supplier.\"Post Code\" AS PostCode,
    Supplier.Telephone,
    Supplier.Fax,
    Supplier.Email,
    Supplier.\"Web Site\" AS Website,
    Supplier.\"Contact Name\" AS ContactName,
    Supplier.\"Vat Registration Number\" AS VAT,
    Supplier.Comment,
    Supplier.Memo,
    Supplier.\"Last Updated\" AS LastUpdated,
    Supplier.\"Record Number\" AS RecordNumber
    FROM Supplier
    WHERE Supplier.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Supplier.ID
    """

#----------------------------------------------------------------------------#
# Supplier Selection (NaphthaBase)
#----------------------------------------------------------------------------#
supplier = """
    SELECT
    SupplierID,
    Name,
    Address1,
    Address2,
    Address3,
    Address4,
    Address5,
    PostCode,
    Telephone,
    Fax,
    Email,
    Website,
    ContactName,
    VAT,
    Comment,
    Memo,
    LastUpdated
    FROM Supplier
    WHERE SupplierID like '%(query)s' OR
    Name like '%(query)s'
    """