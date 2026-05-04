from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api import vault
from app.core.security import create_access_token
from datetime import timedelta

app = FastAPI(title="pyvault-rbac")

# 1. Include our protected "Vault" doors
app.include_router(vault.router)

# 2. Create the Login (Token) Endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Mock Login: 
    - username 'admin' gets admin scopes
    - anything else gets guest scopes
    """
    # In a real app, you would verify the password with verify_password() here
    if form_data.username == "admin":
        user_scopes = ["user:read", "user:admin"]
    else:
        user_scopes = ["user:read"]

    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": user_scopes}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def root():
    return {"message": "The Vault is Online. Visit /docs to authenticate."}