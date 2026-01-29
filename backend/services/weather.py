import requests
from datetime import datetime
import json

class WeatherService:
    def get_forecast(self, location: str, days: int = 7, lang: str = "en"):
        """Get real weather forecast using wttr.in"""
        try:
            # wttr.in returns JSON with format=j1
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            forecasts = []
            current_condition = data['current_condition'][0]
            
            # Map wttr.in response to our format
            for i, day in enumerate(data['weather'][:days]):
                forecasts.append({
                    "date": day['date'],
                    "temp_max": int(day['maxtempC']),
                    "temp_min": int(day['mintempC']),
                    "humidity": int(day['hourly'][4]['humidity']), # Approx mid-day humidity
                    "rainfall_prob": int(day['hourly'][4]['chanceofrain']),
                    "condition": day['hourly'][4]['weatherDesc'][0]['value']
                })

            translations = {
                "en": {"title": f"Live Forecast for {location}"},
                "hi": {"title": f"{location} के लिए लाइव पूर्वानुमान"},
                "mr": {"title": f"{location} साठि थेट हवामान अंदाज"}
            }
            
            return {
                "location": location,
                "title": translations.get(lang, translations["en"])["title"],
                "forecasts": forecasts,
                "current": {
                    "temp": current_condition['temp_C'],
                    "humidity": current_condition['humidity'],
                    "condition": current_condition['weatherDesc'][0]['value']
                }
            }
            
        except Exception as e:
            print(f"Weather API Error: {e}")
            # Fallback to mock if API fails
            return self._get_mock_forecast(location, days, lang)

    def _get_mock_forecast(self, location, days, lang):
        # ... (Previous mock logic kept as backup)
        translations = {
            "en": {"title": f"Forecast for {location} (Offline Mode)"},
            "hi": {"title": f"{location} के लिए पूर्वानुमान (ऑफ़लाइन)"},
            "mr": {"title": f"{location} साठि हवामान अंदाज (ऑफलाइन)"}
        }
        return {
            "location": location, 
            "title": translations.get(lang, translations["en"])["title"],
            "forecasts": [],  # Empty list to trigger UI handler
            "error": "Offline"
        }

    def get_extreme_warnings(self, location: str, lang: str = "en"):
        """Check for extreme weather warnings based on real data"""
        try:
            url = f"https://wttr.in/{location}?format=j1"
            res = requests.get(url, timeout=5).json()
            
            warnings = []
            today = res['weather'][0]
            rain_chance = int(today['hourly'][4]['chanceofrain'])
            max_temp = int(today['maxtempC'])
            
            # Generate warnings based on real values
            if rain_chance > 80:
                msgs = {
                    "en": {"type": "Heavy Rain", "msg": f"High chance of rain ({rain_chance}%). Delay irrigation.", "severity": "High"},
                    "hi": {"type": "भारी बारिश", "msg": f"बारिश की उच्च संभावना ({rain_chance}%)। सिंचाई में देरी करें।", "severity": "उच्च"},
                    "mr": {"type": "मुसळधार पाऊस", "msg": f"पा पावसाची शक्यता ({rain_chance}%)। सिंचन थांबवा.", "severity": "जास्त"}
                }
                warnings.append(msgs.get(lang, msgs["en"]))
                
            if max_temp > 40:
                 msgs = {
                    "en": {"type": "Heatwave", "msg": f"High temperature ({max_temp}°C). Protect seedlings.", "severity": "High"},
                    "hi": {"type": "लू (Heatwave)", "msg": f"उच्च तापमान ({max_temp}°C)। पौधों को बचाएं।", "severity": "उच्च"},
                    "mr": {"type": "उष्णतेची लाट", "msg": f"जास्त तापमान ({max_temp}°C)। रोपांचे रक्षण करा.", "severity": "जास्त"}
                }
                 warnings.append(msgs.get(lang, msgs["en"]))

            return {"location": location, "warnings": warnings}
            
        except:
            return {"location": location, "warnings": []}

    def get_irrigation_schedule(self, crop: str, soil_type: str, weather: dict, lang: str = "en"):
        # Use passed weather data (likely from the forecast we just fetched) to calculate
        # If 'weather' dict is missing keys, use defaults
        temp = float(weather.get("temp", 30))
        humidity = float(weather.get("humidity", 50))
        
        # Simple logic based on real temp/humidity
        if temp > 35 and humidity < 40:
            schedule = "twice_daily" 
        elif temp < 20: 
            schedule = "alternate_days"
        else:
            schedule = "once_daily"

        translations = {
            "en": {
                "skip": "Skip irrigation today",
                "twice_daily": "Irrigate twice (morning & evening)",
                "once_daily": "Irrigate once (evening)",
                "alternate_days": "Irrigate on alternate days"
            },
            "hi": {
                "skip": "आज सिंचाई न करें",
                "twice_daily": "दो बार सिंचाई करें (सुबह और शाम)",
                "once_daily": "एक बार सिंचाई करें (शाम)",
                "alternate_days": "वैकल्पिक दिनों में सिंचाई करें"
            },
            "mr": {
                "skip": "आज सिंचन करू नका",
                "twice_daily": "दोनदा सिंचन करा (सकाळ आणि संध्याकाळ)",
                "once_daily": "एकदा सिंचन करा (संध्याकाळ)",
                "alternate_days": "पर्यायी दिवशी सिंचन करा"
            }
        }
        
        return {
            "crop": crop,
            "schedule": translations.get(lang, translations["en"]).get(schedule, "Check Soil Moisture"),
            "weather_input": f"{temp}°C, {humidity}% RH"
        }

weather_service = WeatherService()
