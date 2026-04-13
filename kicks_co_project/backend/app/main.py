from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, auctions, newsletter, products
from app.core.config import get_settings
from app.db.database import Base, SessionLocal, engine
from app.db.seed import seed_initial_data
import app.models  # noqa: F401

settings = get_settings()
app = FastAPI(title='Kicks & Co API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(auctions.router)
app.include_router(newsletter.router)


@app.on_event('startup')
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()


@app.get('/')
def health_check():
    return {'message': 'Kicks & Co API is running'}
