# 🌱 Krishi-Chetan AI  
### *Edge-AI for the Last-Mile Farmer — Local, Fast, and Transparent*

🏆 **Hackathon Winning Project**  
🥇 1st Place – College Level  
🥈 2nd Place – All Mumbai Colleges (24-Hour Hackathon)

---

## 🚜 The Winning Vision

**Krishi-Chetan AI** is an **edge-native agricultural intelligence platform** designed for farmers operating in low-connectivity, low-literacy environments.

Unlike cloud-heavy agri-tech solutions, Krishi-Chetan runs **entirely on local hardware**, ensuring:
- 🔒 Privacy-first design  
- ⚡ Real-time responses  
- 🌐 Zero internet dependency  
- 💰 90% lower operational cost  

---

## 🛡️ The Technical Moat (Competitive Edge)

### 1️⃣ Quantized Edge Inference
- Runs **heavy Vision & Language models on a single consumer GPU (RTX 4050)**
- Uses **TensorRT with INT8 quantization** for low latency and high throughput

### 2️⃣ Privacy-First Architecture
- **No data leaves the village/district**
- Zero cloud APIs, zero vendor lock-in

### 3️⃣ Hybrid Modeling
- **Deep Learning (Vision)** for disease detection  
- **Gradient Boosting (Tabular ML)** for soil, weather & profit analysis  
- Ensures **accuracy + explainability**

---

## 🧠 All-in-One Feature Breakdown

---

## 🔍 Module A: AI Diagnostic Engine (Core)

### 🌿 Computer Vision – Crop Disease Detection
- **Model:** EfficientNet-B4 (Fine-Tuned)
- **Accuracy:** 98%
- **Coverage:** 38+ crop diseases
- **Input:** Leaf images
- **Stack:** PyTorch + OpenCV

---

### 🌱 Predictive Soil Analytics
- **Models:**  
  - XGBoost  
  - Random Forest (Ensemble)
- **Inputs:**  
  - N-P-K values  
  - Soil pH  
  - Local moisture  
- **Output:**  
  - Most profitable crop recommendation  

---

### 💧 Irrigation Intelligence
- Uses **Penman-Monteith Equation**
- Calculates **real-time water requirements**
- Weather & crop-stage aware

---

## 📊 Module B: Market & Subsidy Intelligence

### 💹 Price Discovery
- Live **Mandi price scraping**
- Market price vs MSP comparison
- Helps farmers decide **when & where to sell**

---

### 🏛️ Smart Subsidy Eligibility
- Cross-references:
  - Landholding size  
  - Soil parameters  
- Maps eligibility for schemes like **PM-KISAN**
- **One-Click Apply Interface**

---

### 🔗 Transparency Layer
- **Blockchain-inspired distributed ledger**
- Logs subsidy approvals
- Prevents local-level corruption

---

## 🗣️ Module C: Accessibility & Local Language

### 🎙️ Multi-Modal Interface
- Voice-to-command in regional languages
- Runs **fully offline on GPU**
- Models:
  - Mozilla DeepSpeech  
  - Whisper (Tiny)

### 🧑‍🌾 Low-Literacy UI
- Icon-based navigation  
  - 🔴 Red → Warnings  
  - 🟢 Green → Actions  
- Minimal text, maximum clarity

---

## 🏗️ Technical Architecture

| Component | Technology | Purpose |
|--------|------------|--------|
| Model Serving | FastAPI + TensorRT | Optimized GPU inference |
| Database | PostgreSQL + PostGIS | Spatial farm analytics |
| AI Stack | PyTorch + Scikit-Learn | Hybrid AI approach |
| Deployment | Docker + Local Tunnel | Zero-cloud edge deployment |

---

## 📚 Dataset Strategy

- **PlantVillage** – Global disease patterns  
- **PlantDoc** – Indian field conditions  
- **Agmarknet** – Market price time-series  
- **IMD Gridded Data** – Hyperlocal weather  

---

## 🎯 Impact Pitch (Prize-Winning Logic)

> *Current agri-tech platforms cost \$50–\$100/month per farmer due to cloud fees.  
Krishi-Chetan AI runs entirely on edge hardware, reducing operational costs by **90%** while providing real-time, offline intelligence.  
By combining AI diagnostics, subsidy transparency, and local-language interfaces, we solve the trust, cost, and literacy gaps that break most agricultural solutions.*

---

## 📐 Mathematical Decision Support

### Crop Suitability Index (CSI)

\[
CSI = \sum_{i=1}^{n} (w_i \times S_i)
\]

Where:
- \( w_i \) = Weight of a parameter  
  - Rainfall → 0.4  
  - Soil pH → 0.3  
- \( S_i \) = Normalized score of parameter \( i \)

✅ **Crop is recommended only if:**  
\[
CSI > 0.75
\]

---

## 🚀 Future Scope
- Federated learning between villages  
- Satellite data integration  
- Edge-based yield forecasting  

---

## 🤝 Team & Acknowledgements
Built during a **24-hour Hackathon** by a team focused on **AI with real-world agricultural impact** 🌾
