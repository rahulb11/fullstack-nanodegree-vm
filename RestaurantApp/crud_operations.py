from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# myFirstRestaurant = Restaurant(name="Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()
# print "first restaurant created"

# restarants = session.query(Restaurant).all()
# for restaurant in restarants:
#     session.delete(restaurant)
# session.commit()

restarants = session.query(Restaurant).all()
for restaurant in restarants:
    print restaurant.name