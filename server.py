from pydantic import BaseModel

from fastapi import FastAPI, HTTPException

import ulid

# Order model for validations
class Order(BaseModel):
    id: int
    quantity: int

class Orders(BaseModel):
    orders: list[Order]

class Pizza:
    id = 0
    name = ""
    size = ""
    price = 0
    toppings = []

    def __init__(self, id, name, size, price, toppings):
        self.id = id
        self.name = name
        self.size = size
        self.price = price
        self.toppings = toppings


class PizzaMenu:
    pizzas = []

    def __init__(self, pizzas):
        self.pizzas = pizzas

    def getItemById(self, id: int):
        for pizza in self.pizzas:
            if pizza['id'] == id:
                return pizza
        return None

pizza_menu = [
    {
        "id": 1,
        "name": "margherita",
        "size": "medium",
        "stock": 10,
        "price": 8.99,
        "toppings": ["tomato sauce", "mozzarella", "basil&quot"]
    },

    {
        "id": 2,
        "name": "veggic paradise",
        "size": "medium",
        "stock": 5,
        "price": 12.99,
        "toppings": ["tomato sauce", "mozzarella", "basil&quot"]
    }
]

app = FastAPI()

def getMenuItem(id: int):
    for pizza in pizza_menu:
        if pizza['id'] == id:
            return pizza
    return None

# get menu, with optional name query parameter
@app.get("/menu")
async def getmenu(name: str, status_code=200):
    print("given name", name)
    if name != '':
        for pizza in pizza_menu:
            if pizza['name'] == name:
                return {
                    "menu": pizza
                }
        return {"menu": None}
    return {
        "menu": pizza_menu
    }

globalorders = []

# place an order
@app.post("/order")
async def placeOrder(order: Orders, status_code=201):
    print("incoming orders", order)

    if order.orders != None:
        current_order = {"order_id": str(ulid.new()), "price": 0}
        for order in order.orders:
            print("processing order", order)
            if order.id != None:
                pizza = getMenuItem(order.id)
                if pizza != None:
                    current_order["price"] += pizza["price"]
                else:
                    return {
                        "message": "no pizza found with given id:" + str(current_order["price"])
                    }
            else:
                raise HTTPException(status_code=400, detail="no id given for the given pizza to find")
                # return {
                #     "message": "no id given for the given pizza to find"
                # }
        globalorders.append(current_order)
        return current_order
    else:
        raise HTTPException(status_code=400, detail="no orders given")
        # return {
        #     "message": "no orders given"
        # }
