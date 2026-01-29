from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from pydantic import BaseModel
import json
import hashlib
from pathlib import Path

# Configuration
SECRET_KEY = "krishi-chetan-secret-key-change-this-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

# Salt for password hashing (in production, use individual salts per user)
PASSWORD_SALT = "krishi-chetan-salt-2024"

# Models
class UserLogin(BaseModel):
    phone: str
    password: str

class UserRegister(BaseModel):
    phone: str
    password: str
    name: str
    role: str = "farmer"  # farmer or officer

class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str
    role: str

# Persistent JSON Database
USERS_DB_FILE = Path(__file__).parent / "users.json"

class AuthService:
    def __init__(self):
        self.users_db = self._load_users()
        
    def _load_users(self) -> Dict[str, dict]:
        """Load users from JSON file, create default users if file doesn't exist"""
        if USERS_DB_FILE.exists():
            try:
                with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                    users = json.load(f)
                    print(f"✓ Loaded {len(users)} users from database")
                    return users
            except Exception as e:
                print(f"⚠ Error loading users: {e}")
                return {}
        else:
            # Create default test users
            print("Creating default test users...")
            default_users = self._create_default_users()
            self._save_users(default_users)
            return default_users
    
    def _create_default_users(self) -> Dict[str, dict]:
        """Create default test accounts for immediate testing"""
        default_users = {}
        
        # Default Farmer account
        farmer_pw = self.get_password_hash("farmer123")
        default_users["9876543210"] = {
            "phone": "9876543210",
            "name": "Test Farmer",
            "role": "farmer",
            "hashed_password": farmer_pw
        }
        
        # Default Officer account
        officer_pw = self.get_password_hash("officer123")
        default_users["9876543211"] = {
            "phone": "9876543211",
            "name": "Test Officer",
            "role": "officer",
            "hashed_password": officer_pw
        }
        
        print("✓ Created default test accounts:")
        print("  Farmer: 9876543210 / farmer123")
        print("  Officer: 9876543211 / officer123")
        
        return default_users
    
    def _save_users(self, users: Dict[str, dict] = None):
        """Save users to JSON file"""
        try:
            users_to_save = users if users is not None else self.users_db
            with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(users_to_save, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(users_to_save)} users to database")
        except Exception as e:
            print(f"✗ Error saving users: {e}")
    
    def verify_password(self, plain_password, hashed_password):
        """Verify password using SHA256"""
        hashed_input = hashlib.sha256((plain_password + PASSWORD_SALT).encode()).hexdigest()
        return hashed_input == hashed_password

    def get_password_hash(self, password):
        """Hash password using SHA256 (simple for demo, use bcrypt in production)"""
        return hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def register_user(self, user: UserRegister):
        """Register a new user with persistent storage"""
        if user.phone in self.users_db:
            print(f"⚠ Registration failed: Phone {user.phone} already registered")
            return None  # User already exists
        
        hashed_pw = self.get_password_hash(user.password)
        user_entry = {
            "phone": user.phone,
            "name": user.name,
            "role": user.role,
            "hashed_password": hashed_pw
        }
        self.users_db[user.phone] = user_entry
        self._save_users()  # Persist to file
        print(f"✓ New user registered: {user.name} ({user.phone}) - Role: {user.role}")
        return user_entry

    def authenticate_user(self, phone: str, password: str):
        """Authenticate user with improved logging"""
        user = self.users_db.get(phone)
        if not user:
            print(f"✗ Login failed: Phone {phone} not found")
            return False
        if not self.verify_password(password, user["hashed_password"]):
            print(f"✗ Login failed: Invalid password for {phone}")
            return False
        print(f"✓ Login successful: {user['name']} ({phone}) - Role: {user['role']}")
        return user

auth_service = AuthService()
