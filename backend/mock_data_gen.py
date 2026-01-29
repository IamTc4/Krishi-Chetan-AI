import json
import random

# Constants for generating realistic data
CROPS = ["Wheat", "Rice", "Sugarcane", "Cotton", "Soybean", "Maize", "Tomato", "Onion"]
LOCATIONS = [
    {"name": "Satara", "lat": 17.68, "lng": 74.00},
    {"name": "Koregaon", "lat": 17.70, "lng": 74.08},
    {"name": "Wai", "lat": 17.94, "lng": 73.89},
    {"name": "Mahabaleshwar", "lat": 17.92, "lng": 73.65},
    {"name": "Karad", "lat": 17.29, "lng": 74.20},
    {"name": "Phaltan", "lat": 17.98, "lng": 74.43}
]
STAGES = ["Vegetative", "Flowering", "Harvesting", "Sowing"]
SOILS = ["Black Soil", "Red Soil", "Alluvial", "Clay"]

def generate_farmers(count=50):
    farmers = {}
    for i in range(count):
        phone = f"98765{str(i).zfill(5)}"
        loc = random.choice(LOCATIONS)
        
        # Vary location slightly for map clusters
        lat_offset = random.uniform(-0.05, 0.05)
        lng_offset = random.uniform(-0.05, 0.05)
        
        farmer = {
            "phone": phone,
            "password": "pass", # Dummy
            "role": "farmer",
            "name": f"Farmer {i+1}",
            "location": loc["name"],
            "lat": loc["lat"] + lat_offset,
            "lng": loc["lng"] + lng_offset, 
            "crop_type": random.choice(CROPS),
            "land_size": round(random.uniform(0.5, 10.0), 1),
            "sowing_date": "2025-11-15",
            "soil_type": random.choice(SOILS),
            "growth_stage": random.choice(STAGES),
            # Risk Simulation
            "risk_score": random.randint(0, 100), 
            "advisory_history": [] 
        }

        # Simulate Advisory History & Adoption
        num_advisories = random.randint(1, 5)
        for _ in range(num_advisories):
            status = random.choice(["pending", "followed", "ignored"])
            farmer["advisory_history"].append({
                "id": f"adv_{random.randint(1000,9999)}",
                "type": random.choice(["Pest", "Weather", "Irrigation"]),
                "message": "Sample advisory message",
                "date": "2026-01-10",
                "status": status
            })

        farmers[phone] = farmer
    
    return farmers

if __name__ == "__main__":
    data = generate_farmers(60)
    with open("services/auth_db.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Generated 60 farmers in services/auth_db.json")
