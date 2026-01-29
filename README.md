# Krishi-Chetan-AI
Krishi-Chetan AI is an edge-native agricultural intelligence platform designed for farmers operating in low-connectivity, low-literacy environments.  Unlike cloud-heavy agri-tech solutions, Krishi-Chetan runs entirely on local hardware, ensuring.
Krishi-Chetan AI
Edge-AI for the Last-Mile Farmer — Local, Fast, and Transparent

🏆 Hackathon Winning Project
🥇 1st Place – College Level
🥈 2nd Place – All Mumbai Colleges (24-Hour Hackathon)

🚜 The Winning Vision

Krishi-Chetan AI is an edge-native agricultural intelligence platform designed for farmers operating in low-connectivity, low-literacy environments.

Unlike cloud-heavy agri-tech solutions, Krishi-Chetan runs entirely on local hardware, ensuring:

🔒 Privacy-first design

⚡ Real-time responses

🌐 Zero internet dependency

💰 90% lower operational cost

🛡️ The Technical Moat (Competitive Edge)
1️⃣ Quantized Edge Inference

Runs LLMs and Vision models on a single consumer GPU (RTX 4050)

Uses TensorRT + INT8 quantization for high throughput and low latency

2️⃣ Privacy-First Architecture

No data leaves the village/district

No cloud APIs, no third-party tracking, no vendor lock-in

3️⃣ Hybrid Modeling Approach

Deep Learning (Vision) for disease detection

Gradient Boosting (Tabular ML) for soil, weather, and profitability analysis

Ensures accuracy + explainability

🧠 All-in-One Feature Breakdown
🔍 Module A: AI Diagnostic Engine (Core)
🌿 Computer Vision – Crop Disease Detection

Model: EfficientNet-B4 (Fine-Tuned)

Accuracy: 98%

Coverage: 38+ crop diseases

Input: Leaf images (mobile camera)

Framework: PyTorch + OpenCV

🌱 Predictive Soil Analytics

Models:

XGBoost

Random Forest (Ensemble)

Inputs:

N-P-K values

Soil pH

Local moisture

Output:

Most profitable crop recommendation

Risk-aware suggestions

💧 Irrigation Intelligence

Uses Penman-Monteith Equation

Computes real-time water requirements

Weather-aware & crop-stage specific

📊 Module B: Market & Subsidy Intelligence
💹 Price Discovery Engine

Live Mandi price scraping

Compares:

Market Price vs. MSP

Helps farmers decide when & where to sell

🏛️ Smart Subsidy Eligibility

Cross-references:

Landholding size

Soil profile

Crop type

Maps eligibility for schemes like:

PM-KISAN

One-Click Apply Interface

🔗 Transparency Layer

Blockchain-inspired distributed ledger

Logs:

Subsidy approvals

Application timestamps

Prevents:

Manual manipulation

Local-level corruption

🗣️ Module C: Accessibility & Local Language
🎙️ Multi-Modal Interface

Voice-to-Command

Runs locally on GPU

Models:

Mozilla DeepSpeech

Whisper (Tiny)

🧑‍🌾 Low-Literacy UI

Icon-based navigation:

🔴 Red → Warnings

🟢 Green → Recommended Actions

Minimal text, maximum clarity

🏗️ Technical Architecture
Component	Technology	Why It Wins
Model Serving	FastAPI + TensorRT	Optimized inference on RTX 4050
Database	PostgreSQL + PostGIS	Spatial farm mapping & analytics
AI Stack	PyTorch + Scikit-Learn	Hybrid AI (Vision + Tabular)
Edge Deployment	Docker + Local Tunnel	Works in zero-internet regions
📚 Dataset Strategy (AI Grounding)

To ensure real-world robustness, models are trained on:

PlantVillage – Global crop disease baseline

PlantDoc – Indian lighting & soil conditions

Agmarknet – Market price time-series

IMD Gridded Data – Hyperlocal weather patterns

🎯 The Impact Pitch (Prize-Winning Logic)

“Current agri-tech platforms cost $50–$100 per farmer per month due to cloud dependencies.
Krishi-Chetan AI runs entirely on local edge hardware, reducing operational costs by 90% while delivering real-time, offline-capable intelligence.
By combining AI diagnostics, subsidy transparency, and local-language interfaces, we solve the trust, cost, and literacy barriers that cause most agricultural technologies to fail.”

📐 Mathematical Decision Support
Crop Suitability Index (CSI)
𝐶
𝑆
𝐼
=
∑
𝑖
=
1
𝑛
(
𝑤
𝑖
×
𝑆
𝑖
)
CSI=
i=1
∑
n
	​

(w
i
	​

×S
i
	​

)

Where:

𝑤
𝑖
w
i
	​

 = Weight of parameter

Rainfall → 0.4

Soil pH → 0.3

𝑆
𝑖
S
i
	​

 = Normalized score of parameter 
𝑖
i

📌 Recommendation Rule:
A crop is suggested only if:

𝐶
𝑆
𝐼
>
0.75
CSI>0.75
🚀 Future Scope

Federated learning between villages

Satellite data fusion

Edge-based yield prediction

🤝 Team & Acknowledgements

Built with ❤️ during a 24-hour hackathon by a team passionate about AI for real-world impact
