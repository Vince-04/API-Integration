from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, get_db
from schemas import OrderCreate, ItemUpdate

import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShopLite API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ITEMS
@app.get("/items", response_model=list[schemas.ItemOut])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()


@app.post("/items", response_model=schemas.ItemOut)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ORDERS
@app.post("/orders", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(item_id=order.item_id, quantity=order.quantity, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders", response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


# SALES
@app.get("/sales", response_model=list[schemas.SaleOut])
def get_sales(db: Session = Depends(get_db)):
    return db.query(models.Sale).all()

@app.post("/sales", response_model=schemas.SaleOut)
def create_sale(sale: schemas.SaleBase, db: Session = Depends(get_db)):
    db_sale = models.Sale(order_id=sale.order_id, total=sale.total)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@app.get("/")
def read_root():
    return {"message": "Welcome to ShopLite API!"}

@app.put("/items/{item_id}", response_model=schemas.ItemOut, summary="Update an Item")
def update_item(item_id: int, updated_item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Only update fields provided
    update_data = updated_item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.customer_name = order.customer_name
    db_order.item_id = order.item_id
    db_order.quantity = order.quantity

    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")

        db.delete(db_item)
        db.commit()
        return {"message": f"Item with id {item_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/orders/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": f"Order with id {order_id} deleted successfully"}