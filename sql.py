""" sql.py  -- Contains Sql queries for R&R Access DB and NaphthaBase.
"""

# Table Creation
create_material_table = """
    CREATE TABLE Material (
    Code text,
    Description text,
    LastUpdated date,
    RecordNo int
    )
    """

create_purchases_table = """
    CREATE TABLE Purchases (
    PO_Num text,
    Code text,
    Batch text,
    Quantity text,
    Price text,
    OrderValue text,
    Supplier text,
    OrderReference text,
    OrderDate date,
    DueDate date,
    PlacedBy text,
    DeliveredQuantity text,
    PrintedComment text,
    DeliveryComment text,
    Status int,
    LastUpdated date
    )
    """

create_stock_table = """
    CREATE TABLE Stock (
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
    Customer text,
    WONumber text,
    Price text,
    UsageReference text,
    StockAction text,
    ItemOrder text,
    QuantityMovement text,
    UserID text,
    LastUpdated date,
    InvoiceDate date,
    BatchUp_Date date
    )
    """

create_sales_table = """
    CREATE TABLE Sales (
    WO_Num text,
    Link text,
    StockCode text,
    CustomerKey text,
    CustomerOrderNumber text,
    DespatchNotes text,
    OrderQuantity text,
    Price text,
    OrderValue text,
    Status int,
    OrderDate date,
    RequiredDate date,
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
    Haulier text,
    BatchDespatched text,
    DespatchedQuantity text,
    LastUpdated date
    )
    """

create_hauliers_table = """
    CREATE TABLE Hauliers (
    HaulierKey text,
    Name text,
    NominalCode text
    )
    """

# Material Selection (R&R Database)
material_codes = """
    SELECT
    Formula.Key AS Code,
    Formula.Description,
    Formula.\"Last Updated\" AS LastUpdated,
    Formula.\"Record Number\" AS RecordNo
    FROM Formula
    WHERE (Formula.\"Customer Key\"='ANY')
    ORDER BY Formula.Key
    """
                 
# Clear Material Table (NaphthaBase)
clear_material_table = """
    DELETE FROM Material
    """

# Purchase Order Selection (R&R Database)
po_data = """
    SELECT
    \"Purchase Order\".\"Order Number\" AS PO_Num,
    \"Purchase Item\".\"Component Code\" AS Code,
    \"Formula Stock\".Batch,
    \"Purchase Item\".Quantity,
    \"Purchase Item\".Price,
    \"Purchase Order\".\"Order Value\" AS OrderValue,
    \"Purchase Order\".Supplier,
    \"Purchase Order\".\"Order Reference\" AS OrderReference,
    \"Purchase Order\".\"Order Date\" AS OrderDate,
    \"Purchase Item\".\"Due Date\" AS DueDate,
    \"Purchase Order\".\"Placed By\" AS PlacedBy,
    \"Purchase Item\".\"Delivered Quantity\" AS DeliveredQuantity,
    \"Purchase Order\".\"Printed Comment\" AS PrintedComment,
    \"Purchase Order\".\"Delivery Comment\" As DeliveryComment,
    \"Purchase Order\".Status,
    \"Purchase Item\".\"Last Updated\" AS LastUpdated       
    FROM (\"Purchase Order\" INNER JOIN \"Purchase Item\" ON
    \"Purchase Order\".\"Order Number\" = 
    \"Purchase Item\".\"Order Number\") LEFT JOIN \"Formula Stock\" ON
    (\"Purchase Item\".\"Component Code\" = \"Formula Stock\".Key) AND 
    (\"Purchase Item\".\"Order Number\" = \"Formula Stock\".PON)       
    ORDER BY \"Purchase Order\".\"Order Number\"
    """

# Purchase Order Selection (NaphthaBase)
purchase_orders = """
    SELECT
    PO_Num,
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
        PO_Num = %(po_num)s)
    WHERE PO_Num = %(po_num)s and LastUpdated = latest
    ORDER BY Code
    """


# Clear Purchase Orders Table (NaphthaBase)
clear_po_table = """
    DELETE FROM Purchases
    """             

# Stock Selection (R&R Database)
get_stock = """
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
    \"Formula Stock Usage\".Customer,
    \"Formula Stock Usage\".\"Works order Number\" AS WONumber,
    \"Formula Stock Usage\".Price,
    \"Formula Stock Usage\".\"Usage Reference\" AS UsageReference,
    \"Formula Stock Usage\".\"Record Type\" AS StockAction,
    \"Formula Stock Usage\".\"Item Order\" AS ItemOrder,
    \"Formula Stock Usage\".Quantity AS QuantityMovement,
    \"Formula Stock Usage\".\"User ID\" AS UserID,
    \"Formula Stock Usage\".\"Last Updated\" AS LastUpdated,
    \"Formula Stock\".\"Last Updated\" AS InvoiceDate,
    \"Formula Stock\".\"Production Date\" AS BatchUp_Date
    FROM \"Formula Stock\", \"Formula Stock Usage\"
    WHERE \"Formula Stock\".Batch = \"Formula Stock Usage\".Batch
    ORDER BY \"Formula Stock\".Batch,
    \"Formula Stock Usage\".\"Last Updated\"
    """

# Stock Selection (NaphthaBase)
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
    WHERE Batch = %(batch_num)s
    """
    
# Clear Stock Table (NaphthaBase)
clear_stock_table = """
    DELETE FROM Stock
    """


# Sales Order Selection (R&R Database)
get_sales = """
    SELECT
    \"Sales Order\".Key AS WO_Num,
    \"Sales Order\".Link,
    \"Sales Order Item\".\"Stock Code\" AS StockCode,
    \"Sales Order\".CustomerKey,
    \"Sales Order\".\"Customer Order Number\" AS CustomerOrderNumber,
    \"Sales Order\".Comment AS DespatchNotes,
    \"Sales Order Item\".Quantity AS OrderQuantity,
    \"Sales Order Item\".Price,
    \"Sales Order\".\"Order Value\" AS OrderValue,
    \"Sales Order\".Status,
    \"Sales Order\".\"Order Date\" AS OrderDate,
    \"Sales Order Item\".\"Required Date\" AS RequiredDate,
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
    \"Sales Order Additional\".Description AS Haulier,
    \"Sales Order Despatch\".Batch AS BatchDespatched,
    \"Sales Order Despatch\".Quantity AS DespatchedQuantity,
    \"Sales Order\".\"Last Updated\" AS LastUpdated
    FROM ((\"Sales Order\" LEFT JOIN \"Sales Order Additional\" ON
    \"Sales Order\".Key = \"Sales Order Additional\".Parent) LEFT JOIN
    \"Sales Order Despatch\" ON
    \"Sales Order\".Key = \"Sales Order Despatch\".Key) LEFT JOIN
    \"Sales Order Item\" ON \"Sales Order\".Key = \"Sales Order Item\".Parent
    """

# Sales Order Selection (NaphthaBase)
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
        WO_Num = %(wo_num)s)
    WHERE WO_Num = %(wo_num)s and LastUpdated = latest
    ORDER BY WO_Num
    """

# Clear Sales Table (NaphthaBase)
clear_sales_table = """
    DELETE FROM Sales
    """


# Hauliers Selection (R&R Database)
get_hauliers = """
    SELECT
    \"Additional Items\".Key AS HaulierKey,
    \"Additional Items\".Name,
    \"Additional Items\".\"Nominal Code\" AS NominalCode
    FROM \"Additional Items\"
    ORDER BY \"Additional Items\".\"Record Number\"
    """
                 
# Clear Hauliers Table (NaphthaBase)
clear_hauliers_table = """
    DELETE FROM Hauliers
    """