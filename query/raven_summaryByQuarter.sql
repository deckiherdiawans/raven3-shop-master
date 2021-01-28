if exists (
    select
        *
    from
        dbo.sysobjects
    where
        id = object_id(N'[raven_summaryByQuarter]')
        and OBJECTPROPERTY(id, N'IsUserTable') = 1
) drop table [raven_summaryByQuarter]

CREATE TABLE raven_summaryByQuarter (
    SaleQty FLOAT,
    saleValue money,
    Inventoryqty float,
    InventoryValue money
)

INSERT INTO raven_summaryByQuarter(SaleQty, saleValue, Inventoryqty, InventoryValue)
SELECT 0,0,0,0

UPDATE raven_summaryByQuarter
SET Inventoryqty = ole.qty,
    InventoryValue = ole.totalSalePrice
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.qty*b.CurrentSalePrice) AS totalSalePrice
        FROM tInvArticle a
        INNER JOIN tInventory b ON b.articleCode = a.articleCode
    ) ole

--cashier
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    saleValue = saleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tCashier a
        INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
        WHERE YEAR(a.dateTrans) = 2020
        AND MONTH(a.dateTrans) BETWEEN 01 AND 03
    ) ole

--wholesale
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    saleValue = saleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
        FROM tShopWholeSale a
        INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
        WHERE YEAR(a.dateTrans) = 2020
        AND MONTH(a.dateTrans) BETWEEN 01 AND 03
    ) ole

--online
UPDATE raven_summaryByQuarter
SET SaleQty = SaleQty + isnull(ole.qty,0) ,
    saleValue = saleValue + isnull(ole.totalValue,0)
FROM
    (
        SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
        FROM tOnline_Cashier a
        INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
        WHERE YEAR(a.dateTrans) = 2020
        AND MONTH(a.dateTrans) BETWEEN 01 AND 03
    ) ole


SELECT a.SaleQty, a.saleValue, isnull(a.Inventoryqty, 0) as Inventoryqty, isnull(a.InventoryValue, 0) as InventoryValue 
FROM raven_summaryByQuarter a