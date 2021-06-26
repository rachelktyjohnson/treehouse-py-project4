from models import (Base, session, Product, engine)
from cleaners import clean_quantity, clean_date, clean_price
import csv
import datetime
import time


def load_csv():
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


def backup_csv():
    print("Backing up the database to 'backup.csv'...")
    time.sleep(1.5)
    with open('backup.csv', 'w', newline='') as csv_file:
        headers = ['product_name', 'product_price', 'product_quantity', 'date_updated']
        writer = csv.DictWriter(
            csv_file,
            delimiter=',',
            fieldnames=headers
        )
        writer.writeheader()
        for product in session.query(Product):
            writer.writerow({
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_quantity': product.product_quantity,
                'date_updated': product.date_updated
            })
    print("All done!")
    time.sleep(1.5)


def menu():
    while True:
        print("--------------------------")
        print("----------MENU------------")
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


def search_product():
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    id_error = True
    id_choice = None
    while id_error:
        print(f'Options: {id_options}')
        try:
            user_product_id = int(input("Enter Product ID: "))
        except ValueError:
            print("Oops. The Product ID should be a number. Try again!")
        else:
            if user_product_id in id_options:
                id_choice = user_product_id
                id_error = False
            else:
                print("Oops. That Product ID doesn't exist. Try again!")
    the_product = session.query(Product).filter(Product.product_id == id_choice).first()
    print("--------------------------")
    print(f'ID: {the_product.product_id}')
    print(f'Product Name: {the_product.product_name}')
    print(f'Product Quantity: {the_product.product_quantity}')
    print('Product Price: $' + '{:.2f}'.format(the_product.product_price / 100, 2))
    print(f'Last Updated: {the_product.date_updated}')
    print("--------------------------")
    input("Press ENTER to continue")


def add_product():
    input_name = input("Product Name: ")

    quantity_error = True
    input_quantity = None
    while quantity_error:
        input_quantity = clean_quantity(input("Product Quantity: "))
        if type(input_quantity) == int:
            quantity_error = False

    price_error = True
    input_price = None
    while price_error:
        input_price = clean_price(input("Product Price ($xx.xx): "))
        if type(input_price) == int:
            price_error = False

    date = datetime.date.today()
    print("Adding to database...")
    time.sleep(1.5)

    # check if the product name already exists
    product_in_db = session.query(Product).filter(Product.product_name == input_name).one_or_none()
    if product_in_db is None:
        new_product = Product(
            product_name=input_name,
            product_quantity=input_quantity,
            product_price=input_price,
            date_updated=date
        )
        session.add(new_product)
        session.commit()
        print(f'"{input_name}" added!')
        time.sleep(1.5)
    else:
        print(f'"{input_name}" already exists! Updating...')
        time.sleep(1.5)
        product_in_db.product_name = input_name
        product_in_db.product_quantity = input_quantity
        product_in_db.product_price = input_price
        product_in_db.date_updated = date
        session.add(product_in_db)
        session.commit()
        print(f'"{input_name}" updated!')
        time.sleep(1.5)


def app():
    app_running = True
    print("└[∵┌]└[ ∵ ]┘[┐∵]┘")
    print("STORE INVENTORY")
    while app_running:
        choice = menu()
        if choice == 'v':
            #  view details of a product
            print("--------------------------")
            print("View details of product".upper())
            search_product()

        elif choice == 'a':
            #  add a product to database
            print("--------------------------")
            print("Add product to database".upper())
            add_product()

        elif choice == 'b':
            #  backup database
            print("--------------------------")
            print("Backup database".upper())
            backup_csv()

        else:
            #  exit
            app_running = False
            print("Bye!")
            print("└[∵┌]└[ ∵ ]┘[┐∵]┘")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    load_csv()
    app()
