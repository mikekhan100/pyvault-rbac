## ⚙️ Setup & Installation
1. **Clone the repository:**
git clone https://github.com/mikekhan100/pyvault-rbac.git
cd pyvault-rbac

2. **Set up Virtual Environment (PowerShell):**
python -m venv venv
.\venv\Scripts\Activate.ps1

3. **Install Dependencies:**
pip install -r requirements.txt

4. **Configure Environment Variables:**
Create a .env file in the root directory:
SECRET_KEY=your_super_secret_vault_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

## 🔐 How it Works
1. **The Token (Key)**
When a user logs in via /token, they receive a JWT.

Admin Login: (Username: admin) returns scopes: ["user:read", "user:admin"]

Guest Login: (Username: guest) returns scopes: ["user:read"]

2. **The Gatekeeper**
The get_current_user dependency in deps.py intercepts requests to protected routes.  It decodes the JWT and verifies if the required scope exists in the token payload.

3. **The Vault Doors**
GET /vault/public-records: Requires user:read.

GET /vault/top-secret: Requires user:admin.

## 🧪 Testing the Vault
1. **Start the server:**
uvicorn app.main:app --reload

2. **Navigate to http://127.0.0.1:8000/docs**

3. **Try accessing /vault/top-secret (It will be blocked).**

4. **Click Authorise, login as admin, and try again!**

## 📜 License
MIT