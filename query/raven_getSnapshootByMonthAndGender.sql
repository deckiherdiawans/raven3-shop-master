if OBJECT_ID('raven_getSnapshootByMonthAndGender') is NOT NULL
drop table [raven_getSnapshootByMonthAndGender]
CREATE TABLE raven_getSnapshootByMonthAndGender (
		-- brandInit VARCHAR(64) COLLATE DATABASE_DEFAULT
		-- ,  brandName VARCHAR(128)
		sex VARCHAR(128)
		, SaleQty FLOAT 
		, saleValue money 
		, inventoryQty FLOAT 
		, inventoryValue money 
)

INSERT INTO raven_getSnapshootByMonthAndGender(sex, SaleQty, saleValue, inventoryQty, inventoryValue)
SELECT distinct a.sex,0,0,0,0 FROM tInvArticle a


--cashier
IF EXISTS ( SELECT * FROM tCashier a WHERE DATEDIFF(m,'2020-09-01',a.dateTrans) = 0 )
BEGIN
	UPDATE raven_getSnapshootByMonthAndGender
	SET
	    SaleQty = SaleQty + isnull(ole.qty,0) ,
	    saleValue = saleValue + isnull(ole.totalValue,0)
	FROM (
		SELECT c.sex, isnull(SUM(b.qty),0) AS qty, isnull(SUM(b.subTotal),0)AS  totalValue
		FROM tCashier a
		INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
		INNER JOIN tInvArticle c ON c.ArticleCode = b.ArticleCode
		WHERE DATEDIFF(m,'2020-09-01',a.dateTrans) = 0
		GROUP BY c.sex
	) ole	
	WHERE raven_getSnapshootByMonthAndGender.sex = ole.sex
END

--wholesale
IF EXISTS ( SELECT * FROM tShopWholeSale a WHERE DATEDIFF(m,'2020-09-01',a.dateTrans) = 0 )
BEGIN
	UPDATE raven_getSnapshootByMonthAndGender
	SET
	    SaleQty = SaleQty + isnull(ole.qty,0) ,
	    saleValue = saleValue + isnull(ole.totalValue,0)
	FROM (
		SELECT c.sex, isnull(SUM(b.qty),0) AS qty, isnull(SUM(b.subTotal),0)AS  totalValue
		FROM tShopWholeSale a
		INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
		INNER JOIN tInvArticle c ON c.ArticleCode = b.ArticleCode
		WHERE DATEDIFF(m,'2020-09-01',a.dateTrans) = 0
		GROUP BY c.sex
	) ole	
	WHERE raven_getSnapshootByMonthAndGender.sex = ole.sex
END

--online

IF EXISTS ( SELECT * FROM tOnline_Cashier a WHERE DATEDIFF(m,'2020-09-01',a.dateTrans) = 0 )
BEGIN
	UPDATE raven_getSnapshootByMonthAndGender
	SET
	    SaleQty = SaleQty + isnull(ole.qty,0) ,
	    saleValue = saleValue + isnull(ole.totalValue,0)
	FROM (
		SELECT c.sex, isnull(SUM(b.qty),0) AS qty, isnull(SUM(b.subTotal),0)AS  totalValue
		FROM tOnline_Cashier a
		INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
		INNER JOIN tInvArticle c ON c.ArticleCode = b.ArticleCode
		WHERE DATEDIFF(m,'2020-09-01',a.dateTrans) = 0
		GROUP BY c.sex
	) ole	
	WHERE raven_getSnapshootByMonthAndGender.sex = ole.sex
END


UPDATE raven_getSnapshootByMonthAndGender
	SET
	    inventoryQty = SaleQty + isnull(ole.qty,0) ,
	    inventoryValue = saleValue + isnull(ole.totalValue,0)
	FROM (
		SELECT a.sex, isnull(SUM(b.qty),0) AS qty, isnull(SUM(b.qty * b.CurrentSalePrice),0)AS  totalValue
		FROM tInvArticle a
		INNER JOIN tInventory b ON b.articleCode = a.articleCode
		GROUP BY a.sex
	) ole	
	WHERE raven_getSnapshootByMonthAndGender.sex = ole.sex


SELECT
CASE
	WHEN sex = 'U' THEN 'UNISEX'
	WHEN sex = 'M' THEN 'MALE'
	WHEN sex = 'F' THEN 'FEMALE'
END, SaleQty, saleValue, inventoryQty, inventoryValue
FROM raven_getSnapshootByMonthAndGender
WHERE SaleQty > 0
AND  inventoryQty > 0