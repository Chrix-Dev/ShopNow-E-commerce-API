from fastapi import FastAPI
from utils.database import Base, engine
from routers import users, products, cart, orders, categories, payments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShopNow E-Commerce API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(categories.router)
app.include_router(payments.router)