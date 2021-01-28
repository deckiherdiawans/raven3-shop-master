import pyodbc
from helpers.database import Database
from helpers.query import executeQuery
from helpers.views import (
    view_summary_monthly,
    view_no_data,
)
from helpers.number_format import (
    qty_format,
    value_format,
    sales_value_percentage_format,
    sell_thru_rate_format,
)


def summary_monthly(date):
    try:
        # AMBIL DATA DARI STORED PROCEDURE DAN HITUNG JUMLAH DATANYA
        result = executeQuery("raven_getSnapshootByMonth '%s'" % date)
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]

        db = Database()
        conn = db.koneksi()
        cursor = conn.cursor()

        cursor.execute(
            """
            if exists (
                select
                    *
                from
                    dbo.sysobjects
                where
                    id = object_id(N'[Raven_summaryByMonth]')
                    and OBJECTPROPERTY(id, N'IsUserTable') = 1
            ) drop table [Raven_summaryByMonth]

            CREATE TABLE Raven_summaryByMonth (
                dateTrans DATETIME,
                SaleQty FLOAT,
                saleValue money,
                Inventoryqty float,
                InventoryValue money
            )

            INSERT INTO Raven_summaryByMonth(dateTrans, SaleQty, saleValue, Inventoryqty, InventoryValue)
            SELECT ?,0,0,0,0
            
            UPDATE Raven_summaryByMonth
            SET Inventoryqty = ole.qty,
                InventoryValue = ole.totalSalePrice
            FROM
                (
                SELECT ? AS dateTrans, SUM(b.qty) AS qty, SUM(b.qty*b.CurrentSalePrice) AS totalSalePrice
                FROM tInvArticle a
                INNER JOIN tInventory b ON b.articleCode = a.articleCode
                ) ole
            WHERE DATEDIFF(m,ole.dateTrans,Raven_summaryByMonth.dateTrans) = 0

            --cashier
            UPDATE Raven_summaryByMonth
            SET SaleQty = SaleQty + isnull(ole.qty,0) ,
                saleValue = saleValue + isnull(ole.totalValue,0)
            FROM
                (
                    SELECT ? AS dateTrans,SUM(b.qty) AS qty, SUM(b.subTotal)AS  totalValue
                    FROM tCashier a
                    INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
                    WHERE DATEDIFF(m,?,a.dateTrans) = 0
                ) ole
            WHERE DATEDIFF(m,ole.dateTrans,Raven_summaryByMonth.dateTrans) = 0

            --wholesale
            UPDATE Raven_summaryByMonth
            SET SaleQty = SaleQty + isnull(ole.qty,0) ,
                saleValue = saleValue + isnull(ole.totalValue,0)
            FROM
                (
                    SELECT ? AS dateTrans, SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tShopWholeSale a
                    INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
                    WHERE DATEDIFF(m,?,a.dateTrans) = 0
                ) ole
            WHERE DATEDIFF(m,ole.dateTrans,Raven_summaryByMonth.dateTrans) = 0

            --online
            UPDATE Raven_summaryByMonth
            SET SaleQty = SaleQty + isnull(ole.qty,0) ,
                saleValue = saleValue + isnull(ole.totalValue,0)
            FROM
                (
                    SELECT ? AS dateTrans,SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
                    FROM tOnline_Cashier a
                    INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
                    WHERE DATEDIFF(m,?,a.dateTrans) = 0
                ) ole
            WHERE DATEDIFF(m,ole.dateTrans,Raven_summaryByMonth.dateTrans) = 0
            """,
            date,
            date,
            date,
            date,
            date,
            date,
            date,
            date,
        )

        cursor.execute(
            """
            SELECT a.SaleQty, a.saleValue, isnull(a.Inventoryqty, 0) as Inventoryqty, isnull(a.InventoryValue, 0) as InventoryValue 
            FROM Raven_summaryByMonth a
            """
        )
        result = cursor.fetchall()

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {"title": "Monthly Sales"}

    # AMBIL BARIS PERTAMA KARENA HASIL DARI RETURN CUMAN SATU BARIS
    result = result[0]

    # JIKA DATA TIDAK NOL
    total_data = len(result)

    if total_data > 0 and result[1] > 0:
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

        return view_summary_monthly(data)
    else:
        return view_no_data(data["title"])