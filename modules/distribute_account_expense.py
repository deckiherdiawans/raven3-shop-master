from helpers.query import executeQuery
from helpers.views import view_summary_daily, view_summary_monthly, view_distribute, view_distribute_expense, view_no_data
from helpers.number_format import qty_format, value_format, sales_value_percentage_format, sell_thru_rate_format

def distribute_account_expense(date):
    # AMBIL DATA DARI STORED PROCEDURE DAN HITUNG JUMLAH DATANYA
    result = executeQuery("raven_getAccountExpenseBydate '%s'" % date)
    total_data = len(result)

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {
        'title' : 'Daily Account Expense'
    }

    # JIKA DATA TIDAK NOL
    if total_data > 0:

        data['table_headers'] = ['#', 'Account', 'Expense']
        data['records'] = []

        # PERSIAPKAN VARIABLE
        counter = 1
        total_expense = 0
        
        # SUM TOTAL SALES VALUE
        for item in result:
            total_expense += round(float(item[1]) / 1000000, 2)

        for item in result:
            # PERSIAPKAN ARRAY UNTUK MENAMPUNG BARIS
            row = []

            # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
            account = item[0]
            expense = item[1]

            # JIKA DATA LEBIH KECIL DARI TOP LIMIT
            

            # FORMAT TAMPILAN DATA
            expense = value_format(expense)

            # MASUKKAN DATA KE ARRAY BARIS
            row = [counter, account, expense]

            # TAMBAHKAN ARRAY BARIS KEDALAM ARRAY RECORD
            data['records'].append(row)

            # INCREMENT UNTUK PENOMORAN
            counter += 1  

        # TAMBAHKAN GRAND TOTAL KE ARRAY BARIS
        row = ['', 'GRAND TOTAL', str(total_expense) + " jt"]

        # TAMBAHKAN ARRAY BARIS KEDALAM ARRAY RECORD
        data['records'].append(row)

        return view_distribute_expense(data)
    else:
        return view_no_data(data['title'])
