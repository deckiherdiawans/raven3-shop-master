from helpers.database import Database
from helpers.views import (
    view_distribute,
    view_no_data,
)
from helpers.number_format import (
    qty_format,
    value_format,
    sales_value_percentage_format,
    sell_thru_rate_format,
)


def distribute_monthly_gender(date, top_limit):
    # result = executeQuery("raven_getSnapshootByMonthAndGender '%s'" % date)

    db = Database()
    conn = db.koneksi()
    cursor = conn.cursor()

    cursor.execute(
        """
        if OBJECT_ID('raven_getSnapshootByMonthAndGender') is NOT NULL
        drop table [raven_getSnapshootByMonthAndGender]
        CREATE TABLE raven_getSnapshootByMonthAndGender (
                -- sexInit VARCHAR(64) COLLATE DATABASE_DEFAULT
                -- ,  sexName VARCHAR(128)
                sex VARCHAR(128)
                , SaleQty FLOAT 
                , saleValue money
                , inventoryQty FLOAT 
                , inventoryValue money
        )

        INSERT INTO raven_getSnapshootByMonthAndGender(sex, SaleQty, saleValue, inventoryQty, inventoryValue)
        SELECT distinct a.sex,0,0,0,0 FROM tInvArticle a


        --cashier
        IF EXISTS ( SELECT * FROM tCashier a WHERE DATEDIFF(m,?,a.dateTrans) = 0 )
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
                WHERE DATEDIFF(m,?,a.dateTrans) = 0
                GROUP BY c.sex
            ) ole	
            WHERE raven_getSnapshootByMonthAndGender.sex = ole.sex
        END

        --wholesale
        IF EXISTS ( SELECT * FROM tShopWholeSale a WHERE DATEDIFF(m,?,a.dateTrans) = 0 )
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
                WHERE DATEDIFF(m,?,a.dateTrans) = 0
                GROUP BY c.sex
            ) ole	
            WHERE raven_getSnapshootByMonthAndGender.sex = ole.sex
        END

        --online

        IF EXISTS ( SELECT * FROM tOnline_Cashier a WHERE DATEDIFF(m,?,a.dateTrans) = 0 )
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
                WHERE DATEDIFF(m,?,a.dateTrans) = 0
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
        """,
        date,
        date,
        date,
        date,
        date,
        date,
    )

    cursor.execute(
        """
        SELECT
        CASE
            WHEN sex = 'U' THEN 'UNISEX'
            WHEN sex = 'M' THEN 'MALE'
            WHEN sex = 'F' THEN 'FEMALE'
            WHEN sex = 'KD' THEN 'KIDS'
            WHEN sex = 'JR' THEN 'JUNIOR'
        END, SaleQty, saleValue, inventoryQty, inventoryValue
        FROM raven_getSnapshootByMonthAndGender
        WHERE SaleQty > 0
        AND  inventoryQty > 0
        """
    )
    result = cursor.fetchall()

    total_data = len(result)

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {"title": "Monthly Gender Share"}

    chart_data = []

    # JIKA DATA TIDAK NOL
    if total_data > 0:
        data["table_headers"] = ["#", "Gender", "Sales", "Inventory"]
        data["table_footer"] = "* STR: Sell-Thru Rate"
        data["records"] = []

        # PERSIAPKAN VARIABLE
        counter = 1
        others_sales_qty = 0
        others_sales_value = 0
        others_inventory_qty = 0
        others_inventory_value = 0
        total_sales_value = 0

        # SUM TOTAL SALES VALUE
        for item in result:
            total_sales_value += round(float(item[2]) / 1000000, 2)

        for item in result:
            # PERSIAPKAN ARRAY UNTUK MENAMPUNG BARIS
            row = []

            # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
            sex = item[0]
            sales_qty = item[1]
            sales_value = item[2]
            inventory_qty = item[3]
            inventory_value = item[4]

            # JIKA DATA LEBIH KECIL DARI TOP LIMIT
            if counter <= top_limit:
                if total_data > 1:
                    # HITUNG PRESENTASE SALES VALUE
                    # DAN FORMAT TAMPILANNYA MENGGUNAKAN TANDA %
                    if sales_value > 0:
                        sales_value_percentage = sales_value_percentage_format(
                            sales_value, total_sales_value
                        )
                        sex_display = sex + sales_value_percentage
                    else:
                        sex_display = sex + " (0%)"

                    chart_data.append([sex_display, sales_value])

                # JIKA INVENTORY QUANTITY TIDAK NOL
                # HITUNG SELL THRU RATE NYA
                if inventory_qty > 0:
                    sell_thru_rate = sell_thru_rate_format(sales_qty, inventory_qty)
                else:
                    sell_thru_rate = "STR: 0%"

                # FORMAT TAMPILAN DATA
                sales_qty = qty_format(sales_qty)
                sales_value = value_format(sales_value)
                inventory_qty = qty_format(inventory_qty)
                inventory_value = value_format(inventory_value)

                # FORMAT POSISI TAMPILAN
                sex_display = sex + "<br/>" + sell_thru_rate
                sales_display = sales_value + "<br/>" + sales_qty
                inventory_display = inventory_value + "<br/>" + inventory_qty

                # MASUKKAN DATA KEDALAM ARRAY BARIS
                row = [counter, sex_display, sales_display, inventory_display]

                # TAMBAHKAN ARRAY BARIS KEDALAM ARRAY RECORDS
                data["records"].append(row)

                # INCREMENT UNTUK PENOMORANc
                counter += 1

            # JIKA DATA DIATAS TOP LIMIT
            # MAKA HITUNG SISA DATA TERSEBUH SEBAGAI OTHERS
            else:
                others_sales_qty += sales_qty
                others_sales_value += sales_value
                others_inventory_qty += inventory_qty
                others_inventory_value += inventory_value

        if total_data > top_limit:
            sex = "OTHERS"
            others_sales_value = round(others_sales_value, 2)
            others_inventory_value = round(others_inventory_value, 2)
            # HITUNG PRESENTASE SALES VALUE
            # DAN FORMAT TAMPILANNYA MENGGUNAKAN TANDA %
            if others_sales_value > 0:
                sales_value_percentage = sales_value_percentage_format(
                    others_sales_value, total_sales_value
                )
                sex_display = sex + sales_value_percentage
            else:
                sex_display = sex + " (0%)"

            chart_data.append([sex_display, others_sales_value])

            # JIKA INVENTORY QUANTITY TIDAK NOL
            # HITUNG SELL THRU RATE NYA
            if others_inventory_qty > 0:
                sell_thru_rate = sell_thru_rate_format(
                    others_sales_qty, others_inventory_qty
                )
            else:
                sell_thru_rate = "STR: 0%"

            # FORMAT DATA OTHERS DAN MASUKKAN KEDALAM ARRAY BARIS
            # KEMUDIAN TAMBAHKAN ARRAY BARIS TERSEBUT KEDALAM ARRAY RECORDS
            others_sales_qty = qty_format(others_sales_qty)
            others_sales_value = value_format(others_sales_value)
            others_inventory_qty = qty_format(others_inventory_qty)
            others_inventory_value = value_format(others_inventory_value)

            # FORMAT POSISI TAMPILAN
            others_sex_display = sex + "<br/>" + sell_thru_rate
            others_sales_display = others_sales_value + "<br/>" + others_sales_qty
            others_inventory_display = (
                others_inventory_value + "<br/>" + others_inventory_qty
            )

            # MASUKKAN DATA KEDALAM ARRAY BARIS
            row = [
                counter,
                others_sex_display,
                others_sales_display,
                others_inventory_display,
            ]
            data["records"].append(row)

        if total_data > 1:
            # CREATE CHART OBJECT, AND APPEND CHART DATA
            try:
                chl = ""
                chd = ""
                for item in chart_data:
                    chl += str(item[0]) + "|"
                    chd += str(item[1]) + ","

                chl = chl[:-1]
                chd = chd[:-1]

                image_url = (
                    "http://cdn.revota.com/raven/?cht=pie&chw=500&chd="
                    + chd
                    + "&chl="
                    + chl
                )
                data["chart"] = image_url

            except Exception as e:
                return str(e)

        return view_distribute(data)
    else:
        return view_no_data(data["title"])