import datetime


def clean_price(price_str):
    try:
        price_float = float(price_str[1::])
        price_int = int(price_float*100)
    except ValueError:
        print("******** PRICE ERROR ********")
        print("Be sure to enter the price with a $ sign")
        print("Ex: $10.99")
    else:
        return price_int


def clean_quantity(quantity_str):
    try:
        quantity_int = int(quantity_str)
    except ValueError:
        print("******** QUANTITY ERROR ********")
        print("Be sure to enter the quantity as an integer")
        print("Ex: 11")
    else:
        return quantity_int


def clean_date(date_str):
    try:
        split_date = date_str.split('/')
        date_date = datetime.date(int(split_date[2]), int(split_date[0]), int(split_date[1]))
    except ValueError:
        print("******** DATE ERROR ********")
        print("Be sure to enter the date in a MM/DD/YYYY format")
        print("Ex: 12/28/2018")
    else:
        return date_date
