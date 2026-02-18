"""
Rate Limiting Middleware
Prevents brute force attacks on auth endpoints
"""
from typing import Dict
from datetime import datetime, timedelta
from fastapi import HTTPException, Request, status


class RateLimiter:
    """
    Simple in-memory rate limiter
    Production: Use Redis or similar for distributed rate limiting
    """

    def __init__(self):
        # Store: {identifier: [(timestamp1, timestamp2, ...)]}
        self.requests: Dict[str, list] = {}

    def _clean_old_requests(self, identifier: str, window_seconds: int):
        """Remove requests outside the time window"""
        if identifier not in self.requests:
            return

        cutoff_time = datetime.utcnow() - timedelta(seconds=window_seconds)
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] if req_time > cutoff_time
        ]

    def check_rate_limit(
        self, identifier: str, max_requests: int, window_seconds: int
    ) -> bool:
        """
        Check if request is within rate limit

        Args:
            identifier: Unique identifier (email, IP, user_id)
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds

        Returns:
            True if allowed, False if rate limit exceeded
        """
        # Clean old requests
        self._clean_old_requests(identifier, window_seconds)

        # Initialize if new identifier
        if identifier not in self.requests:
            self.requests[identifier] = []

        # Check limit
        if len(self.requests[identifier]) >= max_requests:
            return False

        # Add current request
        self.requests[identifier].append(datetime.utcnow())
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_login(request: Request):
    """
    Rate limit for login endpoint
    FR-000g: 5 attempts per 15 minutes per email

    Usage:
        @router.post("/login", dependencies=[Depends(rate_limit_login)])
        async def login(...):
            ...
    """
    # Get email from request body
    body = await request.json()
    email = body.get("email", "")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required"
        )

    # Check rate limit: 5 requests per 15 minutes (900 seconds)
    allowed = rate_limiter.check_rate_limit(
        identifier=f"login:{email}", max_requests=5, window_seconds=900
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again in 15 minutes.",
        )


async def rate_limit_register(request: Request):
    """
    Rate limit for register endpoint
    3 attempts per hour per IP

    Usage:
        @router.post("/register", dependencies=[Depends(rate_limit_register)])
        async def register(...):
            ...
    """
    # Get client IP
    client_ip = request.client.host

    # Check rate limit: 3 requests per hour (3600 seconds)
    allowed = rate_limiter.check_rate_limit(
        identifier=f"register:{client_ip}", max_requests=3, window_seconds=3600
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again in 1 hour.",
        )
