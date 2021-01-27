from helpers.query import executeQuery
from helpers.views import view_summary_daily, view_summary_monthly, view_distribute, view_distribute_expense, view_no_data
from helpers.number_format import qty_format, value_format, sales_value_percentage_format, sell_thru_rate_format


# RETURN DARI FUNGSI INI SEHARUSNYA STRING HTML YANG SUDAH ADA DATANYA
def summary_daily_store(date):
    # AMBIL DATA DARI STORED PROCEDURE DAN HITUNG JUMLAH DATANYA
    result = executeQuery("raven_getCashierBydate '%s', 10" % date)
    total_data = len(result)

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {
        'title' : 'Daily Store Sales',
    }

    # AMBIL BARIS PERTAMA KARENA HASIL DARI RETURN CUMAN SATU BARIS
    result = result[0]

    # JIKA DATA TIDAK NOL
    if total_data > 0 and result[2] > 0:
        # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
        total_transactions = result[2]
        sales_value = result[1]
        sales_qty = result[0]
        total_customers = result[3]
        sales_per_order = 0
        qty_per_order = 0

        if (total_transactions > 0):
            if(sales_value > 0):
                # HITUNG DATA SALE PER ORDER DAN QTY PER ORDER KEMUDIAN FORMAT 
                sales_per_order = sales_value / total_transactions
                sales_per_order = value_format(sales_per_order)
                qty_per_order = sales_qty / total_transactions
                qty_per_order = qty_format(qty_per_order)
            else:
                sales_per_order = "0 jt"
                qty_per_order = "0 pcs"

        # FORMAT DATA SALES VALUE DAN QTY VALUE
        sales_value = value_format(sales_value)
        sales_qty = qty_format(sales_qty)

        # MASUKAN DATA KE ARRAY RECORDS
        data['records'] = [
            ["Sales Qty", sales_qty],
            ["Sales Value" , sales_value],
            ["Transactions" , total_transactions],
            ["Customer" , total_customers],
            ["Average Purchase Value" , sales_per_order],
            ["Unit Per Transaction" , qty_per_order]
        ]

        return view_summary_daily(data)
    else:
        return view_no_data(data['title'])
