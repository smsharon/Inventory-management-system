import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Product 
from datetime import datetime

@click.command()
@click.option('--name', prompt='Enter product name', help='Product name')
@click.option('--description', prompt='Enter product description', help='Product description')
@click.option('--price', prompt='Enter product price', type=float, help='Product price')
@click.option('--category', prompt='Enter product category', help='Product category')
def add_product(name, description, price, category):
    # Create a database session
    engine = create_engine('sqlite:///inventory.db')
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Query the category by name
        existing_category = session.query(Category).filter_by(name=category).first()

        if not existing_category:
            # If the category doesn't exist, create it
            new_category = Category(name=category)
            session.add(new_category)
            session.commit()

        # Create a new product with the given details and category
        product = Product(name=name, description=description, price=price, category=existing_category)
        session.add(product)
        session.commit()

if __name__ == "__main__":
    add_product()
