def qty_format(number):
    qty = round(number) # membulatkan angka, karena hasil query ada angka 0 dibelakang koma
    qty = "{:,}".format(qty).replace(',', '.') # digit grouping untuk angka ribuan
    qty = str(qty) + " pcs" # konversi angka jadi string dan tambahkan tulisan "pcs"
    return qty

def value_format(number):
    """ 
    bagi number dengan 1jt
    jika hasil pembagian 1jt menghasilkan 4 digit maka bagi lagi dengan 1000
    untuk menentukan bahwa number tersebut bernilai milyaran
    karena 1 milyar = 1000 jt
    """
    # value = round(float(number) / 1000000, 2)

    # if len(str(round(value))) < 4:
    #     value = str(value) + " jt"
    #     return value
    # else:
    #     value = value / 1000
    #     value = round(value, 2)
    #     value = str(value) + " m"
    #     return value
    
    value = round(float(number) / 1000000, 2) # konversi angka ke pecahan juta, dengan 2 angka dibelakang koma
    value = '{:,}'.format(value).replace(',', ' ').replace('.', ',').replace(' ', '.') # default tanda (,) menjadi tanda (.) sebagai pemisah ribuan
    value = str(value) + " jt" # konversi angka ke string dan concat dengan " jt" dibelakangnya
    return value

def sales_value_percentage_format(sales_value, total_sales_value):
    # sales_value = round(float(sales_value) / 1000000, 2)
    sales_value = float(sales_value) / 1000000
    sales_value_percentage = (sales_value * 100) / total_sales_value
    sales_value_percentage = round(sales_value_percentage, 1)
    sales_value_percentage = str(sales_value_percentage).replace('.', ',')
    sales_value_percentage = "(" + sales_value_percentage + "%)"
    return sales_value_percentage

def sell_thru_rate_format(sales_qty, inventory_qty):
    sales_qty = float(sales_qty)
    inventory_qty = float(inventory_qty)
    sell_thru_rate = round( sales_qty / inventory_qty, 2)
    sell_thru_rate = str(sell_thru_rate).replace('.', ',')
    sell_thru_rate = 'STR: ' + sell_thru_rate + '%'
    return sell_thru_rate