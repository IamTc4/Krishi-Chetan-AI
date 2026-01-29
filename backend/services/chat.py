from pydantic import BaseModel
import random

class ChatMessage(BaseModel):
    message: str
    language: str = "en"  # en, hi, mr

class ChatResponse(BaseModel):
    response: str
    action_suggested: str = None

class ChatService:
    def __init__(self):
        # Simple keywords for demo. Real implementation would use LLM.
        self.responses = {
            "en": {
                "default": "I'm not sure, but I can help with crop prices, weather, and soil health.",
                "price": "Market prices are trending up for onions and tomatoes today.",
                "weather": "It is sunny today with a high of 32°C. Good for harvesting.",
                "disease": "Please upload a photo of the affected plant in the 'Diagnose' tab.",
                "subsidy": "You might be eligible for PM-KISAN. Check the 'Market & Subsidy' tab.",
                "water": "Irrigation is recommended in the evening.",
                "soil": "Soil nitrogen levels are looking low in your region."
            },
            "hi": {
                "default": "मुझे खेद है, मुझे समझ नहीं आया। मैं फसल की कीमतों, मौसम और मिट्टी के स्वास्थ्य में मदद कर सकता हूं।",
                "price": "प्याज और टमाटर के बाजार भाव आज ऊपर जा रहे हैं।",
                "weather": "आज धूप खिली है और तापमान 32 डिग्री है। कटाई के लिए अच्छा है।",
                "disease": "कृपया 'रोग निदान' टैब में प्रभावित पौधे की फोटो अपलोड करें।",
                "subsidy": "आप पीएम-किसान के लिए पात्र हो सकते हैं। 'मंडी और सब्सिडी' टैब देखें।",
                "water": "शाम के समय सिंचाई की सलाह दी जाती है।",
                "soil": "आपके क्षेत्र में मिट्टी में नाइट्रोजन का स्तर कम लग रहा है।"
            },
            "mr": {
                "default": "मला माफ करा, मला समजले नाही. मी पीक भाव, हवामान आणि माती आरोग्याबद्दल मदत करू शकतो.",
                "price": "कांदा आणि टोमॅटोचे बाजार भाव आज वाढत आहेत.",
                "weather": "आज ऊन आहे आणि तापमान ३२ अंश आहे. कापणीसाठी चांगले आहे.",
                "disease": "कृपया 'रोग निदान' टॅबमध्ये प्रभावित वनस्पतीचा फोटो अपलोड करा.",
                "subsidy": "तुम्ही पीएम-किसानसाठी पात्र असू शकता. 'बाजार आणि अनुदान' टॅब तपासा.",
                "water": "संध्याकाळी सिंचन करण्याची शिफारस केली जाते.",
                "soil": "तुमच्या भागात मातीतील नायट्रोजनची पातळी कमी दिसत आहे."
            }
        }

    def get_response(self, query: str, lang: str) -> ChatResponse:
        lang_code = lang if lang in ["en", "hi", "mr"] else "en"
        query_lower = query.lower()
        
        resp_dict = self.responses[lang_code]
        
        if "price" in query_lower or "bhav" in query_lower or "mandi" in query_lower or "rate" in query_lower or "भाव" in query_lower:
            return ChatResponse(response=resp_dict["price"], action_suggested="market")
        
        if "weather" in query_lower or "rain" in query_lower or "mousam" in query_lower or "hawa" in query_lower or "हवामान" in query_lower:
            return ChatResponse(response=resp_dict["weather"], action_suggested="weather")
        
        if "disease" in query_lower or "pest" in query_lower or "keeda" in query_lower or "rog" in query_lower or "रोग" in query_lower:
            return ChatResponse(response=resp_dict["disease"], action_suggested="diagnose")
            
        if "subsidy" in query_lower or "gov" in query_lower or "anudan" in query_lower or "scheme" in query_lower or "अनुदान" in query_lower:
            return ChatResponse(response=resp_dict["subsidy"], action_suggested="market")

        if "water" in query_lower or "irrigation" in query_lower or "pani" in query_lower or "पाणी" in query_lower:
            return ChatResponse(response=resp_dict["water"], action_suggested="settings")

        if "soil" in query_lower or "khad" in query_lower or "fertilizer" in query_lower or "mati" in query_lower or "माती" in query_lower:
            return ChatResponse(response=resp_dict["soil"], action_suggested="dashboard")

        return ChatResponse(response=resp_dict["default"])

chat_service = ChatService()
