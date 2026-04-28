from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from pydantic import ValidationError
from app.core.security import SECRET_KEY, ALGORITHM
from app.schemas.user import TokenData

# Defines where the user goes to get their key (the /token endpoint)
# We also define what 'Clearance Levels' exist in our Vault system
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "user:read": "Read-only access to vault items.",
        "user:admin": "Full administrative control over the vault.",
    },
)

async def get_current_user(
    security_scopes: SecurityScopes, 
    token: str = Depends(oauth2_scheme)
):
    # Standard 401 error if the token is missing or broken
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        # Decode the token using our Master Secret Key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # Get the scopes stored inside the token
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
        
    except (JWTError, ValidationError):
        raise credentials_exception

    # RBAC LOGIC: Check if the user has the SPECIFIC clearance required for this door
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient clearance! You do not have the required permissions.",
                headers={"WWW-Authenticate": authenticate_value},
            )
            
    return token_data