from sqlalchemy import create_engine,Column,Integer,String,Float,Table,DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship,declarative_base
from datetime import datetime


Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship("Product", back_populates="category")

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    product = relationship("Product", back_populates="inventory")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    date_added = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", uselist=False, back_populates="product")

    def __init__(self, name, description, price, category=None):
        self.name = name
        self.description = description
        self.price = price
        self.category = category



if __name__ == "__main__": 
    engine = create_engine('sqlite:///inventory.db')       
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        menu = '''
        ========================================================
            INVENTORY MANAGEMENT SYSTEM
        ========================================================
            1: ADD PRODUCT                          
            2: VIEW PRODUCTS
            3: UPDATE PRODUCT DETAILS
            4: SEARCH PRODUCT
            5: EXIT
        ========================================================
        '''
        
        print(menu)
        choice = input("Enter your choice (1/2/3/4/5): ")

        