class FertilizerAdvisor:
    def get_advice(self, crop, stage, acres):
        """
        Automated Fertilizer Advisor.
        Suggests Basal vs Top-Dressing splits.
        """
        # Simplified Logic Knowledge Base
        kb = {
            "wheat": {
                "basal": {"urea": 50, "dap": 50, "mop": 40}, # kg per acre
                "crown_root": {"urea": 60},
                "flowering": {"urea": 0, "npk_spray": "19:19:19"}
            }
        }
        
        crop_data = kb.get(crop.lower(), kb['wheat'])
        
        advice = []
        
        if stage == "sowing":
            advice.append({
                "type": "Basal Dose (Foundation)",
                "items": [
                    f"Urea: {crop_data['basal']['urea'] * acres} kg",
                    f"DAP: {crop_data['basal']['dap'] * acres} kg",
                    f"MOP: {crop_data['basal']['mop'] * acres} kg"
                ]
            })
        elif stage == "growth":
             advice.append({
                "type": "Top Dressing (Growth)",
                "items": [f"Urea: {crop_data['crown_root']['urea'] * acres} kg"]
            })
            
        return advice

fertilizer_service = FertilizerAdvisor()
