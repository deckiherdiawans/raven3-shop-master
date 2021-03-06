from helpers.query import executeQuery
from helpers.views import (
    view_summary_daily,
    view_summary_monthly,
    view_distribute,
    view_distribute_expense,
    view_no_data,
)
from helpers.number_format import (
    qty_format,
    value_format,
    sales_value_percentage_format,
    sell_thru_rate_format,
)


def distribute_monthly_brand(date, top_limit):
    # AMBIL DATA DARI STORED PROCEDURE DAN HITUNG JUMLAH DATANYA
    result = executeQuery("raven_getSnapshootByMonthAndBrand '%s'" % date)
    total_data = len(result)

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {"title": "Monthly Brand Share"}

    chart_data = []

    # JIKA DATA TIDAK NOL
    if total_data > 0:
        data["table_headers"] = ["#", "Brand", "Sales", "Inventory"]
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
            total_sales_value += round(float(item[3]) / 1000000, 2)

        for item in result:
            # PERSIAPKAN ARRAY UNTUK MENAMPUNG BARIS
            row = []

            # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
            brand = item[1]
            sales_qty = item[2]
            sales_value = item[3]
            inventory_qty = item[4]
            inventory_value = item[5]

            # JIKA DATA LEBIH KECIL DARI TOP LIMIT
            if counter <= top_limit:
                if total_data > 1:
                    # HITUNG PRESENTASE SALES VALUE
                    # DAN FORMAT TAMPILANNYA MENGGUNAKAN TANDA %
                    if sales_value > 0:
                        sales_value_percentage = sales_value_percentage_format(
                            sales_value, total_sales_value
                        )
                        brand_display = brand + sales_value_percentage
                    else:
                        brand_display = brand + " (0%)"

                    chart_data.append([brand_display, sales_value])

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
                brand_display = brand + "<br/>" + sell_thru_rate
                sales_display = sales_value + "<br/>" + sales_qty
                inventory_display = inventory_value + "<br/>" + inventory_qty

                # MASUKKAN DATA KEDALAM ARRAY BARIS
                row = [counter, brand_display, sales_display, inventory_display]

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
            brand = "OTHERS"
            others_sales_value = round(others_sales_value, 2)
            others_inventory_value = round(others_inventory_value, 2)
            # HITUNG PRESENTASE SALES VALUE
            # DAN FORMAT TAMPILANNYA MENGGUNAKAN TANDA %
            if others_sales_value > 0:
                sales_value_percentage = sales_value_percentage_format(
                    others_sales_value, total_sales_value
                )
                brand_display = brand + sales_value_percentage
            else:
                brand_display = brand + " (0%)"

            chart_data.append([brand_display, others_sales_value])

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
            others_brand_display = brand + "<br/>" + sell_thru_rate
            others_sales_display = others_sales_value + "<br/>" + others_sales_qty
            others_inventory_display = (
                others_inventory_value + "<br/>" + others_inventory_qty
            )

            # MASUKKAN DATA KEDALAM ARRAY BARIS
            row = [
                counter,
                others_brand_display,
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
