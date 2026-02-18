"""
Authentication API Endpoints
POST /api/v1/auth/register - Register new user
POST /api/v1/auth/login - Authenticate user and return JWT tokens
POST /api/v1/auth/refresh - Refresh access token
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from src.services.auth_service import AuthService
from src.core.security import decode_token, create_access_token
from src.middleware.rate_limit import rate_limit_login, rate_limit_register

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_register)],
)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    Register a new user account

    - **email**: Valid email address (unique)
    - **password**: Minimum 8 characters

    Returns JWT access and refresh tokens

    Rate limit: 3 attempts per hour per IP
    """
    try:
        user = await AuthService.register_user(db, request)
        tokens = AuthService.create_tokens(user)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse, dependencies=[Depends(rate_limit_login)])
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return JWT tokens

    - **email**: Registered email address
    - **password**: User's password

    Returns JWT access and refresh tokens

    Rate limit: 5 attempts per 15 minutes per email (FR-000g)
    """
    user = await AuthService.authenticate_user(db, request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = AuthService.create_tokens(user)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token

    - **refresh_token**: Valid JWT refresh token

    Returns new access token (refresh token remains the same)
    """
    # Decode refresh token
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    token_data = {"sub": payload.get("sub"), "email": payload.get("email")}
    new_access_token = create_access_token(token_data)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=request.refresh_token,  # Keep same refresh token
        token_type="bearer",
    )
