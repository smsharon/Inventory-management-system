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

def add_product(session):
    while True:
        # Take user input for product details
        name = input("Enter the product name (or type 'cancel' to go back to the main menu): ")
        
        if name.lower() == 'cancel':
            # If the user types 'cancel', exit the function and return to the main menu
            return
        
        description = input("Enter the product description: ")
        price = float(input("Enter the product price: "))
        category_name = input("Enter the product category: ")

        # Check if the category already exists in the database, or create it if not
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)

        # Create a new Product object and add it to the session
        new_product = Product(name=name, description=description, price=price, category=category)
        session.add(new_product)
        session.commit()

        print("Product added successfully!")
def view_products(session):
    # Query all products from the database
    products = session.query(Product).all()

    # Check if there are any products
    if not products:
        print("No products found.")
    else:
        print("List of Products:")
        for product in products:
            display_product_info(product)
            print("-" * 40)

def display_product_info(product):
    print(f'ID: {product.id}')
    print(f'Name: {product.name}')
    print(f'Description: {product.description}')
    print(f'Price: {product.price}')
    print(f'Category: {product.category.name if product.category else "N/A"}')
    print(f'Date Added: {product.date_added}')
    print("-" * 40)         

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
        if choice == "1":
            add_product(session) 
        elif choice == "2":
            view_products(session)    

        