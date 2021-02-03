from helpers.database import Database
from helpers.postgresql import Postgre
from helpers.views import (
    view_summary_quarter4,
    view_no_data,
)
from helpers.number_format import (
    qty_format,
    value_format,
    sales_value_percentage_format,
    sell_thru_rate_format,
)


def summary_quarter4(yg, yh, dt):
    db = Database()
    conn = db.koneksi()
    cursor = conn.cursor()

    cursor.execute(
        """
        IF EXISTS (
            SELECT *
            FROM dbo.sysobjects
            WHERE id = OBJECT_ID(N'[raven_summaryByQuarter]')
            AND OBJECTPROPERTY(id, N'IsUserTable') = 1
        ) DROP TABLE [raven_summaryByQuarter]

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
                    WHERE c.dateTrans BETWEEN ? AND GETDATE()
                    GROUP BY c.barcode
                ) invhistory
                ON b.barcode = invhistory.barcode
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
                WHERE a.dateTrans BETWEEN ? AND ?
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
                WHERE a.dateTrans BETWEEN ? AND ?
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
                WHERE a.dateTrans BETWEEN ? AND ?
            ) ole
        """,
        dt,
        yg,
        yh,
        yg,
        yh,
        yg,
        yh,
    )

    cursor.execute(
        """
        SELECT a.SaleQty, a.saleValue, isnull(a.Inventoryqty, 0) as Inventoryqty, isnull(a.InventoryValue, 0) as InventoryValue 
        FROM raven_summaryByQuarter a
        """
    )

    dbResult = cursor.fetchall()
    getData = dbResult[0]
    data1 = getData[0]
    data2 = getData[1]
    data3 = getData[2]
    data4 = getData[3]

    pg = Postgre()
    pgconn = pg.connection()
    pgcursor = pgconn.cursor()

    query = """
        DROP TABLE IF EXISTS raven_SummaryByQuarter;

        CREATE TABLE raven_summaryByQuarter (
            SaleQty FLOAT,
            SaleValue FLOAT,
            InventoryQty FLOAT,
            InventoryValue FLOAT
        );

        INSERT INTO raven_summaryByQuarter (SaleQty, SaleValue, InventoryQty, InventoryValue) VALUES (%s, %s, %s, %s);

        SELECT SaleQty, SaleValue::numeric, COALESCE(InventoryQty, 0) AS InventoryQty, COALESCE(InventoryValue::numeric, 0) AS InventoryValue
        FROM raven_summaryByQuarter;

        """

    values = (data1, data2, data3, data4)

    pgcursor.execute(query, values)
    pgconn.commit()
    result = pgcursor.fetchall()

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {"title": "Quarter 4 Sales<br>(October, November, December)"}

    # AMBIL BARIS PERTAMA KARENA HASIL DARI RETURN CUMAN SATU BARIS
    result = result[0]

    # JIKA DATA TIDAK NOL
    total_data = len(result)

    if total_data > 0 and result[0] > 0:
        # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
        sale_qty = result[0]
        sale_value = result[1]
        inventory_qty = result[2]
        inventory_value = result[3]

        # FORMAT TAMPILAN DATA
        sale_qty = qty_format(sale_qty)
        sale_value = value_format(sale_value)
        inventory_qty = qty_format(inventory_qty)
        inventory_value = value_format(inventory_value)

        # MASUKAN DATA KE ARRAY RECORDS
        data["records"] = [
            ["Sales Qty", sale_qty],
            ["Sales Value", sale_value],
            ["Inventory Qty", inventory_qty],
            ["Inventory Value", inventory_value],
        ]

        return view_summary_quarter4(data)
    else:
        return view_no_data(data["title"])