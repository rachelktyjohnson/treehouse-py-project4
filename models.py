from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Title', String)
    product_quantity = Column('Author', String)
    product_price = Column('Price', Integer)
    date_updated = Column('Date', Date)

    def __repr__(self):
        return f'<Product(ID: {self.product_id}, Name: {self.product_name},' \
               f'Quantity: {self.product_quantity}, Price: ${self.product_price})>'
