from helpers.query import executeQuery
from helpers.views import view_summary_daily, view_summary_monthly, view_distribute, view_distribute_expense, view_no_data
from helpers.number_format import qty_format, value_format, sales_value_percentage_format, sell_thru_rate_format

def distribute_daily_brand_share(date, top_limit):
    # AMBIL DATA DARI STORED PROCEDURE DAN HITUNG JUMLAH DATANYA
    result = executeQuery("raven_getCashierBydateAndBrand '%s'" % date)
    total_data = len(result)

    # PERSIAPKAN ARRAY UNTUK MENAMPUNG DATA
    data = {
        'title' : 'Daily Brand Share'
    }

    chart_data = []

    # JIKA DATA TIDAK NOL
    if total_data > 0:

        data['table_headers'] = ['#', 'Brand', 'Qty', 'Sales Value']
        data['records'] = []

        # PERSIAPKAN VARIABLE
        counter = 1
        others_qty = 0
        others_sales_value = 0
        total_sales_value = 0
        
        # SUM TOTAL SALES VALUE
        for item in result:
            total_sales_value += round(float(item[3]) / 1000000, 2)

        for item in result:
            # PERSIAPKAN ARRAY UNTUK MENAMPUNG BARIS
            row = []

            # MASUKAN RECORD KEDALAM VARIABLE SUPAYA TIDAK MEMBINGUNGKAN
            brand = item[1]
            qty = item[2]
            sales_value = item[3]

            # JIKA DATA LEBIH KECIL DARI TOP LIMIT
            if counter <= top_limit:

                if total_data > 1:
                    # HITUNG PRESENTASE SALES VALUE
                    # DAN FORMAT TAMPILANNYA MENGGUNAKAN TANDA %
                    if sales_value > 0:
                        sales_value_percentage = sales_value_percentage_format(sales_value, total_sales_value)
                        brand_display = brand + sales_value_percentage
                    else:
                        brand_display = brand + ' (0%)'
                        
                    chart_data.append([brand_display, sales_value])

                # FORMAT TAMPILAN DATA
                qty = qty_format(qty)
                sales_value = value_format(sales_value)

                # MASUKKAN DATA KE ARRAY BARIS
                row = [counter, brand, qty, sales_value]

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
            brand = "OTHERS"
            others_sales_value = round(others_sales_value, 2)
            # HITUNG PRESENTASE SALES VALUE
            # DAN FORMAT TAMPILANNYA MENGGUNAKAN TANDA %
            if others_sales_value > 0:
                sales_value_percentage = sales_value_percentage_format(others_sales_value, total_sales_value)
                brand_display = brand + sales_value_percentage
            else:
                brand_display = brand + ' (0%)'

            chart_data.append([brand_display, others_sales_value])

            # FORMAT DATA OTHERS DAN MASUKKAN KEDALAM ARRAY BARIS 
            # KEMUDIAN TAMBAHKAN ARRAY BARIS TERSEBUT KEDALAM ARRAY RECORDS
            qty = qty_format(others_qty)
            others_sales_value = value_format(others_sales_value)
            row = [counter, brand, qty, others_sales_value]
            data['records'].append(row)

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

                image_url = "http://cdn.revota.com/raven/?cht=pie&chw=500&chd=" + chd + "&chl=" + chl
                data['chart'] = image_url

            except Exception as e:
                return(str(e))

        return view_distribute(data)
    else:
        return view_no_data(data['title'])
