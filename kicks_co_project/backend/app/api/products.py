from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Product
from app.schemas.product import ProductResponse

router = APIRouter(prefix='/api/products', tags=['products'])


@router.get('', response_model=list[ProductResponse])
def list_products(category: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Product)
    if category and category != 'all':
        query = query.filter(Product.category == category)
    return query.order_by(Product.id.asc()).all()
