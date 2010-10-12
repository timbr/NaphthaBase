""" sql.py  -- Contains Sql queries for R&R Access DB and Naphthabase.
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

#Purchase Order Selection (R&R Database)
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

#Purchase Order Selection (NaphthaBase)
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
