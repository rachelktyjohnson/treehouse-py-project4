from models import (Base, session, Product, engine)
import csv
import datetime
import time


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


def load_csv():
    #  open the CSV file
    with open('inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db is None:
                if row[0] != 'product_name':
                    print(row)
                    name = row[0]
                    price = clean_price(row[1])
                    quantity = clean_quantity(row[2])
                    date = clean_date(row[3])
                    new_product = Product(
                        product_name=name,
                        product_quantity=quantity,
                        product_price=price,
                        date_updated=date
                    )
                    session.add(new_product)
        session.commit()


def menu():
    while True:
        print("--------------------------")
        print("[v]iew the details of a single product")
        print("[a]dd a new product to the database")
        print("[b]ackup the entire database")
        print("e[x]it program")
        print("--------------------------")
        menu_choice = input("Make your choice [v/a/b/x]: ")
        menu_options = ['v', 'a', 'b', 'x']
        if menu_choice in menu_options:
            return menu_choice
        else:
            print("Please choose a valid option!")


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            #  view details of a product
            print("--------------------------")
            print("View details of product".upper())
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            id_choice = None
            while id_error:
                print(f'Options: {id_options}')
                user_product_id = int(input("Enter Product ID: "))
                if user_product_id in id_options:
                    id_choice = user_product_id
                    id_error = False
                else:
                    print("Oops. That's not a valid Product ID. Try again!")
            the_product = session.query(Product).filter(Product.product_id == id_choice).first()
            print("--------------------------")
            print(f'ID: {the_product.product_id}')
            print(f'Product Name: {the_product.product_name}')
            print(f'Product Quantity: {the_product.product_quantity}')
            print(f'Product Price: {the_product.product_price}')
            print(f'Last Updated: {the_product.date_updated}')
            print("--------------------------")
            input("Press ENTER to continue")
        elif choice == 'a':
            #  add a product to database
            print("--------------------------")
            print("Add product to database".upper())
        elif choice == 'b':
            #  backup database
            print("--------------------------")
            print("Backup database".upper())
        else:
            #  exit
            app_running = False
            print("Bye!")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    load_csv()
    app()
