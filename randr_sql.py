"""randr_sql.py  -- Contains Sql queries for R&R and NaphthaBase databases.

Routines for cloning the R&R database and updating to the Naphthabase with a
revision history.
"""

tables = ['Formula', 'Purchase_Order', 'Purchase_Item', 'Formula_Stock',
          'Formula_Stock_Usage', 'Sales_Order', 'Sales_Order_Item',
          'Sales_Order_Additional', 'Sales_Order_Despatch',
          'Missing_Order_Numbers', 'Additional_Items', 'Customer', 'Depot',
          'Contact', 'Supplier']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#----------------------------------------------------------------------------#
# Formula Table (R&R Database)
#----------------------------------------------------------------------------#
Formula = """
    SELECT
    Formula.Key AS Code,
    Formula.Description,
    Formula.\"Last Updated\" AS LastUpdated,
    Formula.\"Record Number\" AS RecordNum
    FROM Formula
    WHERE (Formula.\"Customer Key\"='ANY')
    AND Formula.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Formula.Key
    """

#----------------------------------------------------------------------------#
# Create Clone of Formula Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_formula = """
    CREATE TABLE Formula (
    Code text,
    Description text,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Purchase Order Table (R&R Database)
#----------------------------------------------------------------------------#
Purchase_Order = """
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
    \"Purchase Order\".\"Record Number\" AS RecordNum
    FROM \"Purchase Order\"
    WHERE \"Purchase Order\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Purchase Order\".\"Order Number\"
    """

#----------------------------------------------------------------------------#
# Create Clone of Purchase Order Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_purchase_order = """
    CREATE TABLE Purchase_Order (
    PO_Num text,
    OrderValue text,
    Supplier text,
    OrderReference text,
    OrderDate text,
    PlacedBy text,
    PrintedComment text,
    DeliveryComment text,
    Status text,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Purchase Item Table (R&R Database)
#----------------------------------------------------------------------------#
Purchase_Item = """
    SELECT
    \"Purchase Item\".\"Component Code\" AS Code,
    \"Purchase Item\".Quantity,
    \"Purchase Item\".Price,
    \"Purchase Item\".\"Due Date\" AS DueDate,
    \"Purchase Item\".\"Delivered Quantity\" AS DeliveredQuantity,
    \"Purchase Item\".\"Last Updated\" AS LastUpdated,
    \"Purchase Item\".\"Record Number\" AS RecordNum
    FROM (\"Purchase Item\"
    WHERE \"Purchase Item\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Purchase Item\".\"Record Number\"
    """

#----------------------------------------------------------------------------#
# Create Clone of Purchase Item Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_purchase_item = """
    CREATE TABLE Purchase_Item (
    Code text,
    Quantity text,
    Price text,
    DueDate date,
    DeliveredQuantity text,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """
#****************************************************************************#

#----------------------------------------------------------------------------#
# Formula Stock Table (R&R Database)
#----------------------------------------------------------------------------#
Formula_Stock = """
    SELECT
    \"Formula Stock\".Batch,
    \"Formula Stock Usage\".Formula AS Code,
    \"Formula Stock Usage\".Revision,
    \"Formula Stock\".Type AS BatchStatus,
    \"Formula Stock\".Quantity AS QuantityNow,
    \"Formula Stock\".\"Original Quantity\" AS OriginalDeliveredQuantity,
    \"Formula Stock\".Location AS StockInfo,
    \"Formula Stock\".Supplier,
    \"Formula Stock\".PON AS PONumber,
    \"Formula Stock\".Cost AS PurchaseCost,
    \"Formula Stock\".\"Last Updated\" AS LastUpdated,
    \"Formula Stock\".\"Production Date\" AS BatchUp_Date,
    \"Formula Stock\".\"Record Number\" AS RecordNum
    FROM \"Formula Stock\"
    WHERE \"Formula Stock\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Formula Stock\".Batch
    """

#----------------------------------------------------------------------------#
# Create Clone of Formula Stock Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_formula_stock = """
    CREATE TABLE Formula_Stock (
    Batch text,
    Code text,
    Revision text,
    BatchStatus text,
    QuantityNow text,
    OriginalDeliveredQuantity text,
    StockInfo text,
    Supplier text,
    PONumber text,
    PurchaseCost text,
    LastUpdated date,
    BatchUp_Date date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Formula Stock Usage Table (R&R Database)
#----------------------------------------------------------------------------#
Formula_Stock_Usage = """
    SELECT
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
    \"Formula Stock Usage\".\"Record Number\" AS RecordNum
    FROM \"Formula Stock Usage\"
    WHERE \"Formula Stock Usage\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Formula Stock Usage\".\"Last Updated\"
    """

#----------------------------------------------------------------------------#
# Create Clone of Formula Stock Usage Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_formula_stock_usage = """
    CREATE TABLE Formula_Stock_Usage (
    Code text,
    Revision text,
    Customer text,
    WONumber text,
    Price text,
    UsageReference text,
    StockAction text,
    ItemOrder text,
    QuantityMovement text,
    UserID text,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Sales Order Table(R&R Database)
#----------------------------------------------------------------------------#
Sales_Order = """
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
    \"Sales Order\".\"Record Number\" AS RecordNum
    FROM \"Sales Order\"
    WHERE \"Sales Order\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Create Clone of Sales Order Table(NaphthaBase)
#----------------------------------------------------------------------------#
clone_sales_order = """
    CREATE TABLE Sales_Order (
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
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Sales Order Item Table (R&R Database)
#----------------------------------------------------------------------------#
Sales_Order_Item = """
    SELECT
    \"Sales Order Item\".Parent,
    \"Sales Order Item\".\"Stock Code\" AS StockCode,
    \"Sales Order Item\".Quantity AS OrderQuantity,
    \"Sales Order Item\".Price,
    \"Sales Order Item\".\"Required Date\" AS RequiredDate,
    \"Sales Order Item\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Item\".\"Record Number\" AS RecordNum
    FROM \"Sales Order Item\"
    WHERE \"Sales Order Item\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Clone of Sales Order Item Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_sales_order_item = """
    CREATE TABLE Sales_Order_Item (
    Parent text,
    StockCode text,
    OrderQuantity text,
    Price text,
    RequiredDate date,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Sales Order Additional Table(R&R Database)
#----------------------------------------------------------------------------#
Sales_Order_Additional = """
    SELECT
    \"Sales Order Additional\".Parent AS WO_Num,
    \"Sales Order Additional\".Description AS Haulier,
    \"Sales Order Additional\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Additional\".\"Record Number\" AS RecordNum
    FROM "Sales Order Additional\"
    WHERE \"Sales Order Additional\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Clone of Sales Order Additional Table(NaphthaBase)
#----------------------------------------------------------------------------#
clone_sales_order_additional = """
    CREATE TABLE Sales_Order_Additional (
    WO_Num text,
    Haulier text,
    LastUpdated text,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Sales Order Despatch (R&R Database)
#----------------------------------------------------------------------------#
Sales_Order_Despatch = """
    SELECT
    \"Sales Order Despatch\".Key,
    \"Sales Order Despatch\".\"Stock Code\" AS StockCode,
    \"Sales Order Despatch\".Batch AS BatchDespatched,
    \"Sales Order Despatch\".Quantity AS DespatchedQuantity,
    \"Sales Order Despatch\".\"Last Updated\" AS LastUpdated
    \"Sales Order Despatch\".\"Record Number\" AS RecordNum
    FROM \"Sales Order Despatch\"    
    WHERE \"Sales Order Despatch\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Clone of Sales Order Despatch Table(NaphthaBase)
#----------------------------------------------------------------------------#
clone_sales_order_despatch = """
    CREATE TABLE Sales_Order_Despatch (
    Key text,
    StockCode text,
    BatchDespatched text,
    DespatchedQuantity text,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Missing Order Numbers Table(R&R Database)
#----------------------------------------------------------------------------#
Missing_Order_Numbers = """
    SELECT
    \"Missing Order Number\".Key AS WO_Num,
    \"Missing Order Number\".\"User ID\" AS UserID,
    \"Missing Order Number\".Reason AS Reason,
    \"Missing Order Number\".DateTime AS LastUpdated,
    \"Missing Order Number\".\"Record Number\" AS RecordNum
    FROM \"Missing Order Number\"
    WHERE \"Missing Order Number\".Key > '1'
    AND \"Missing Order Number\".DateTime > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Clone of Missing Order Numbers Table(NaphthaBase)
#----------------------------------------------------------------------------#
clone_missing_order_numbers = """
    CREATE TABLE Missing_Order_Numbers (
    WO_Num text,
    UserID text,
    Reason text,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Additional Items Table (R&R Database)
#----------------------------------------------------------------------------#
Additional_Items = """
    SELECT
    \"Additional Items\".Key AS HaulierKey,
    \"Additional Items\".Name,
    \"Additional Items\".\"Nominal Code\" AS NominalCode,
    \"Additional Items\".\"Last Updated\" AS LastUpdated,
    \"Additional Items\".\"Record Number\" AS RecordNum
    FROM \"Additional Items\"
    WHERE \"Additional Items\".\"Last Updated\" > #%(lastupdate)s#
    ORDER BY \"Additional Items\".\"Record Number\"
    """

#----------------------------------------------------------------------------#
# Clone Additional Items Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_additional_items = """
    CREATE TABLE Additional_Items (
    HaulierKey text,
    Name text,
    NominalCode text,
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Customer Table (R&R Database)
#----------------------------------------------------------------------------#
Customer = """
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
    Customer.\"Record Number\" AS RecordNum
    FROM Customer
    WHERE Customer.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Customer.ID
    """

#----------------------------------------------------------------------------#
# Clone of Customer Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_customer = """
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
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Depot Table(R&R Database)
#----------------------------------------------------------------------------#
Depot = """
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
    Depot.\"Record Number\" AS RecordNum
    FROM Depot
    WHERE Depot.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Depot.\"Client ID\"
    """

#----------------------------------------------------------------------------#
# Clone of Depot Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_depot = """
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
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Contact Table(R&R Database)
#----------------------------------------------------------------------------#
Contact = """
    SELECT
    Contact.\"Client ID\" AS ClientID,
    Contact.Title,
    Contact.Forename,
    Contact.Surname,
    Contact.Phone,
    Contact.Department,
    Contact.\"Last Updated\" AS LastUpdated,
    Contact.\"Record Number\" AS RecordNum
    FROM Contact
    WHERE Contact.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Contact.\"Client ID\"
    """

#----------------------------------------------------------------------------#
# Clone of Contact Table(NaphthaBase)
#----------------------------------------------------------------------------#
clone_contact = """
    CREATE TABLE Contact (
    ClientID text,
    Title text,
    Forename text,
    Surname text,
    Phone text,
    Department text,
    LastUpdated text,
    RecordNum int,
    Priority int
    )
    """

#****************************************************************************#

#----------------------------------------------------------------------------#
# Supplier Table (R&R Database)
#----------------------------------------------------------------------------#
Supplier = """
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
    Supplier.\"Record Number\" AS RecordNum
    FROM Supplier
    WHERE Supplier.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Supplier.ID
    """

#----------------------------------------------------------------------------#
# Clone of Supplier Table (NaphthaBase)
#----------------------------------------------------------------------------#
clone_supplier = """
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
    LastUpdated date,
    RecordNum int,
    Priority int
    )
    """