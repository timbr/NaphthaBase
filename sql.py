""" sql.py  -- Contains Sql queries for R&R Access DB and NaphthaBase.
"""

#----------------------------------------------------------------------------#
# NaphthaBase Table Creation
#----------------------------------------------------------------------------#
create_formula_table = """
    CREATE TABLE Formula (
    id INTEGER PRIMARY KEY,
    Code varchar(10),
    Description varchar(40),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_purchase_order_table = """
    CREATE TABLE PurchaseOrder (
    id INTEGER PRIMARY KEY,
    PO_Num varchar(10),
    OrderValue varchar(15),
    Supplier varchar(10),
    OrderReference varchar(30),
    OrderDate date,
    PlacedBy varchar(30),
    PrintedComment text,
    DeliveryComment text,
    Status int,
    LastUpdated datetime,
    RecordNo int
    )
    """

create_purchase_item_table = """
    CREATE TABLE PurchaseItem (
    id INTEGER PRIMARY KEY,
    PO_Num varchar(10),
    Code varchar(10),
    Quantity varchar(15),
    Price varchar(15),
    DueDate date,
    DeliveredQuantity varchar(15),
    LastUpdated datetime,
    RecordNo int
    )    
    """

create_formula_stock_table = """
    CREATE TABLE FormulaStock (
    id INTEGER PRIMARY KEY,
    Batch varchar(10),
    BatchStatus varchar(10),
    QuantityNow varchar(15),
    OriginalDeliveredQuantity varchar(15),
    StockInfo text,
    Supplier varchar(15),
    PONumber varchar(10),
    PurchaseCost varchar(15),
    BatchUp_Date datetime,
    LastUpdated datetime,
    RecordNo int
    )
    """

create_formula_stock_usage_table = """
    CREATE TABLE FormulaStockUsage (
    id INTEGER PRIMARY KEY,
    Batch varchar(10),
    Code varchar(10),
    Revision int,
    Customer varchar(10),
    WONumber varchar(10),
    Price varchar(15),
    UsageReference text,
    StockAction text,
    ItemOrder varchar(10),
    QuantityMovement varchar(15),
    UserID varchar(10),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_sales_order_table = """
    CREATE TABLE SalesOrder (
    id INTEGER PRIMARY KEY,
    WO_Num varchar(10),
    Link varchar(10),
    CustomerKey varchar(10),
    CustomerOrderNumber varchar(30),
    DespatchNotes text,
    OrderValue varchar(15),
    Status int,
    OrderDate date,
    DespatchDate date,
    InvoiceDate date,
    Operator varchar(30),
    DespatchCompanyName varchar(40),
    DespatchAddress1 varchar(40),
    DespatchAddress2 varchar(40),
    DespatchAddress3 varchar(40),
    DespatchPostCode varchar(15),
    DeliveryNoteComment1 varchar(40),
    DeliveryNoteComment2 varchar(40),
    DeliveryNoteComment3 varchar(40),
    DeliveryNoteComment4 varchar(40),
    DeliveryNoteComment5 varchar(40),
    InvoiceComment1 varchar(40),
    InvoiceComment2 varchar(40),
    InvoiceComment3 varchar(40),
    InvoiceComment4 varchar(40),
    InvoiceComment5 varchar(40),
    InvoiceComment6 varchar(40),
    InvoiceTerms varchar(40),
    ItemCount int,
    LastUpdated datetime,
    RecordNo int
    )
    """

create_sales_order_item_table = """
    CREATE TABLE SalesOrderItem (
    id INTEGER PRIMARY KEY,
    Parent varchar(10),
    StockCode varchar(10),
    OrderQuantity varchar(15),
    Price varchar(15),
    RequiredDate date,
    LastUpdated datetime,
    RecordNo int
    )
    """

create_sales_order_additional_table = """
    CREATE TABLE SalesOrderAdditional (
    id INTEGER PRIMARY KEY,
    Parent varchar(10),
    Haulier varchar(40),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_sales_order_despatch_table = """
    CREATE TABLE SalesOrderDespatch (
    id INTEGER PRIMARY KEY,
    Key varchar(10),
    StockCode varchar(10),
    BatchDespatched varchar(10),
    DespatchedQuantity varchar(15),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_missing_order_number_table = """
    CREATE TABLE MissingOrderNumber (
    id INTEGER PRIMARY KEY,
    WO_Num varchar(10),
    UserID varchar(30),
    Reason varchar(40),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_additional_items_table = """
    CREATE TABLE AdditionalItems (
    id INTEGER PRIMARY KEY,
    HaulierKey varchar(10),
    Name varchar(30),
    NominalCode varchar(10),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_customer_table = """
    CREATE TABLE Customer (
    id INTEGER PRIMARY KEY,
    CustomerID varchar(10),
    Name varchar(30),
    Address1 varchar(30),
    Address2 varchar(30),
    Address3 varchar(30),
    Address4 varchar(30),
    Address5 varchar(30),
    PostCode varchar(10),
    Telephone varchar(15),
    Fax varchar(15),
    Email varchar(30),
    Website varchar(30),
    ContactName varchar(30),
    VAT varchar(30),
    Comment text,
    Memo text,
    CreditLimit varchar(30),
    Terms varchar(30),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_depot_table = """
    CREATE TABLE Depot (
    id INTEGER PRIMARY KEY,
    ClientID varchar(10),
    Name varchar(40),
    Address1 varchar(40),
    Address2 varchar(40),
    Address3 varchar(40),
    Address4 varchar(40),
    Address5 varchar(40),
    PostCode varchar(10),
    Telephone varchar(15),
    Fax varchar(15),
    Email varchar(40),
    Comment text,
    LastUpdated datetime,
    RecordNo int
    )
    """

create_contact_table = """
    CREATE TABLE Contact (
    id INTEGER PRIMARY KEY,
    ClientID varchar(10),
    Title varchar(10),
    Forename varchar(40),
    Surname varchar(40),
    Phone varchar(15),
    Department varchar(40),
    LastUpdated datetime,
    RecordNo int
    )
    """

create_supplier_table = """
    CREATE TABLE Supplier (
    id INTEGER PRIMARY KEY,
    SupplierID varchar(10),
    Name varchar(40),
    Address1 varchar(40),
    Address2 varchar(40),
    Address3 varchar(40),
    Address4 varchar(40),
    Address5 varchar(40),
    PostCode varchar(10),
    Telephone varchar(15),
    Fax varchar(15),
    Email varchar(40),
    Website varchar(40),
    ContactName varchar(40),
    VAT varchar(40),
    Comment text,
    Memo text,
    LastUpdated datetime,
    RecordNo int
    )
    """

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#----------------------------------------------------------------------------#
# Formula Table
#----------------------------------------------------------------------------#
formula = """
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
# Purchase Order Table
#----------------------------------------------------------------------------#
purchase_order = """
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
    \"Purchase Order\".\"Record Number\" AS RecordNo
    FROM \"Purchase Order\"
    WHERE \"Purchase Order\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Purchase Order\".\"Order Number\"
    """

#----------------------------------------------------------------------------#
# Purchase Item Table
#----------------------------------------------------------------------------#
purchase_item = """
    SELECT
    \"Purchase Item\".\"Order Number\" AS PO_Num,
    \"Purchase Item\".\"Component Code\" AS Code,
    \"Purchase Item\".Quantity,
    \"Purchase Item\".Price,
    \"Purchase Item\".\"Due Date\" AS DueDate,
    \"Purchase Item\".\"Delivered Quantity\" AS DeliveredQuantity,
    \"Purchase Item\".\"Last Updated\" AS LastUpdated,
    \"Purchase Item\".\"Record Number\" AS RecordNo
    FROM \"Purchase Item\"
    WHERE \"Purchase Item\".\"Last Updated\" > #%(lastupdate)s#
    """
           

#****************************************************************************#

#----------------------------------------------------------------------------#
# Formula Stock Table
#----------------------------------------------------------------------------#
formula_stock = """
    SELECT
    \"Formula Stock\".Batch,
    \"Formula Stock\".Type AS BatchStatus,
    \"Formula Stock\".Quantity AS QuantityNow,
    \"Formula Stock\".\"Original Quantity\" AS OriginalDeliveredQuantity,
    \"Formula Stock\".Location AS StockInfo,
    \"Formula Stock\".Supplier,
    \"Formula Stock\".PON AS PONumber,
    \"Formula Stock\".Cost AS PurchaseCost,
    \"Formula Stock\".\"Production Date\" AS BatchUp_Date,
    \"Formula Stock\".\"Last Updated\" AS LastUpdated,
    \"Formula Stock\".\"Record Number\" AS RecordNo
    FROM \"Formula Stock\"
    WHERE \"Formula Stock\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Formula Stock\".Batch
    """
    
#----------------------------------------------------------------------------#
# Formula Stock UsageTable
#----------------------------------------------------------------------------#
formula_stock_usage = """
    SELECT
    \"Formula Stock Usage\".Batch,
    \"Formula Stock Usage\".Formula AS Code,
    \"Formula Stock Usage\".Revision,
    \"Formula Stock Usage\".Customer,
    \"Formula Stock Usage\".\"Works order Number\" AS WONumber,
    \"Formula Stock Usage\".Price,
    \"Formula Stock Usage\".\"Usage Reference\" AS UsageReference,
    \"Formula Stock Usage\".\"Record Type\" AS StockAction,
    \"Formula Stock Usage\".\"Item Order\" AS ItemOrder,
    \"Formula Stock Usage\".Quantity AS QuantityMovement,
    \"Formula Stock Usage\".\"User ID\" AS UserID,
    \"Formula Stock Usage\".\"Last Updated\" AS LastUpdated,
    \"Formula Stock Usage\".\"Record Number\" AS RecordNo
    FROM \"Formula Stock Usage\"
    WHERE \"Formula Stock Usage\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Formula Stock Usage\".\"Last Updated\"
    """


#****************************************************************************#

#----------------------------------------------------------------------------#
# Sales Order Table
#----------------------------------------------------------------------------#
sales_order = """
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
    \"Sales Order\".\"Record Number\" AS RecordNo
    FROM \"Sales Order\"
    WHERE \"Sales Order\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Sales Order Item Table
#----------------------------------------------------------------------------#
sales_order_item = """
    SELECT
    \"Sales Order Item\".Parent,
    \"Sales Order Item\".\"Stock Code\" AS StockCode,
    \"Sales Order Item\".Quantity AS OrderQuantity,
    \"Sales Order Item\".Price,
    \"Sales Order Item\".\"Required Date\" AS RequiredDate,
    \"Sales Order Item\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Item\".\"Record Number\" AS RecordNo
    FROM \"Sales Order Item\"
    WHERE \"Sales Order Item\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Sales Order Additional Table
#----------------------------------------------------------------------------#
sales_order_additional = """
    SELECT
    \"Sales Order Additional\".Parent,
    \"Sales Order Additional\".Description AS Haulier,
    \"Sales Order Additional\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Additional\".\"Record Number\" AS RecordNo
    FROM \"Sales Order Additional\"
    WHERE \"Sales Order Additional\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Sales Order DespatchTable
#----------------------------------------------------------------------------#
sales_order_despatch = """
    SELECT
    \"Sales Order Despatch\".Key,
    \"Sales Order Despatch\".\"Stock Code\" AS StockCode,
    \"Sales Order Despatch\".Batch AS BatchDespatched,
    \"Sales Order Despatch\".Quantity AS DespatchedQuantity,
    \"Sales Order Despatch\".\"Last Updated\",
    \"Sales Order Despatch\".\"Record Number\" AS RecordNo
    FROM \"Sales Order Despatch\"
    WHERE \"Sales Order Despatch\".\"Last Updated\" > #%(lastupdate)s#
    """


#****************************************************************************#

#----------------------------------------------------------------------------#
# Missing Order Number Table
#----------------------------------------------------------------------------#
missing_order_number = """
    SELECT
    \"Missing Order Number\".Key AS WO_Num,
    \"Missing Order Number\".\"User ID\" AS UserID,
    \"Missing Order Number\".Reason AS Reason,
    \"Missing Order Number\".DateTime AS LastUpdated,
    \"Missing Order Number\".\"Record Number\" AS RecordNo
    FROM \"Missing Order Number\"
    WHERE (\"Missing Order Number\".Key > '1')
    AND (\"Missing Order Number\".DateTime > #%(lastupdate)s#)
    """


#****************************************************************************#

#----------------------------------------------------------------------------#
# Additional Items Table
#----------------------------------------------------------------------------#
additional_items = """
    SELECT
    \"Additional Items\".Key AS HaulierKey,
    \"Additional Items\".Name,
    \"Additional Items\".\"Nominal Code\" AS NominalCode,
    \"Additional Items\".\"Last Updated\" AS LastUpdated,
    \"Additional Items\".\"Record Number\" AS RecordNo
    FROM \"Additional Items\"
    WHERE \"Additional Items\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Additional Items\".\"Record Number\"
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Customer Table
#----------------------------------------------------------------------------#
customer = """
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
    Customer.\"Record Number\" AS RecordNo
    FROM Customer
    WHERE Customer.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Customer.ID
    """


#****************************************************************************#

#----------------------------------------------------------------------------#
# Depot Table
#----------------------------------------------------------------------------#
depot = """
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


#****************************************************************************#

#----------------------------------------------------------------------------#
# Contact Table
#----------------------------------------------------------------------------#
contact = """
    SELECT
    Contact.\"Client ID\" AS ClientID,
    Contact.Title,
    Contact.Forename,
    Contact.Surname,
    Contact.Phone,
    Contact.Department,
    Contact.\"Last Updated\" AS LastUpdated,
    Contact.\"Record Number\" AS RecordNo
    FROM Contact
    WHERE Contact.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Contact.\"Client ID\"
    """


#****************************************************************************#

#----------------------------------------------------------------------------#
# Supplier Table
#----------------------------------------------------------------------------#
supplier = """
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
    Supplier.\"Record Number\" AS RecordNo
    FROM Supplier
    WHERE Supplier.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Supplier.ID
    """

