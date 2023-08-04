from fastapi import FastAPI, HTTPException
from apiconfig import Product,  ProductList, Cart, User

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


@app.get("/getproducts")
async def root():
    return products


@app.get("/product/{prod_id}")
async def fetch_item(prod_id: int):
    print(prod_id)
    get_item = next((x for x in products["prods"] if x["id"] == prod_id), None)
    if get_item == None:
        raise HTTPException(status_code=404, detail="Böyle bir ürün bulunamadı")
    return get_item

