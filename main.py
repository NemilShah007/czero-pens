from fastapi import FastAPI

app = FastAPI()

inventory = {
    "CZPR": {
        "productName": "CZero Pen Brand",
        "variant": "Red Pen",
        "price": 1.00,
        "quantity": 5,
        "description": "High quality pens that are carbon-neutral"
    },
    "CZPB": {
        "productName": "CZero Pen Brand",
        "variant": "Blue Pen",
        "price": 1.00,
        "quantity": 5,
        "description": "High quality pens that are carbon-neutral"
    },
    "CZPG": {
        "productName": "CZero Pen Brand",
        "variant": "Green Pen",
        "price": 1.00,
        "quantity": 5,
        "description": "High quality pens that are carbon-neutral"
    },
    "RPG": {
        "productName": "Red's Pens",
        "variant": "Black Fountain Pen",
        "price": 5.00,
        "quantity": 100,
        "description": "Fountain pens designed by Paul Red"
    },
    "PRG": {
        "productName": "Red's Pens",
        "variant": "Purple Fountain Pen",
        "price": 5.00,
        "quantity": 100,
        "description": "Fountain pens designed by Paul Red"
    },
    "BYP": {
        "productName": "Good Quality Pencil",
        "variant": "",
        "price": 0.5,
        "quantity": 1000,
        "description": "Handmade Pencils"
    }
}

@app.get("/")
async def root():
    return {"message": "Welcome to CZero Pens API"}

@app.get("/inventory")
async def get_inventory():
    return inventory

@app.get("/inventory/{sku}")
async def get_product(sku: str):
    if sku in inventory:
        return inventory[sku]
    else:
        return {"error": "Item not found"}

@app.put("/inventory/{sku}")
async def update_product(sku: str, quantity: int = None, description: str = None):
    if sku in inventory:
        if quantity and description:
            inventory[sku]["quantity"] = quantity
            inventory[sku]["description"] = description
            return inventory[sku]
        elif quantity:
            inventory[sku]["quantity"] = quantity
            return inventory[sku]
        elif description:
            inventory[sku]["description"] = description
            return inventory[sku]
    else:
        return {"error": "Item not found"}

@app.delete("/inventory/{sku}")
async def delete_product(sku: str):
    if sku in inventory:
        del inventory[sku]
        return {"message": "Item deleted"}
    else:
        return {"error": "Item not found"}

@app.post("/inventory")
async def add_product(product: dict):
    sku = product["SKU"]
    if sku in inventory:
        return {"error": "Item already exists"}
    else:
        product.pop("SKU", None)  # Remove the SKU key from the dictionary
        inventory[sku] = product
        return inventory[sku]

@app.post("/cart")
async def buy_product(items: dict):
    total = 0.0
    for sku, quantity in items.items():
        if sku in inventory:
            price = inventory[sku]["price"]
            total += price * quantity
        else:
            return {"error": f"Item not found: {sku}"}
    return {"total": total}

@app.get("/search/{query}")
async def search_inventory(query: str):
    results = []
    for sku, product in inventory.items():
        if query.lower() in product["productName"].lower() or query.lower() in product["variant"].lower() or query in str(product["quantity"]):
            results.append(product)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)