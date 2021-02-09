IF EXISTS (
    SELECT *
    FROM dbo.sysobjects
    WHERE id = OBJECT_ID(N'[raven_summaryByQuarter]')
    AND OBJECTPROPERTY(id, N'IsUserTable') = 1
) DROP TABLE [raven_summaryByQuarter]

CREATE TABLE raven_summaryByQuarter (
    rowID INT,
    SaleQty FLOAT,
    SaleValue MONEY,
    Inventoryqty FLOAT,
    InventoryValue MONEY
)

INSERT INTO raven_summaryByQuarter(rowID, SaleQty, SaleValue, Inventoryqty, InventoryValue)
-- SELECT 0,0,0,0
SELECT 1,0,0,0,0 UNION SELECT 2,0,0,0,0 UNION SELECT 3,0,0,0,0 UNION SELECT 4,0,0,0,0

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
            WHERE c.dateTrans BETWEEN '2019-04-01 00:00:00' AND GETDATE()
            GROUP BY c.barcode
        ) invhistory
        ON b.barcode = invhistory.barcode
    ) ole
WHERE rowID = 1

--cashier
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tCashier a
        INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-01-01 00:00:00' AND '2019-04-01 00:00:00'
    ) ole
WHERE rowID = 1

--wholesale
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tShopWholeSale a
        INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-01-01 00:00:00' AND '2019-04-01 00:00:00'
    ) ole
WHERE rowID = 1

--online
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
        FROM tOnline_Cashier a
        INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-01-01 00:00:00' AND '2019-04-01 00:00:00'
    ) ole
WHERE rowID = 1


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
            WHERE c.dateTrans BETWEEN '2019-07-01 00:00:00' AND GETDATE()
            GROUP BY c.barcode
        ) invhistory
        ON b.barcode = invhistory.barcode
    ) ole
WHERE rowID = 2

--cashier
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tCashier a
        INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-04-01 00:00:00' AND '2019-07-01 00:00:00'
    ) ole
WHERE rowID = 2

--wholesale
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tShopWholeSale a
        INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-04-01 00:00:00' AND '2019-07-01 00:00:00'
    ) ole
WHERE rowID = 2

--online
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
        FROM tOnline_Cashier a
        INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-04-01 00:00:00' AND '2019-07-01 00:00:00'
    ) ole
WHERE rowID = 2


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
            WHERE c.dateTrans BETWEEN '2019-10-01 00:00:00' AND GETDATE()
            GROUP BY c.barcode
        ) invhistory
        ON b.barcode = invhistory.barcode
    ) ole
WHERE rowID = 3

--cashier
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tCashier a
        INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-07-01 00:00:00' AND '2019-10-01 00:00:00'
    ) ole
WHERE rowID = 3

--wholesale
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tShopWholeSale a
        INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-07-01 00:00:00' AND '2019-10-01 00:00:00'
    ) ole
WHERE rowID = 3

--online
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
        FROM tOnline_Cashier a
        INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-07-01 00:00:00' AND '2019-10-01 00:00:00'
    ) ole
WHERE rowID = 3


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
            WHERE c.dateTrans BETWEEN '2020-01-01 00:00:00' AND GETDATE()
            GROUP BY c.barcode
        ) invhistory
        ON b.barcode = invhistory.barcode
    ) ole
WHERE rowID = 4

--cashier
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tCashier a
        INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-10-01 00:00:00' AND '2020-01-01 00:00:00'
    ) ole
WHERE rowID = 4

--wholesale
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tShopWholeSale a
        INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-10-01 00:00:00' AND '2020-01-01 00:00:00'
    ) ole
WHERE rowID = 4

--online
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    SaleValue = SaleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
        FROM tOnline_Cashier a
        INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
        WHERE a.dateTrans BETWEEN '2019-10-01 00:00:00' AND '2020-01-01 00:00:00'
    ) ole
WHERE rowID = 4


SELECT rowID, a.SaleQty, a.SaleValue, isnull(a.Inventoryqty, 0) as Inventoryqty, isnull(a.InventoryValue, 0) as InventoryValue 
FROM raven_summaryByQuarter a