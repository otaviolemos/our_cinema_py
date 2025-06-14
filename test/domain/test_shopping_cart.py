
from datetime import datetime, timedelta
from domain.price_table import PriceTable
from domain.price_type import PriceType
from domain.reservation import Reservation
from domain.room import Room
from domain.session import Session
from domain.shopping_cart import ShoppingCart
from domain.user import User
from test.builder.movie_builder import MovieBuilder


# def test_create_shoping_cart():
#     room = Room("1")
#     movie = MovieBuilder().aMovie().with_duration(90).build()
#     today = datetime.now()
#     tomorrow = today + timedelta(days=1)
#     tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
#     session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
#     user = User("test_user")

#     reservation1 = Reservation(seats=['A3','A4'], session=session)
    
#     price_table = PriceTable(
#         { PriceType.REGULAR: 50.00, 
#           PriceType.SENIOR: 25.00 }
#     )

#     cart = ShoppingCart(user,reservation1, price_table)
#     assert cart.total_price() == 75.00
