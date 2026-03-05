from fastapi import FastAPI

api = FastAPI()


@api.get("/shop")
def list_products():
    ...

@api.get("/shop/{category}")
def list2_products(category: str):
    return f"category - {category}"

@api.get("/shop/{category}/{product}")
def list3_products(category: str, product: str):
    return f"category - {category} | product - {product}"

@api.post("/shop")
def list4_products():
    ...