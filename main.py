from fastapi import FastAPI

from users.user_api import user_router
from cards.card_api import card_router
from laptops.laptop_api import laptop_router
from carts.cart_api import cart_router

from database import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')

app.include_router(user_router)
app.include_router(card_router)
app.include_router(laptop_router)
app.include_router(cart_router)
