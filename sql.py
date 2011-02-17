""" sql.py  -- Contains Sql queries for R&R Access DB.
"""

#----------------------------------------------------------------------------#
# Material Selection (R&R Database)
#----------------------------------------------------------------------------#
get_material_codes = """
    SELECT
    Formula.Key AS Material,
    Formula.Description,
    Formula.\"Minimum Stock\" AS MinimumStock,
    Formula.\"Last Updated\" AS LastUpdated,
    Formula.\"Record Number\" AS RecordNumber
    FROM Formula
    WHERE (Formula.\"Customer Key\" != 'ANY')
    AND Formula.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Formula.Key
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
# Purchase Item Selection (R&R Database)
#----------------------------------------------------------------------------#
get_purchaseitem = """
    SELECT
    \"Purchase Item\".\"Order Number\" AS PO_Num,
    \"Purchase Item\".Index,
    \"Purchase Item\".\"Component Code\" AS Material,
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
# Stock Selection (R&R Database)
#----------------------------------------------------------------------------#
get_stock = """
    SELECT
    \"Formula Stock\".Batch,
    \"Formula Stock\".Key AS Material,
    \"Formula Stock\".Location AS StockInfo,
    \"Formula Stock\".Type AS BatchStatus,
    \"Formula Stock\".Supplier,
    \"Formula Stock\".PON AS PO_Num,
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
    \"Formula Stock Usage\".\"Works Order Number\" AS WO_Num,
    \"Formula Stock Usage\".PON AS PO_Num,
    \"Formula Stock Usage\".Formula AS Material,
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
# Despatch Selection (R&R Database)
#----------------------------------------------------------------------------#
get_despatch = """
    SELECT
    \"Sales Order Despatch\".Key AS WO_Num,
    \"Sales Order Despatch\".\"Stock Code\" AS Material,
    \"Sales Order Despatch\".Batch AS BatchDespatched,
    \"Sales Order Despatch\".Quantity AS DespatchedQuantity,
    \"Sales Order Despatch\".\"Last Updated\" AS LastUpdated,
    \"Sales Order Despatch\".\"Record Number\" AS RecordNumber
    FROM \"Sales Order Despatch\"
    WHERE \"Sales Order Despatch\".\"Last Updated\" > #%(lastupdate)s#
    """

#----------------------------------------------------------------------------#
# Sales Item Selection (R&R Database)
#----------------------------------------------------------------------------#
get_salesitem = """
    SELECT
    \"Sales Order Item\".Parent AS WO_Num,
    \"Sales Order Item\".\"Stock Code\" AS Material,
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
# Sales Order Additional (R&R Database)
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

#----------------------------------------------------------------------------#
# Deleted Sales Orders (R&R Database)
#----------------------------------------------------------------------------#
get_deleted_sales = """
    SELECT
    \"Missing Order Number\".Key AS WO_Num,
    \"Missing Order Number\".\"User ID\" AS UserID,
    \"Missing Order Number\".Reason AS Reason,
    \"Missing Order Number\".DateTime AS LastUpdated,
    \"Missing Order Number\".\"Record Number\" AS RecordNumber
    FROM \"Missing Order Number\"
    WHERE (\"Missing Order Number\".Key > '1' AND
    \"Missing Order Number\".DateTime > #%(lastupdate)s#)
    """

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
    Depot.\"Record Number\" AS RecordNumber
    FROM Depot
    WHERE Depot.\"Last Updated\" > #%(lastupdate)s#
    ORDER BY Depot.\"Client ID\"
    """

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