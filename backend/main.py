from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import databases
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware

# Настройки базы данных
DATABASE_URL = "postgresql://straders:straders@db/straders_db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Определение таблицы
items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель Pydantic
class Item(BaseModel):
    name: str
    price: float

class ItemInDB(Item):
    id: int

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/items/", response_model=List[ItemInDB])
async def read_items():
    query = items.select()
    return await database.fetch_all(query)

@app.post("/items/", response_model=ItemInDB)
async def create_item(item: Item):
    query = items.insert().values(name=item.name, price=item.price)
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}

@app.put("/items/{item_id}/", response_model=ItemInDB)
async def update_item(item_id: int, item: Item):
    query = items.update().where(items.c.id == item_id).values(name=item.name, price=item.price)
    await database.execute(query)
    return {**item.dict(), "id": item_id}

@app.delete("/items/{item_id}/")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {"message": "Item deleted"}
