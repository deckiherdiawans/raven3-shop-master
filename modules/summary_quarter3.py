from helpers.database import Database
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


def summary_quarter3(year, p5, p6):
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
                WHERE YEAR(a.dateTrans) = ?
                AND MONTH(a.dateTrans) BETWEEN ? AND ?
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
                WHERE YEAR(a.dateTrans) = ?
                AND MONTH(a.dateTrans) BETWEEN ? AND ?
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
                WHERE YEAR(a.dateTrans) = ?
                AND MONTH(a.dateTrans) BETWEEN ? AND ?
            ) ole
        """,
        year,
        p5,
        p6,
        year,
        p5,
        p6,
        year,
        p5,
        p6,
    )

    cursor.execute(
        """
        SELECT a.SaleQty, a.saleValue, isnull(a.Inventoryqty, 0) as Inventoryqty, isnull(a.InventoryValue, 0) as InventoryValue 
        FROM raven_summaryByQuarter a
        """
    )
    result = cursor.fetchall()

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {"title": "Quarter 3 Sales"}

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