from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="Krishi-Chetan AI API",
    description="Edge-AI Local Backend for Farmers",
    version="0.1.0"
)

# CORS - Allow all for local dev ease
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static assets (CSS, JS, Images)
# We mount the entire frontend directory to / (so style.css is at /style.css)
# However, mounting at "/" overrides all other routes if not careful.
# Better strategy: Mount specific assets or just everything as a fallback?
# FASTAPI StaticFiles matches typically take precedence if mounted at root. 
# But we want specific API routes too.

# Solution: Mount assets to root but after API routes? 
# Actually, standard practice for SPA/Static + API:
# API routes first. 
# Then StaticFiles for assets.
# Then a catch-all for index.html (if SPA routing) or just serve index.html at root.

# Here we have flat files: style.css, app.js at root of frontend.
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# We want style.css to be found at check relative links in index.html.
# In index.html: <link rel="stylesheet" href="style.css">
# So we need to serve from root.

# --- Module: Authentication ---
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from services.auth import auth_service, UserRegister, Token, UserLogin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # In a real app we decode token here. 
    # For now, just a placeholder as we aren't fully validating on every request in this MVP
    # But ideally:
    # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return token 

@app.post("/api/auth/register", response_model=dict)
def register(user: UserRegister):
    user_entry = auth_service.register_user(user)
    if not user_entry:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return {"msg": "User created successfully", "phone": user.phone}

@app.post("/api/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # We use form_data.username as the phone number
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={"sub": user["phone"], "role": user["role"], "name": user["name"]}
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user_name": user["name"], 
        "role": user["role"]
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# --- Module A: AI Diagnostic Engine ---
from services.vision import vision_service
from services.soil import soil_service
from pydantic import BaseModel

class SoilData(BaseModel):
    rainfall: float
    ph: float
    n: float
    p: float
    crop_name: str = "Wheat"

@app.post("/api/diagnose/leaf")
def diagnose_leaf(lang: str = "en"):
    # In a real app, we'd accept an UploadFile
    # For this demo, we just trigger the mock service
    result = vision_service.predict(None, lang)
    return result

@app.post("/api/analyze/soil")
def analyze_soil(data: SoilData, lang: str = "en"):
    result = soil_service.recommend(data.dict(), lang)
    return result

# --- Module B: Market & Subsidy Intelligence ---
from services.market import market_service

class SubsidyQuery(BaseModel):
    land_size: float
    category: str = "General"

@app.get("/api/market/prices")
def get_market_prices(lang: str = "en"):
    return market_service.get_prices(lang)

@app.get("/api/market/news")
def get_news(lang: str = "en"):
    return market_service.get_news(lang)

@app.get("/api/market/retailers")
def get_retailers():
    return market_service.get_retailers()

@app.post("/api/subsidy/check")
def check_subsidy(query: SubsidyQuery, lang: str = "en"):
    # Log valid subsidies to blockchain
    result = market_service.check_subsidy(query.land_size, query.category, lang)
    if result:
        ledger_service.add_transaction({"event": "Subsidy Checked", "eligible": True, "land": query.land_size})
    return result

# --- Module C: Irrigation & Transparency ---
from services.irrigation import irrigation_service
from services.blockchain import ledger_service

class WeatherData(BaseModel):
    temp: float
    humidity: float
    wind: float
    sun_hours: float

@app.post("/api/irrigate/calc")
def calculate_irrigation(data: WeatherData):
    return irrigation_service.calculate_water_need(data.temp, data.humidity, data.wind, data.sun_hours)

@app.get("/api/transparency/ledger")
def get_ledger():
    return ledger_service.get_chain()

# --- Module D: Officer & Governance ---
from services.officer import officer_service
from services.fertilizer import fertilizer_service

@app.get("/api/officer/heatmap")
def get_heatmap():
    return officer_service.get_outbreak_heatmap()

@app.get("/api/officer/alerts")
def get_alerts(lang: str = "en"):
    return officer_service.get_alerts(lang)

class BulkAdvisoryRequest(BaseModel):
    phones: List[str]
    advisory: Advisory

@app.post("/api/officer/send-advisory")
def send_bulk_advisory(req: BulkAdvisoryRequest):
    """Send advisory to multiple farmers"""
    results = []
    for phone in req.phones:
        result = farmer_service.add_advisory(phone, req.advisory)
        results.append({"phone": phone, "status": result["status"]})
    return {"sent": len(results), "results": results}

# --- Module E: Farmer Features ---
from services.farmer import farmer_service, FarmerProfile, Advisory
from services.weather import weather_service

@app.post("/api/farmer/profile")
def save_farmer_profile(profile: FarmerProfile):
    """Save farmer profile"""
    return farmer_service.save_profile(profile)

@app.get("/api/farmer/profile/{phone}")
def get_farmer_profile(phone: str):
    """Get farmer profile"""
    profile = farmer_service.get_profile(phone)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.get("/api/farmer/sowing-recommendation")
def get_sowing_rec(crop: str, location: str, lang: str = "en"):
    """Get best sowing time"""
    return farmer_service.get_sowing_recommendation(crop, location, lang)

@app.get("/api/farmer/fertilizer-dosage")
def get_fertilizer_dosage(crop: str, land_size: float, stage: str, lang: str = "en"):
    """Get fertilizer recommendations"""
    return farmer_service.get_fertilizer_dosage(crop, land_size, stage, lang)

@app.post("/api/farmer/advisory")
def add_advisory(phone: str, advisory: Advisory):
    """Add advisory to history"""
    return farmer_service.add_advisory(phone, advisory)

@app.get("/api/farmer/advisory-history/{phone}")
def get_advisory_history(phone: str, limit: int = 10):
    """Get advisory history"""
    return farmer_service.get_advisory_history(phone, limit)

@app.post("/api/farmer/advisory/{phone}/{id}/status")
def update_advisory_status(phone: str, id: str, status: str):
    """Update advisory status (followed/ignored)"""
    return farmer_service.update_advisory_status(phone, id, status)

# --- Module F: Officer Features ---
@app.get("/api/officer/farmers")
def get_farmers():
    # Load from the file we just generated/updated
    if os.path.exists("services/auth_db.json"):
        with open("services/auth_db.json", "r") as f:
            db = json.load(f)
            return [v for v in db.values() if v.get("role") == "farmer"]
    return []

@app.get("/api/officer/crop-patterns")
def get_crop_patterns():
    # Calculate real stats from DB
    if os.path.exists("services/auth_db.json"):
        with open("services/auth_db.json", "r") as f:
            db = json.load(f)
            farmers = [v for v in db.values() if v.get("role") == "farmer"]
            
            counts = {}
            for fam in farmers:
                c = fam.get("crop_type", "Unknown")
                counts[c] = counts.get(c, 0) + 1
            
            # Convert to percentages
            total = len(farmers)
            if total > 0:
                return {k: round((v/total)*100, 1) for k, v in counts.items()}
    
    return {"Wheat": 0} # Fallback

@app.get("/api/officer/priority-list")
def get_priority_list():
    if os.path.exists("services/auth_db.json"):
        with open("services/auth_db.json", "r") as f:
            db = json.load(f)
            farmers = [v for v in db.values() if v.get("role") == "farmer"]
            
            # Calculate Global Adoption
            total_adv = 0
            followed_adv = 0
            for fam in farmers:
                hist = fam.get("advisory_history", [])
                total_adv += len(hist)
                followed_adv += len([h for h in hist if h["status"] == "followed"])
            
            adoption_rate = round((followed_adv / total_adv * 100), 1) if total_adv > 0 else 0
            
            # Filter High Risk
            priority = []
            for fam in farmers:
                risk = fam.get("risk_score", 0)
                # Logic: High risk score OR many ignored advisories
                ignored = len([h for h in fam.get("advisory_history", []) if h["status"] == "ignored"])
                if risk > 60 or ignored >= 1: 
                    priority.append({
                        "name": fam.get("name"),
                        "phone": fam.get("phone"),
                        "location": fam.get("location", "Satara"),
                        "risk_score": risk,
                        "reason": f"{ignored} Ignored Advisories" if ignored >= 1 else "High Pest Risk Prediction"
                    })
            
            # Sort by risk
            priority.sort(key=lambda x: x["risk_score"], reverse=True)
            
            return {
                "priority_list": priority[:20], # Top 20
                "metrics": {
                    "adoption_rate": adoption_rate,
                    "total_farmers": len(farmers)
                }
            }
    return {"priority_list": [], "metrics": {"adoption_rate": 0, "total_farmers": 0}}
            
    # Calculate Global Adoption Rate
    total_followed = 0
    total_advisories = 0
    for phone in farmer_service.advisories:
        for adv in farmer_service.advisories[phone]:
            total_advisories += 1
            if adv.get("status") == "followed":
                total_followed += 1
    
    adoption_rate = (total_followed / total_advisories * 100) if total_advisories > 0 else 0
            
    return {
        "priority_list": priority,
        "metrics": {
            "adoption_rate": round(adoption_rate, 1),
            "total_farmers": len(all_farmers)
        }
    }

@app.get("/api/officer/pending-recs")
def get_pending_recs():
    return officer_service.get_pending_recs()

@app.post("/api/officer/validate-rec/{rec_id}")
def validate_rec(rec_id: str, new_text: str):
    return officer_service.validate_rec(rec_id, new_text)

@app.get("/api/weather/warnings")
def get_weather_warnings(location: str, lang: str = "en"):
    """Get extreme weather warnings"""
    return weather_service.get_extreme_warnings(location, lang)

@app.post("/api/weather/irrigation-schedule")
def get_irrigation_schedule(crop: str, soil_type: str, weather: dict, lang: str = "en"):
    """Get irrigation schedule"""
    return weather_service.get_irrigation_schedule(crop, soil_type, weather, lang)

# --- Module F: Officer Features ---
@app.get("/api/officer/farmers")
def get_all_farmers():
    """Get all registered farmers"""
    from services.auth import auth_service
    farmers = [u for u in auth_service.users_db.values() if u.get("role") == "farmer"]
    return farmers

@app.post("/api/officer/send-advisory")
def send_bulk_advisory(phones: List[str], advisory: Advisory):
    """Send advisory to multiple farmers"""
    results = []
    for phone in phones:
        result = farmer_service.add_advisory(phone, advisory)
        results.append({"phone": phone, "status": result["status"]})
    return {"sent": len(results), "results": results}

from typing import List

# Serve specific files for the root access
@app.get("/")
async def read_index():
    return FileResponse("../frontend/index.html")

# --- Module: Chat ---
from services.chat import chat_service, ChatMessage, ChatResponse

@app.post("/api/chat/ask", response_model=ChatResponse)
def ask_chat(msg: ChatMessage):
    # Detect language basic check (optional, rely on frontend passing it)
    return chat_service.get_response(msg.message, msg.language)

# Serve specific files for the root access
@app.get("/")
async def read_index():
    return FileResponse("../frontend/index.html")

@app.get("/login.html")
async def read_login():
    return FileResponse("../frontend/login.html")

@app.get("/style.css")
async def read_css():
    return FileResponse("../frontend/style.css")

@app.get("/app.js")
async def read_js():
    return FileResponse("../frontend/app.js")

@app.get("/translations.js")
async def read_trans():
    return FileResponse("../frontend/translations.js")

# Mount a catch-all if needed, but for now specific files are safer to avoid conflicts
