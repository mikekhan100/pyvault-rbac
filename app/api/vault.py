from fastapi import APIRouter, Security, Depends
from app.api.deps import get_current_user
from app.schemas.user import TokenData

router = APIRouter(prefix="/vault", tags=["Vault"])

@router.get("/public-records")
async def read_public_vault(
    current_user: TokenData = Security(get_current_user, scopes=["user:read"])
):
    """
    This door requires 'user:read' clearance.
    """
    return {
        "access": "Granted",
        "data": "This is semi-sensitive information for all vault members.",
        "user": current_user.username
    }

@router.get("/top-secret")
async def read_private_vault(
    current_user: TokenData = Security(get_current_user, scopes=["user:admin"])
):
    """
    This door requires 'user:admin' clearance.
    """
    return {
        "access": "Granted",
        "secret_data": "The vault combination is 42-13-37.",
        "admin_id": current_user.username
    }