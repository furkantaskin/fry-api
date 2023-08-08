from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import base64


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    quantity: Optional[int] = 0
    price: float


class ProductList(BaseModel):
    prods: List[Product]


class User(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: str
    password: str
    auth_level: Optional[int] = None
    cart: Optional[ProductList] = None


users: Dict[str, List[User]] = {
    "users": [
        {
            "id": 1,
            "name": "Furkan Taşkın",
            "email": "taskinfurkan1@gmail.com",
            "password": "deneme123",
            "auth_level": 1
        },
        {
            "id": 2,
            "name": "Diğer Furkan",
            "email": "deneme@domain.com",
            "password": "321deneme",
            "auth_level": 0
        }
    ]
}

products: ProductList = {
    "prods": [
        {
            "id": 1,
            "name": "Fön Makinesi",
            "description": "Siyah fön makinesi",
            "price": 3.14,
        },
        {
            "id": 2,
            "name": "Vantilatör",
            "description": "Soğutuculu vantilatör",
            "price": 99,
        },
        {
            "id": 3,
            "name": "İpek Gömlek",
            "description": "İpek gömlek",
            "price": 440.25,
        },
        {
            "id": 4,
            "name": "Bisiklet",
            "description": "Dağ tipi bisiklet",
            "price": 9_999.99,
        },
        {
            "id": 5,
            "name": "Bilgisayar",
            "description": "Dizüstü bilgisayar",
            "price": 45_234.67,
        },
        {
            "id": 6,
            "name": "Fincan",
            "description": "Özel baskılı porselen kahve fincanı",
            "price": 45.99,
        },
    ]
}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)


def check_item_exist(item, user_or_prod):
    if (user_or_prod == "user"):
        return next((x for x in users["users"] if x["id"] == item), None)

    else:
        return next((x for x in products["prods"] if x["id"] == item), None)


@app.get("/")
async def greet():
    return {"message": "it works!"}


@app.get("/products")
async def root():
    return products


@app.get("/product/{prod_id}")
async def fetch_item(prod_id: int):
    get_item = check_item_exist(prod_id, "prod")
    if get_item == None:
        raise HTTPException(
            status_code=404, detail="Böyle bir ürün bulunamadı")
    return get_item


@app.post("/addproduct")
async def add_product(product: Product):
    last_id: int = products["prods"][-1]["id"]
    update_item = product.dict()
    update_item["id"] = last_id + 1
    products["prods"].append(update_item)
    return products


@app.get("/users")
async def get_users():
    return users


@app.get("/user/{user_id}")
async def fetch_user(user_id: int):
    get_user = check_item_exist(user_id, "user")
    if get_user == None:
        raise HTTPException(
            status_code=404, detail="Kullanıcı bulunamadı")
    return get_user


@app.post("/sign-in")
async def sign_in(user: Dict[str, Any]):
    get_user = next((x for x in users["users"] if x["email"] == user["email"]), None)
    print(get_user)
    if get_user == None or get_user["password"] != user["password"]:
        raise HTTPException(
            status_code=404, detail="Kullanıcı bulunamadı")
    
    get_hash_dict: Dict[str, str] = {
        "name": get_user["name"],
        "email": get_user["email"],
        "auth_level": get_user["auth_level"]
    }
    get_hash = base64.b64encode(str(get_hash_dict).encode("utf-8"))
    return {"auth_level": get_user["auth_level"], "get_hash": get_hash}
