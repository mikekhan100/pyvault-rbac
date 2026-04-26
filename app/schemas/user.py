from pydantic import BaseModel, EmailStr
from typing import List, Optional

# This is the base data shared across all user types
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

# This is what we require when a user "Registers" for the Vault
class UserCreate(UserBase):
    password: str

# This is the "Identity Card" returned by the Vault
# It contains the 'scopes' which define their RBAC permissions
class UserOut(UserBase):
    id: int
    is_active: bool = True
    scopes: List[str] = [] # e.g., ["user:read", "vault:admin"]

    class Config:
        # This allows Pydantic to work with database objects (ORMs)
        from_attributes = True

# This represents the data stored inside the JWT token
class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []