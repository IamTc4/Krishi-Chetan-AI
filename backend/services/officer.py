from typing import List, Dict

class OfficerIntelligence:
    def __init__(self):
        self.pending_recs = [
            {"id": "ai_1", "farmer": "9876543210", "type": "Soil AI", "recommendation": "Use 20kg extra Urea for Wheat.", "status": "pending"},
            {"id": "ai_2", "farmer": "9876543210", "type": "Doctor AI", "recommendation": "Spray Copper Oxychloride for Blight.", "status": "pending"}
        ]

    def get_pending_recs(self):
        return [r for r in self.pending_recs if r["status"] == "pending"]

    def validate_rec(self, rec_id: str, new_text: str):
        for r in self.pending_recs:
            if r["id"] == rec_id:
                r["recommendation"] = new_text
                r["status"] = "validated"
                return {"status": "success", "rec": r}
        return {"status": "error"}

    def get_outbreak_heatmap(self):
        """
        Generates GeoJSON-like data for Pest Outbreaks.
        Simulates PostGIS spatial query.
        """
        # Mock coordinates around Satara, Maharashtra
        base_lat = 17.68
        base_lng = 74.00
        
        outbreaks = []
        for i in range(5):
            outbreaks.append({
                "lat": base_lat + random.uniform(-0.05, 0.05),
                "lng": base_lng + random.uniform(-0.05, 0.05),
                "intensity": random.randint(1, 10), # 10 = High Risk
                "pest": "Fall Armyworm",
                "radius": 500 # meters
            })
            
        return outbreaks

    def get_alerts(self, lang="en"):
        # Localized Alerts
        alerts = {
            "en": [
                {"zone": "Zone A (North)", "risk": "High", "prediction": "Fungal Blight likely in 48 hrs."},
                {"zone": "Zone B (West)", "risk": "Low", "prediction": "Conditions stable."}
            ],
            "hi": [
                {"zone": "जोन ए (उत्तर)", "risk": "उच्च", "prediction": "48 घंटे में फंगल ब्लाइट की संभावना।"},
                {"zone": "जोन बी (पश्चिम)", "risk": "कम", "prediction": "स्थिति सामान्य है।"}
            ],
            "mr": [
                {"zone": "झोन ए (उत्तर)", "risk": "जास्त", "prediction": "४८ तासांत करपा रोगाची शक्यता."},
                {"zone": "झोन बी (पश्चिम)", "risk": "कमी", "prediction": "परिस्थिती सामान्य आहे."}
            ]
        }
        return alerts.get(lang, alerts["en"])

officer_service = OfficerIntelligence()
