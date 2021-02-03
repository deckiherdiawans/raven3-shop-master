import pyodbc as py

conn = py.connect("DSN=DBBLOODS-SHOP_v47;uid=revota;pwd=r3vot4", autocommit=True)
cursor = conn.cursor()

cursor.execute(
    """
    IF EXISTS (
        SELECT *
        FROM dbo.sysobjects
        WHERE id = OBJECT_ID(N'[raven_summaryByQuarter]')
        AND OBJECTPROPERTY(id, N'IsUserTable') = 1
    ) drop table [raven_summaryByQuarter]

    CREATE TABLE raven_summaryByQuarter (
        SaleQty FLOAT,
        saleValue MONEY,
        Inventoryqty FLOAT,
        InventoryValue MONEY
    )

    INSERT INTO raven_summaryByQuarter(SaleQty, saleValue, Inventoryqty, InventoryValue)
    SELECT 0,0,0,0

    UPDATE raven_summaryByQuarter
    SET Inventoryqty = ole.qty,
        InventoryValue = ole.totalSalePrice
    FROM
        (
            SELECT SUM(ISNULL(b.qty,0) - ISNULL(invhistory.qty,0)) AS qty, SUM((ISNULL(b.qty,0) * ISNULL(b.currentsalePrice,0)) - ISNULL(invhistory.salePrice,0)) AS totalSalePrice
            FROM tInvArticle a
            INNER JOIN tInventory b ON b.articleCode = a.articleCode
            LEFT JOIN 
            (
                SELECT c.barcode, SUM(c.qty * c.transtype) AS qty, SUM(c.qty * c.transtype * c.salePrice) AS salePrice
                FROM tInvHistory c
                WHERE c.dateTrans BETWEEN '2020-04-01 00:00:00 ' AND GETDATE()
                GROUP BY c.barcode
            ) invhistory
            ON b.barcode = invhistory.barcode
        ) ole

    --cashier
    UPDATE raven_summaryByQuarter
    SET SaleQty = SaleQty + ISNULL(ole.qty,0) ,
        saleValue = saleValue + ISNULL(ole.totalValue,0)
    FROM
        (
            SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
            FROM tCashier a
            INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
            WHERE a.dateTrans BETWEEN '2020-01-01 00:00:00' AND '2020-04-01 00:00:00'
        ) ole

    --wholesale
    UPDATE raven_summaryByQuarter
    SET SaleQty = SaleQty + ISNULL(ole.qty,0) ,
        saleValue = saleValue + ISNULL(ole.totalValue,0)
    FROM
        (
            SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
            FROM tShopWholeSale a
            INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
            WHERE a.dateTrans BETWEEN '2020-01-01 00:00:00' AND '2020-04-01 00:00:00'
        ) ole

    --online
    UPDATE raven_summaryByQuarter
    SET SaleQty = SaleQty + ISNULL(ole.qty,0) ,
        saleValue = saleValue + ISNULL(ole.totalValue,0)
    FROM
        (
            SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
            FROM tOnline_Cashier a
            INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
            WHERE a.dateTrans BETWEEN '2020-01-01 00:00:00' AND '2020-04-01 00:00:00'
        ) ole
    """
)

cursor.execute(
    """
    SELECT a.SaleQty, a.saleValue, ISNULL(a.Inventoryqty, 0) as Inventoryqty, ISNULL(a.InventoryValue, 0) as InventoryValue 
    FROM raven_summaryByQuarter a
    """
)
dbResult = cursor.fetchall()
result = dbResult[0]
print(result[1])