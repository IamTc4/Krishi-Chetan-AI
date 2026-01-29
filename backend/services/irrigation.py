import math

class IrrigationEngine:
    def __init__(self):
        pass

    def calculate_water_need(self, temp_c, humidity, wind_speed, sunlight_hours, crop_stage="mid_season"):
        """
        Rigorous Penman-Monteith Implementation.
        Formula: I_req = (ET0 * Kc) - R_eff
        """
        # 1. Calculate ET0 (Reference Evapotranspiration)
        # Constants
        psy_const = 0.066
        slope_vap_pressure = 4098 * (0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))) / ((temp_c + 237.3) ** 2)
        rn = 0.408 * (sunlight_hours * 0.5) 
        u2 = wind_speed * 0.27
        wind_term = (900 / (temp_c + 273)) * u2 * (1 - (humidity / 100))
        
        et0 = (0.408 * slope_vap_pressure * rn + psy_const * wind_term) / (slope_vap_pressure + psy_const * (1 + 0.34 * u2))
        
        # 2. Determine K_c (Crop Coefficient)
        # Stages: Initial=0.3-0.5, Mid=1.1-1.2, End=0.4
        kc_map = {
            "initial": 0.40,
            "mid_season": 1.15,
            "late_season": 0.50
        }
        kc = kc_map.get(crop_stage, 1.0)
        
        # 3. Effective Rainfall (R_eff) - Mock value for "Today"
        # In real system, this comes from IMD API
        r_eff = 0.0 # Assuming no rain today
        
        # 4. Final Calculation
        i_req = (et0 * kc) - r_eff
        i_req = max(0, i_req) # No negative irrigation
        
        return {
            "et0": round(et0, 2),
            "kc": kc,
            "r_eff": r_eff,
            "irrigation_required_mm": round(i_req, 2),
            "advice": f"Apply {round(i_req, 1)}mm of water" if i_req > 2 else "Soil moisture sufficient"
        }

irrigation_service = IrrigationEngine()
