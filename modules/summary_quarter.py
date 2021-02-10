from helpers.database import Database
from helpers.postgresql import Postgre
from helpers.views import (
    view_summary_monthly,
    view_summary_quarter,
    view_no_data,
)
from helpers.number_format import (
    qty_format,
    value_format,
    sales_value_percentage_format,
    sell_thru_rate_format,
)


def summary_quarter(year, quarter):
    # show all the quarters in this condition
    if quarter == "" or quarter == "q1-q4":
        # set timestamp variables for BETWEEN statement in query
        timestampA = year + "-01-01 00:00:00"
        timestampB = year + "-04-01 00:00:00"
        timestampC = year + "-04-01 00:00:00"
        timestampD = year + "-07-01 00:00:00"
        timestampE = year + "-07-01 00:00:00"
        timestampF = year + "-10-01 00:00:00"
        timestampG = year + "-10-01 00:00:00"
        timestampH = str(int(year) + 1) + "-01-01 00:00:00"

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
                rowID INT,
                SaleQty FLOAT,
                SaleValue MONEY,
                InventoryQty FLOAT,
                InventoryValue MONEY
            )

            INSERT INTO raven_summaryByQuarter(rowID, SaleQty, SaleValue, InventoryQty, InventoryValue)
            SELECT 1,0,0,0,0 UNION SELECT 2,0,0,0,0 UNION SELECT 3,0,0,0,0 UNION SELECT 4,0,0,0,0;

            UPDATE raven_summaryByQuarter
            SET InventoryQty = ole.qty,
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
            WHERE rowID = 1

            --cashier
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tCashier a
                    INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 1

            --wholesale
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tShopWholeSale a
                    INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 1

            --online
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
                    FROM tOnline_Cashier a
                    INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 1


            UPDATE raven_summaryByQuarter
            SET InventoryQty = ole.qty,
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
            WHERE rowID = 2

            --cashier
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tCashier a
                    INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 2

            --wholesale
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tShopWholeSale a
                    INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 2

            --online
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
                    FROM tOnline_Cashier a
                    INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 2


            UPDATE raven_summaryByQuarter
            SET InventoryQty = ole.qty,
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
            WHERE rowID = 3

            --cashier
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tCashier a
                    INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 3

            --wholesale
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tShopWholeSale a
                    INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 3

            --online
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
                    FROM tOnline_Cashier a
                    INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 3


            UPDATE raven_summaryByQuarter
            SET InventoryQty = ole.qty,
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
            WHERE rowID = 4

            --cashier
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tCashier a
                    INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 4

            --wholesale
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tShopWholeSale a
                    INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 4

            --online
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
                    FROM tOnline_Cashier a
                    INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            WHERE rowID = 4
            """,
            timestampB,
            timestampA,
            timestampB,
            timestampA,
            timestampB,
            timestampA,
            timestampB,
            timestampD,
            timestampC,
            timestampD,
            timestampC,
            timestampD,
            timestampC,
            timestampD,
            timestampF,
            timestampE,
            timestampF,
            timestampE,
            timestampF,
            timestampE,
            timestampF,
            timestampH,
            timestampG,
            timestampH,
            timestampG,
            timestampH,
            timestampG,
            timestampH,
        )

        cursor.execute(
            """
            SELECT a.SaleQty, a.SaleValue, ISNULL(a.InventoryQty, 0) as InventoryQty, ISNULL(a.InventoryValue, 0) as InventoryValue 
            FROM raven_summaryByQuarter a
            """
        )

        dbResult = cursor.fetchall()

        getData1 = dbResult[0]
        getData2 = dbResult[1]
        getData3 = dbResult[2]
        getData4 = dbResult[3]

        SaleQty1 = getData1[0]
        SaleValue1 = getData1[1]
        InventoryQty1 = getData1[2]
        InventoryValue1 = getData1[3]
        title1 = "Quarter 1 Sales<br>(January, February, March)"

        SaleQty2 = getData2[0]
        SaleValue2 = getData2[1]
        InventoryQty2 = getData2[2]
        InventoryValue2 = getData2[3]
        title2 = "Quarter 2 Sales<br>(April, May, June)"

        SaleQty3 = getData3[0]
        SaleValue3 = getData3[1]
        InventoryQty3 = getData3[2]
        InventoryValue3 = getData3[3]
        title3 = "Quarter 3 Sales<br>(July, August, September)"

        SaleQty4 = getData4[0]
        SaleValue4 = getData4[1]
        InventoryQty4 = getData4[2]
        InventoryValue4 = getData4[3]
        title4 = "Quarter 4 Sales<br>(October, November, December)"

        pg = Postgre()
        pgconn = pg.connection()
        pgcursor = pgconn.cursor()

        pgcursor.execute(
            """
            DROP TABLE IF EXISTS dataTemp;
            
            CREATE TABLE IF NOT EXISTS dataTemp (
                SaleQty FLOAT,
                SaleValue MONEY,
                InventoryQty FLOAT,
                InventoryValue MONEY,
                title VARCHAR,
                CreatedDate TIMESTAMP
            );

            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

            CREATE TABLE IF NOT EXISTS raven_summaryByQuarter (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
                SaleQty FLOAT,
                SaleValue MONEY,
                InventoryQty FLOAT,
                InventoryValue MONEY,
                title VARCHAR,
                CreatedDate TIMESTAMP
            );
            """
        )
        pgconn.commit()

        query = """
                INSERT INTO dataTemp (SaleQty, SaleValue, InventoryQty, InventoryValue, title, CreatedDate) VALUES (%s, %s, %s, %s, %s, NOW());

                INSERT INTO raven_summaryByQuarter (uuid, SaleQty, SaleValue, InventoryQty, InventoryValue, title, CreatedDate)
                VALUES (uuid_generate_v1(), %s, %s, %s, %s, %s, NOW());
                """
        values = [
            (
                SaleQty1,
                SaleValue1,
                InventoryQty1,
                InventoryValue1,
                title1,
                SaleQty1,
                SaleValue1,
                InventoryQty1,
                InventoryValue1,
                title1,
            ),
            (
                SaleQty2,
                SaleValue2,
                InventoryQty2,
                InventoryValue2,
                title2,
                SaleQty2,
                SaleValue2,
                InventoryQty2,
                InventoryValue2,
                title2,
            ),
            (
                SaleQty3,
                SaleValue3,
                InventoryQty3,
                InventoryValue3,
                title3,
                SaleQty3,
                SaleValue3,
                InventoryQty3,
                InventoryValue3,
                title3,
            ),
            (
                SaleQty4,
                SaleValue4,
                InventoryQty4,
                InventoryValue4,
                title4,
                SaleQty4,
                SaleValue4,
                InventoryQty4,
                InventoryValue4,
                title4,
            ),
        ]
        pgcursor.executemany(query, values)
        pgconn.commit()

        pgcursor.execute(
            """
            SELECT SaleQty, SaleValue::numeric, COALESCE(InventoryQty, 0) AS InventoryQty, COALESCE(InventoryValue::numeric, 0) AS InventoryValue, title
            FROM dataTemp a;
            """
        )
        pgconn.commit()
        result = pgcursor.fetchall()

        # JIKA DATA TIDAK NOL
        total_data = len(result)

        if total_data > 0 and result[0][0] > 0:
            # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
            sale_qty = result[0][0]
            sale_value = result[0][1]
            inventory_qty = result[0][2]
            inventory_value = result[0][3]
            title = result[0][4]
            sale_qty1 = result[1][0]
            sale_value1 = result[1][1]
            inventory_qty1 = result[1][2]
            inventory_value1 = result[1][3]
            title1 = result[1][4]
            sale_qty2 = result[2][0]
            sale_value2 = result[2][1]
            inventory_qty2 = result[2][2]
            inventory_value2 = result[2][3]
            title2 = result[2][4]
            sale_qty3 = result[3][0]
            sale_value3 = result[3][1]
            inventory_qty3 = result[3][2]
            inventory_value3 = result[3][3]
            title3 = result[3][4]

            # FORMAT TAMPILAN DATA
            sale_qty = qty_format(sale_qty)
            sale_value = value_format(sale_value)
            inventory_qty = qty_format(inventory_qty)
            inventory_value = value_format(inventory_value)
            sale_qty1 = qty_format(sale_qty1)
            sale_value1 = value_format(sale_value1)
            inventory_qty1 = qty_format(inventory_qty1)
            inventory_value1 = value_format(inventory_value1)
            sale_qty2 = qty_format(sale_qty2)
            sale_value2 = value_format(sale_value2)
            inventory_qty2 = qty_format(inventory_qty2)
            inventory_value2 = value_format(inventory_value2)
            sale_qty3 = qty_format(sale_qty3)
            sale_value3 = value_format(sale_value3)
            inventory_qty3 = qty_format(inventory_qty3)
            inventory_value3 = value_format(inventory_value3)

            # MASUKAN DATA KE ARRAY RECORDS
            data = {"title": title}
            data["records"] = [
                ["Sales Qty", sale_qty],
                ["Sales Value", sale_value],
                ["Inventory Qty", inventory_qty],
                ["Inventory Value", inventory_value],
            ]
            data1 = {"title": title1}
            data1["records"] = [
                ["Sales Qty", sale_qty1],
                ["Sales Value", sale_value1],
                ["Inventory Qty", inventory_qty1],
                ["Inventory Value", inventory_value1],
            ]
            data2 = {"title": title2}
            data2["records"] = [
                ["Sales Qty", sale_qty2],
                ["Sales Value", sale_value2],
                ["Inventory Qty", inventory_qty2],
                ["Inventory Value", inventory_value2],
            ]
            data3 = {"title": title3}
            data3["records"] = [
                ["Sales Qty", sale_qty3],
                ["Sales Value", sale_value3],
                ["Inventory Qty", inventory_qty3],
                ["Inventory Value", inventory_value3],
            ]

            # return data, data1, data2, data3
            return view_summary_quarter(data, data1, data2, data3)
        else:
            return view_no_data(data["title"])
    else:
        # show one quarter as requested on URL
        # using quarter element from URL as condition to set the timestamp variables for BETWEEN statement in query
        if quarter == "q1":
            timestampA = year + "-01-01 00:00:00"
            timestampB = year + "-04-01 00:00:00"
            data = {"title": "Quarter 1 Sales<br>(January, February, March)"}
        elif quarter == "q2":
            timestampA = year + "-04-01 00:00:00"
            timestampB = year + "-07-01 00:00:00"
            data = {"title": "Quarter 2 Sales<br>(April, May, June)"}
        elif quarter == "q3":
            timestampA = year + "-07-01 00:00:00"
            timestampB = year + "-10-01 00:00:00"
            data = {"title": "Quarter 3 Sales<br>(July, August, September)"}
        elif quarter == "q4":
            timestampA = year + "-10-01 00:00:00"
            timestampB = str(int(year) + 1) + "-01-01 00:00:00"
            data = {"title": "Quarter 4 Sales<br>(October, November, December)"}

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
                SaleValue MONEY,
                InventoryQty FLOAT,
                InventoryValue MONEY
            )

            INSERT INTO raven_summaryByQuarter(SaleQty, SaleValue, InventoryQty, InventoryValue)
            SELECT 0,0,0,0

            UPDATE raven_summaryByQuarter
            SET InventoryQty = ole.qty,
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
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tCashier a
                    INNER JOIN tCashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole

            --wholesale
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) AS totalValue
                    FROM tShopWholeSale a
                    INNER JOIN tShopWholeSaleDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole

            --online
            UPDATE raven_summaryByQuarter
            SET SaleQty = SaleQty + ISNULL(ole.qty,0),
                SaleValue = SaleValue + ISNULL(ole.totalValue,0)
            FROM
                (
                    SELECT SUM(b.qty) AS qty, SUM(b.subTotal) totalValue
                    FROM tOnline_Cashier a
                    INNER JOIN tOnline_CashierDetail b ON b.noTrans = a.noTrans
                    WHERE a.dateTrans BETWEEN ? AND ?
                ) ole
            """,
            timestampB,
            timestampA,
            timestampB,
            timestampA,
            timestampB,
            timestampA,
            timestampB,
        )

        cursor.execute(
            """
            SELECT a.SaleQty, a.SaleValue, ISNULL(a.InventoryQty, 0) as InventoryQty, ISNULL(a.InventoryValue, 0) as InventoryValue 
            FROM raven_summaryByQuarter a
            """
        )

        dbResult = cursor.fetchall()
        getData = dbResult[0]
        SaleQty = getData[0]
        SaleValue = getData[1]
        InventoryQty = getData[2]
        InventoryValue = getData[3]
        title = "Single Quarter Request"

        pg = Postgre()
        pgconn = pg.connection()
        pgcursor = pgconn.cursor()

        pgcursor.execute(
            """
            DROP TABLE IF EXISTS dataTemp;

            CREATE TABLE IF NOT EXISTS dataTemp (
                SaleQty FLOAT,
                SaleValue MONEY,
                InventoryQty FLOAT,
                InventoryValue MONEY,
                title VARCHAR,
                CreatedDate TIMESTAMP
            );

            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

            CREATE TABLE IF NOT EXISTS raven_summaryByQuarter (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
                SaleQty FLOAT,
                SaleValue MONEY,
                InventoryQty FLOAT,
                InventoryValue MONEY,
                title VARCHAR,
                CreatedDate TIMESTAMP
            );
            """
        )
        pgconn.commit()

        query = """
                INSERT INTO dataTemp (SaleQty, SaleValue, InventoryQty, InventoryValue, title, CreatedDate) VALUES (%s, %s, %s, %s, %s, NOW());

                INSERT INTO raven_summaryByQuarter (uuid, SaleQty, SaleValue, InventoryQty, InventoryValue, title, CreatedDate)
                VALUES (uuid_generate_v1(), %s, %s, %s, %s, %s, NOW());

                SELECT SaleQty, SaleValue::numeric, COALESCE(InventoryQty, 0) AS InventoryQty, COALESCE(InventoryValue::numeric, 0) AS InventoryValue
                FROM dataTemp;
                """
        values = (
            SaleQty,
            SaleValue,
            InventoryQty,
            InventoryValue,
            title,
            SaleQty,
            SaleValue,
            InventoryQty,
            InventoryValue,
            title,
        )
        pgcursor.execute(query, values)
        pgconn.commit()
        result = pgcursor.fetchall()

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

            # return data
            return view_summary_monthly(data)
        else:
            return view_no_data(data["title"])