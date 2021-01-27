from helpers.query import executeQuery
from helpers.views import view_summary_daily, view_summary_monthly, view_distribute, view_distribute_expense, view_no_data
from helpers.number_format import qty_format, value_format, sales_value_percentage_format, sell_thru_rate_format


def distribute_daily_wholesale_customer(date, top_limit):
    # AMBIL DATA DARI STORED PROCEDURE DAN HITUNG JUMLAH DATANYA
    result = executeQuery("raven_getWholesaleByChannel '%s'" % date)
    total_data = len(result)

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {
        'title' : 'Daily Wholesale Customer'
    }

    # JIKA DATA TIDAK NOL
    if total_data > 0:

        data['table_headers'] = ['#', 'Customer', 'Qty', 'Sales Value']
        data['records'] = []

        # PERSIAPKAN VARIABLE
        counter = 1
        others_qty = 0
        others_sales_value = 0
        total_sales_value = 0
        
        # SUM TOTAL SALES VALUE
        for item in result:
            total_sales_value += round(float(item[2]) / 1000000, 2)

        for item in result:
            # PERSIAPKAN ARRAY UNTUK MENAMPUNG BARIS
            row = []

            # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
            customer = item[0]
            qty = item[1]
            sales_value = item[2]

            # JIKA DATA LEBIH KECIL DARI TOP LIMIT
            if counter <= top_limit:
                # FORMAT TAMPILAN DATA
                qty = qty_format(qty)
                sales_value = value_format(sales_value)

                # MASUKKAN DATA KE ARRAY BARIS
                row = [counter, customer, qty, sales_value]

                # TAMBAHKAN ARRAY BARIS KEDALAM ARRAY RECORD
                data['records'].append(row)

                # INCREMENT UNTUK PENOMORAN
                counter += 1  

            # JIKA DATA DIATAS TOP LIMIT 
            # MAKA HITUNG SISA DATA TERSEBUT SEBAGAI OTHERS
            else:
                others_qty += qty
                others_sales_value += sales_value

        if (total_data > top_limit):
            customer = "OTHERS"
            others_sales_value = round(others_sales_value, 2)

            # FORMAT DATA OTHERS DAN MASUKKAN KEDALAM ARRAY BARIS 
            # KEMUDIAN TAMBAHKAN ARRAY BARIS TERSEBUT KEDALAM ARRAY RECORDS
            qty = qty_format(others_qty)
            others_sales_value = value_format(others_sales_value)
            row = [counter, customer, qty, others_sales_value]
            data['records'].append(row)

        return view_distribute(data)
    else:
        return view_no_data(data['title'])
