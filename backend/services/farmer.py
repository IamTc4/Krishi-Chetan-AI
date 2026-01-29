from pydantic import BaseModel
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Optional, List, Dict

# Farmer Profile Model
class FarmerProfile(BaseModel):
    phone: str
    crop_type: str
    location: str
    sowing_date: str  # ISO format
    land_size: float  # acres
    growth_stage: str = "seedling"  # seedling, vegetative, flowering, harvest
    soil_type: str = "loamy"

class Advisory(BaseModel):
    date: str
    type: str  # irrigation, fertilizer, pesticide, weather, pest
    message: str
    language: str = "en"

# Persistent storage
PROFILES_FILE = Path(__file__).parent / "farmer_profiles.json"
ADVISORIES_FILE = Path(__file__).parent / "farmer_advisories.json"

class FarmerService:
    def __init__(self):
        self.profiles = self._load_profiles()
        self.advisories = self._load_advisories()
    
    def _load_profiles(self) -> Dict[str, dict]:
        if PROFILES_FILE.exists():
            with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_profiles(self):
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, indent=2, ensure_ascii=False)
    
    def _load_advisories(self) -> Dict[str, List[dict]]:
        if ADVISORIES_FILE.exists():
            with open(ADVISORIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_advisories(self):
        with open(ADVISORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.advisories, f, indent=2, ensure_ascii=False)
    
    def save_profile(self, profile: FarmerProfile):
        """Save or update farmer profile"""
        self.profiles[profile.phone] = profile.dict()
        self._save_profiles()
        return {"status": "success", "message": "Profile saved"}
    
    def get_profile(self, phone: str):
        """Get farmer profile"""
        return self.profiles.get(phone)
    
    def get_sowing_recommendation(self, crop: str, location: str, lang: str = "en"):
        """Best time for sowing based on crop and location"""
        # Simplified recommendations (in production, use weather data + crop calendar)
        sowing_calendar = {
            "Tomato": {"best_months": ["October", "November"], "avoid": "Monsoon"},
            "Wheat": {"best_months": ["October", "November"], "avoid": "Summer"},
            "Rice": {"best_months": ["June", "July"], "avoid": "Winter"},
            "Onion": {"best_months": ["November", "December"], "avoid": "Monsoon"},
            "Cotton": {"best_months": ["May", "June"], "avoid": "Winter"}
        }
        
        crop_info = sowing_calendar.get(crop, {"best_months": ["Consult local expert"], "avoid": "N/A"})
        
        translations = {
            "en": {
                "title": f"Best Sowing Time for {crop}",
                "best": f"Optimal months: {', '.join(crop_info['best_months'])}",
                "avoid": f"Avoid: {crop_info['avoid']}"
            },
            "hi": {
                "title": f"{crop} के लिए सबसे अच्छा बुवाई का समय",
                "best": f"इष्टतम महीने: {', '.join(crop_info['best_months'])}",
                "avoid": f"बचें: {crop_info['avoid']}"
            },
            "mr": {
                "title": f"{crop} साठी सर्वोत्तम पेरणी वेळ",
                "best": f"इष्टतम महिने: {', '.join(crop_info['best_months'])}",
                "avoid": f"टाळा: {crop_info['avoid']}"
            }
        }
        
        t = translations.get(lang, translations["en"])
        return {
            "crop": crop,
            "location": location,
            "recommendation": t["best"],
            "warning": t["avoid"],
            "details": "Based on regional climate patterns"
        }
    
    def get_fertilizer_dosage(self, crop: str, land_size: float, stage: str, lang: str = "en"):
        """Fertilizer recommendations based on crop, land, and growth stage"""
        # Simplified dosage (kg per acre)
        dosage_table = {
            "Tomato": {"seedling": {"N": 20, "P": 30, "K": 20}, "vegetative": {"N": 40, "P": 20, "K": 30}, "flowering": {"N": 30, "P": 40, "K": 40}},
            "Wheat": {"seedling": {"N": 30, "P": 25, "K": 15}, "vegetative": {"N": 40, "P": 15, "K": 20}, "flowering": {"N": 25, "P": 30, "K": 25}},
            "Rice": {"seedling": {"N": 25, "P": 30, "K": 20}, "vegetative": {"N": 50, "P": 20, "K": 30}, "flowering": {"N": 30, "P": 35, "K": 35}}
        }
        
        dosage = dosage_table.get(crop, dosage_table["Tomato"]).get(stage, {"N": 30, "P": 25, "K": 20})
        total = {k: v * land_size for k, v in dosage.items()}
        
        translations = {
            "en": {
                "title": f"Fertilizer Dosage for {crop} ({stage} stage)",
                "urea": f"Urea (46% N): {round(total['N'] / 0.46, 1)} kg",
                "dap": f"DAP (18% N, 46% P): {round(total['P'] / 0.46, 1)} kg",
                "mop": f"MOP (60% K): {round(total['K'] / 0.60, 1)} kg"
            },
            "hi": {
                "title": f"{crop} के लिए उर्वरक खुराक ({stage} चरण)",
                "urea": f"यूरिया: {round(total['N'] / 0.46, 1)} किलो",
                "dap": f"डीएपी: {round(total['P'] / 0.46, 1)} किलो",
                "mop": f"एमओपी: {round(total['K'] / 0.60, 1)} किलो"
            },
            "mr": {
                "title": f"{crop} साठी खत डोस ({stage} टप्पा)",
                "urea": f"युरिया: {round(total['N'] / 0.46, 1)} किलो",
                "dap": f"डीएपी: {round(total['P'] / 0.46, 1)} किलो",
                "mop": f"एमओपी: {round(total['K'] / 0.60, 1)} किलो"
            }
        }
        
        t = translations.get(lang, translations["en"])
        return {
            "crop": crop,
            "land_size": land_size,
            "stage": stage,
            "recommendation": [t["urea"], t["dap"], t["mop"]],
            "note": "Apply in split doses for better efficiency"
        }
    
    def add_advisory(self, phone: str, advisory: Advisory):
        """Add advisory to history"""
        if phone not in self.advisories:
            self.advisories[phone] = []
        
        # Add ID for tracking
        adv_dict = advisory.dict()
        adv_dict["id"] = f"{int(datetime.now().timestamp())}_{phone}"
        adv_dict["status"] = "pending" # pending, followed, ignored
        
        self.advisories[phone].append(adv_dict)
        self._save_advisories()
        return {"status": "success", "id": adv_dict["id"]}
    
    def update_advisory_status(self, phone: str, advisory_id: str, status: str):
        """Update status of an advisory (followed/ignored)"""
        if phone in self.advisories:
            for adv in self.advisories[phone]:
                if adv.get("id") == advisory_id:
                    adv["status"] = status
                    self._save_advisories()
                    return {"status": "success", "new_status": status}
        return {"status": "error", "message": "Advisory not found"}

    def get_advisory_history(self, phone: str, limit: int = 10):
        """Get recent advisories"""
        history = self.advisories.get(phone, [])
        return history[-limit:]  # Last N advisories

farmer_service = FarmerService()
