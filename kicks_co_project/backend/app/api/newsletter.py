from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import NewsletterSubscriber
from app.schemas.newsletter import MessageResponse, NewsletterRequest

router = APIRouter(prefix='/api/newsletter', tags=['newsletter'])


@router.post('/subscribe', response_model=MessageResponse)
def subscribe(payload: NewsletterRequest, db: Session = Depends(get_db)):
    existing = db.query(NewsletterSubscriber).filter(NewsletterSubscriber.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already subscribed')

    subscriber = NewsletterSubscriber(email=payload.email.lower())
    db.add(subscriber)
    db.commit()
    return {'message': 'Subscribed successfully'}
