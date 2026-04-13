from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Auction
from app.schemas.auction import AuctionResponse

router = APIRouter(prefix='/api/auctions', tags=['auctions'])


@router.get('', response_model=list[AuctionResponse])
def list_auctions(db: Session = Depends(get_db)):
    return db.query(Auction).order_by(Auction.ends_at.asc()).all()
