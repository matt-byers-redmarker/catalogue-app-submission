from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Category, CategoryItem
 
engine = create_engine('sqlite:///MBitemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Items within Soccer
# category1 = Category(name = "Soccer")

# session.add(category1)
# session.commit()

# CategoryItem1 = CategoryItem(name = "Soccer Ball", description = "A round soccer ball.", category = category1)

# session.add(CategoryItem1)
# session.commit()

# CategoryItem2 = CategoryItem(name = "Keeping Gloves", description = "Thick gloves for keeping.", category = category1)

# session.add(CategoryItem2)
# session.commit()



# #Items within AFL
# category2 = Category(name = "AFL")

# session.add(category2)
# session.commit()

# CategoryItem1 = CategoryItem(name = "AFL ball", description = "A real good quality footy.", category = category2)

# session.add(CategoryItem1)
# session.commit()

# CategoryItem2 = CategoryItem(name = "Grippo", description = "Helps you grab those marks", category = category2)

# session.add(CategoryItem2)
# session.commit()

session.rollback()

print ("session rolledback!")

# print ("added categories and items!")
