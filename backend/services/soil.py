class SoilAnalyzer:
    def __init__(self):
        pass

    def calculate_csi(self, rainfall, soil_ph, nitrogen, phosphorous):
        """
        Calculate Crop Suitability Index (CSI) - Weighted Mean.
        Formula: CSI = Sum(w_i * S_i) / Sum(w_i)
        """
        # Weights (w_i)
        w_rain = 0.4
        w_ph = 0.3
        w_n = 0.2
        w_p = 0.1
        total_weight = w_rain + w_ph + w_n + w_p
        
        # Normalized Scores (S_i) 0.0 to 1.0
        # Example for 'Wheat'
        s_rain = min(rainfall / 200, 1.0)
        s_ph = 1.0 - abs(6.5 - soil_ph) / 6.5 # Optimal 6.5
        s_n = min(nitrogen / 120, 1.0)
        s_p = min(phosphorous / 60, 1.0)
        
        numerator = (w_rain * s_rain) + (w_ph * s_ph) + (w_n * s_n) + (w_p * s_p)
        csi = numerator / total_weight
        
        return round(csi, 3)

    def recommend(self, data, lang="en"):
        rain = data.get('rainfall', 100)
        ph = data.get('ph', 6.5)
        n = data.get('n', 50)
        p = data.get('p', 20)
        crop = data.get('crop_name', 'Wheat')
        
        csi = self.calculate_csi(rain, ph, n, p)
        
        # Translation
        status_map = {
            "en": {
                "high": f"Highly Recommended for {crop} (> 0.75)",
                "med": f"Moderately Suitable for {crop}",
                "low": f"Not Recommended for {crop}"
            },
            "hi": {
                "high": f"{crop} के लिए अत्यधिक अनुशंसित (> 0.75)",
                "med": f"{crop} के लिए मध्यम उपयुक्त",
                "low": f"{crop} के लिए अनुशंसित नहीं"
            },
            "mr": {
                "high": f"{crop} साठी अत्यंत शिफारस केलेले (> 0.75)",
                "med": f"{crop} साठी मध्यम योग्य",
                "low": f"{crop} साठी शिफारस केलेली नाही"
            }
        }
        t = status_map.get(lang, status_map["en"])

        rec_status = t["low"]
        if csi > 0.75:
            rec_status = t["high"]
        elif csi > 0.50:
             rec_status = t["med"]
             
        return {
            "csi_score": csi,
            "crop": crop,
            "status": rec_status,
            "details": "Calculated via Weighted Ensemble Model"
        }

soil_service = SoilAnalyzer()
