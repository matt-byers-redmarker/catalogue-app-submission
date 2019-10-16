from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///MBitemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# First user
User1 = User(
    username="Thomas Shelby",
    email="thomas.shelby@shelbycompanylimited.com",
    picture='')
session.add(User1)

# Items within Soccer
category1 = Category(name="Soccer")
session.add(category1)

CategoryItem1 = CategoryItem(
    name="Soccer Ball",
    description="A round soccer ball.",
    category=category1,
    user=User1)
session.add(CategoryItem1)

CategoryItem2 = CategoryItem(
    name="Keeping Gloves",
    description="Thick gloves for keeping.",
    category=category1,
    user=User1)
session.add(CategoryItem2)


# Items within AFL
category2 = Category(name="AFL")

session.add(category2)

CategoryItem1 = CategoryItem(
    name="AFL ball",
    description="A real good quality footy.",
    category=category2,
    user=User1)

session.add(CategoryItem1)

CategoryItem2 = CategoryItem(
    name="Grippo",
    description="Helps you grab those marks",
    category=category2,
    user=User1)

session.add(CategoryItem2)
session.commit()

print ("User added!")
print ("added categories and items!")
