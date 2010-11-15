""" sql.py  -- Contains Sql queries for R&R Access DB and NaphthaBase.
"""

#----------------------------------------------------------------------------#
# NaphthaBase Table Creation
#----------------------------------------------------------------------------#
create_formula_table = """
    CREATE TABLE Formula (
    Code text,
    Description text,
    LastUpdated date,
    RecordNo int
    )
    """

create_purchase_order_table = """
    CREATE TABLE PurchaseOrder (
    PO_Num text,
    OrderValue text,
    Supplier text,
    OrderReference text,
    OrderDate date,
    PlacedBy text,
    PrintedComment text,
    DeliveryComment text,
    Status int
    )
    """

create_purchase_item_table = """
    CREATE TABLE PurchaseItem (
    PO_Num text,
    Code text,
    Quantity text,
    Price text,
    DueDate date,
    DeliveredQuantity text,
    LastUpdated date
    )    
    """

create_formula_stock_table = """
    CREATE TABLE FormulaStock (
    Batch text,
    BatchStatus text,
    QuantityNow text,
    OriginalDeliveredQuantity text,
    StockInfo text,
    Supplier text,
    PONumber text,
    PurchaseCost text,
    InvoiceDate date,
    BatchUp_Date date
    )
    """

create_formula_stock_usage_table = """
    CREATE TABLE FormulaStockUsage (
    Batch text,
    Code text,
    Revision int,
    Customer text,
    WONumber text,
    Price text,
    UsageReference text,
    StockAction text,
    ItemOrder text,
    QuantityMovement text,
    UserID text,
    LastUpdated date
    )
    """

create_sales_order_table = """
    CREATE TABLE SalesOrder (
    WO_Num text,
    Link text,
    CustomerKey text,
    CustomerOrderNumber text,
    DespatchNotes text,
    OrderValue text,
    Status int,
    OrderDate date,
    DespatchDate date,
    InvoiceDate date,
    Operator text,
    DespatchCompanyName text,
    DespatchAddress1 text,
    DespatchAddress2 text,
    DespatchAddress3 text,
    DespatchPostCode text,
    DeliveryNoteComment1 text,
    DeliveryNoteComment2 text,
    DeliveryNoteComment3 text,
    DeliveryNoteComment4 text,
    DeliveryNoteComment5 text,
    InvoiceComment1 text,
    InvoiceComment2 text,
    InvoiceComment3 text,
    InvoiceComment4 text,
    InvoiceComment5 text,
    InvoiceComment6 text,
    InvoiceTerms text,
    ItemCount int,
    LastUpdated date
    )
    """

create_sales_order_item_table = """
    CREATE TABLE SalesOrderItem (
    Parent text,
    StockCode text,
    OrderQuantity text,
    Price text,
    RequiredDate date
    )
    """

create_sales_order_additional_table = """
    CREATE TABLE SalesOrderAdditional (    
    Parent text,
    Haulier text
    )
    """

create_sales_order_despatch_table = """
    CREATE TABLE SalesOrderDespatch (    
    Key text,
    StockCode text,
    BatchDespatched text,
    DespatchedQuantity text
    )
    """

create_missing_order_number_table = """
    CREATE TABLE MissingOrderNumber (
    WO_Num text,
    UserID text,
    Reason text,
    LastUpdated date
    )
    """

create_additional_items_table = """
    CREATE TABLE AdditionalItems (
    HaulierKey text,
    Name text,
    NominalCode text,
    LastUpdated date
    )
    """

create_customer_table = """
    CREATE TABLE Customer (
    CustomerID text,
    Name text,
    Address1 text,
    Address2 text,
    Address3 text,
    Address4 text,
    Address5 text,
    PostCode text,
    Telephone text,
    Fax text,
    Email text,
    Website text,
    ContactName text,
    VAT text,
    Comment text,
    Memo text,
    CreditLimit text,
    Terms text,
    LastUpdated date
    )
    """

create_depot_table = """
    CREATE TABLE Depot (
    ClientID text,
    Name text,
    Address1 text,
    Address2 text,
    Address3 text,
    Address4 text,
    Address5 text,
    PostCode text,
    Telephone text,
    Fax text,
    Email text,
    Comment text,
    LastUpdated date
    )
    """

create_contact_table = """
    CREATE TABLE Contact (
    ClientID text,
    Title text,
    Forename text,
    Surname text,
    Phone text,
    Department text,
    LastUpdated date
    )
    """

create_supplier_table = """
    CREATE TABLE Supplier (
    SupplierID text,
    Name text,
    Address1 text,
    Address2 text,
    Address3 text,
    Address4 text,
    Address5 text,
    PostCode text,
    Telephone text,
    Fax text,
    Email text,
    Website text,
    ContactName text,
    VAT text,
    Comment text,
    Memo text,
    LastUpdated text
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
    \"Purchase Order\".Status
    FROM \"Purchase Order\"
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
    \"Purchase Item\".\"Last Updated\" AS LastUpdated       
    FROM \"Purchase Item\"
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
    \"Formula Stock\".\"Last Updated\" AS InvoiceDate,
    \"Formula Stock\".\"Production Date\" AS BatchUp_Date
    FROM \"Formula Stock\"
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
    \"Formula Stock Usage\".\"Last Updated\" AS LastUpdated
    FROM \"Formula Stock Usage\"
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
    \"Sales Order\".\"Last Updated\" AS LastUpdated
    FROM \"Sales Order\"
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
    \"Sales Order Item\".\"Required Date\" AS RequiredDate
    FROM \"Sales Order Item\"
    """

#----------------------------------------------------------------------------#
# Sales Order Additional Table
#----------------------------------------------------------------------------#
sales_order_additional = """
    SELECT
    \"Sales Order Additional\".Parent,
    \"Sales Order Additional\".Description AS Haulier
    FROM \"Sales Order Additional\"
    """

#----------------------------------------------------------------------------#
# Sales Order DespatchTable
#----------------------------------------------------------------------------#
sales_order_despatch = """
    SELECT
    \"Sales Order Despatch\".Key,
    \"Sales Order Despatch\".\"Stock Code\" AS StockCode,
    \"Sales Order Despatch\".Batch AS BatchDespatched,
    \"Sales Order Despatch\".Quantity AS DespatchedQuantity
    FROM \"Sales Order Despatch\"
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
    \"Missing Order Number\".DateTime AS LastUpdated
    FROM \"Missing Order Number\"
    WHERE \"Missing Order Number\".Key > '1'
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
    \"Additional Items\".\"Last Updated\" AS LastUpdated
    FROM \"Additional Items\"
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
    Customer.\"Last Updated\" AS LastUpdated
    FROM Customer
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
    Depot.\"Last Updated\" AS LastUpdated
    FROM Depot
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
    Contact.\"Last Updated\" AS LastUpdated
    FROM Contact
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
    Supplier.\"Last Updated\" AS LastUpdated
    FROM Supplier
    ORDER BY Supplier.ID
    """

