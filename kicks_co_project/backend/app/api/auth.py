from fastapi import APIRouter, Depends, HTTPException, Response, status, Cookie
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.config import get_settings
from app.db.database import get_db
from app.models import User, UserSession
from app.schemas.auth import AuthResponse, LoginRequest, SignupRequest, UserResponse
from app.services.security import generate_session_token, get_session_expiry, hash_password, verify_password

router = APIRouter(prefix='/api/auth', tags=['auth'])
settings = get_settings()


@router.post('/signup', response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    user = User(
        full_name=payload.full_name,
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    session = UserSession(
        user_id=user.id,
        session_token=generate_session_token(),
        expires_at=get_session_expiry(),
    )
    db.add(session)
    db.commit()

    response.set_cookie(
        key=settings.session_cookie_name,
        value=session.session_token,
        httponly=True,
        samesite='lax',
        max_age=settings.session_expire_hours * 3600,
    )
    return {'message': 'Account created successfully', 'user': user}


@router.post('/login', response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid email or password')

    session = UserSession(
        user_id=user.id,
        session_token=generate_session_token(),
        expires_at=get_session_expiry(),
    )
    db.add(session)
    db.commit()

    response.set_cookie(
        key=settings.session_cookie_name,
        value=session.session_token,
        httponly=True,
        samesite='lax',
        max_age=settings.session_expire_hours * 3600,
    )
    return {'message': 'Logged in successfully', 'user': user}


@router.post('/logout')
def logout(
    response: Response,
    db: Session = Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
):
    if session_token:
        db.query(UserSession).filter(UserSession.session_token == session_token).delete()
        db.commit()
    response.delete_cookie(settings.session_cookie_name)
    return {'message': 'Logged out successfully'}


@router.get('/me', response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
