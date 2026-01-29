// Krishi-Chetan Edge-AI Client Logic

// --- 1. Navigation & Init ---
if (!localStorage.getItem('token')) {
    window.location.href = 'login.html';
}

const userRole = localStorage.getItem('user_role') || 'farmer';
const userName = localStorage.getItem('user_name') || 'User';
const userPhone = localStorage.getItem('user_phone') || '9876543210';

window.addEventListener('DOMContentLoaded', () => {
    const userSpan = document.querySelector('.user-profile span');
    if (userSpan) {
        userSpan.innerHTML = `<strong>${userName}</strong> <small>(${userRole})</small>`;
    }

    if (userRole === 'officer') {
        const diagLink = document.querySelector('[onclick="showModule(\'diagnose\')"]');
        if (diagLink) diagLink.parentElement.style.display = 'none';
        showModule('officer');
    } else {
        const officeLink = document.querySelector('[onclick="showModule(\'officer\')"]');
        if (officeLink) officeLink.parentElement.style.display = 'none';
        showModule('dashboard');
    }
});

function logout() {
    localStorage.clear();
    window.location.href = 'login.html';
}

function showModule(moduleId) {
    document.querySelectorAll('.module').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(moduleId);
    if (target) target.classList.remove('hidden');

    document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
    const activeLink = document.querySelector(`.nav-links li[onclick="showModule('${moduleId}')"]`);
    if (activeLink) activeLink.classList.add('active');

    if (moduleId === 'market') loadMarketData();
    if (moduleId === 'dashboard') loadDashboard();
    if (moduleId === 'officer') loadOfficerDashboard();
}

async function loadDashboard() {
    const lang = (typeof currentLang !== 'undefined') ? currentLang : 'en';
    if (userRole === 'farmer') {
        loadFarmerDashboard(lang);
    } else {
        initDashboardCharts();
    }
}

// --- 2. Farmer Dashboard Logic ---
async function loadFarmerDashboard(lang) {
    try {
        const res = await fetch(`/api/farmer/profile/${userPhone}`);
        if (res.ok) {
            const profile = await res.json();
            document.getElementById('farmer-profile-setup').classList.add('hidden');
            renderFarmerStats(profile, lang);
            loadDetailedRecs(profile, lang);
            loadAdvisoryHistory(lang);
        } else {
            document.getElementById('farmer-profile-setup').classList.remove('hidden');
        }
    } catch (e) { console.error("Profile Error", e); }
    loadWeatherWidget(lang);
}

function renderFarmerStats(profile, lang) {
    const statsRow = document.querySelector('#dashboard .stats-row');
    if (statsRow) {
        statsRow.innerHTML = `
            <div class="stat-card">
                <div class="stat-icon">🌱</div>
                <div><h4>Crop</h4><h2>${profile.crop_type}</h2><small>${profile.land_size} Acres</small></div>
            </div>
            <div class="stat-card">
                 <div class="stat-icon">📍</div>
                 <div><h4>Location</h4><h2>${profile.location}</h2></div>
            </div>
            <div class="stat-card">
                 <div class="stat-icon">📅</div>
                 <div><h4>Season</h4><h2>${new Date(profile.sowing_date).toLocaleDateString()}</h2><small>Sowing Date</small></div>
            </div>
        `;
    }
}

async function saveProfile() {
    const profile = {
        phone: userPhone,
        name: userName,
        location: document.getElementById('prof-loc').value,
        crop_type: document.getElementById('prof-crop').value,
        land_size: parseFloat(document.getElementById('prof-land').value),
        sowing_date: document.getElementById('prof-date').value,
        soil_type: document.getElementById('prof-soil').value,
        growth_stage: "Vegetative"
    };
    const res = await fetch('/api/farmer/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile)
    });
    if (res.ok) { alert("Profile Saved!"); loadFarmerDashboard((typeof currentLang !== 'undefined') ? currentLang : 'en'); }
}

async function loadDetailedRecs(profile, lang) {
    const sRes = await fetch(`/api/farmer/sowing-recommendation?crop=${profile.crop_type}&location=${profile.location}&lang=${lang}`);
    const sowing = await sRes.json();
    document.getElementById('rec-sowing').innerHTML = `<strong>${sowing.best_sowing_window}</strong><br><small>${sowing.reasoning}</small>`;

    const fRes = await fetch(`/api/farmer/fertilizer-dosage?crop=${profile.crop_type}&land_size=${profile.land_size}&stage=${profile.growth_stage}&lang=${lang}`);
    const fert = await fRes.json();
    document.getElementById('rec-fert').innerHTML = `Urea: ${fert.dosage.Urea_kg}kg<br>DAP: ${fert.dosage.DAP_kg}kg`;

    document.getElementById('rec-climate').innerHTML = `<strong>Safe</strong><br><small>No heatwave expected</small>`;
    loadIrrigationRec(profile.crop_type, profile.soil_type, lang);
}

async function loadAdvisoryHistory(lang) {
    const res = await fetch(`/api/farmer/advisory-history/${userPhone}`);
    const history = await res.json();
    const container = document.getElementById('advisory-history');
    if (container) {
        if (history.length > 0) {
            let html = '';
            history.forEach(adv => {
                html += `
                    <div class="card" style="border-left: 3px solid var(--accent); position: relative; margin-bottom:10px;">
                        <small>${new Date(adv.date).toLocaleDateString()}</small>
                        <h4>${adv.type.toUpperCase()}</h4>
                        <p>${adv.message}</p>
                        <div style="margin-top: 10px; display: flex; gap: 10px;">
                            ${adv.status === 'followed' ? '<span style="color:#00ff88">✅ Followed</span>' :
                        (adv.status === 'ignored' ? '<span style="color:#ff4b4b">❌ Ignored</span>' : `
                                <button onclick="updateAdvisoryStatus('${adv.id}', 'followed')" class="action-btn small">✅ Follow</button>
                                <button onclick="updateAdvisoryStatus('${adv.id}', 'ignored')" class="action-btn small" style="background:#ff4b4b">❌ Ignore</button>
                              `)}
                        </div>
                    </div>`;
            });
            container.innerHTML = html;
        } else { container.innerHTML = '<div style="color:#666">No past advisories found.</div>'; }
    }
}

async function updateAdvisoryStatus(id, status) {
    const res = await fetch(`/api/farmer/advisory/${userPhone}/${id}/status?status=${status}`, { method: 'POST' });
    if (res.ok) loadAdvisoryHistory((typeof currentLang !== 'undefined') ? currentLang : 'en');
}

// --- 3. Officer Logic ---
let map = null;
let officerCharts = {};

async function loadOfficerDashboard() {
    loadAIReviewQueue();
    loadOfficerPriorityList();

    const res = await fetch('/api/officer/priority-list');
    const data = await res.json();
    const metrics = data.metrics || { adoption_rate: 0, total_farmers: 0 };

    const adoptionEl = document.getElementById('global-adoption-rate');
    const totalEl = document.getElementById('total-farmer-count');
    if (adoptionEl) adoptionEl.innerText = metrics.adoption_rate + '%';
    if (totalEl) totalEl.innerText = metrics.total_farmers;

    initOfficerCharts();
    initOfficerMap();
}

function initOfficerCharts() {
    // 1. Crop Distribution Chart
    fetch('/api/officer/crop-patterns').then(res => res.json()).then(data => {
        const el = document.getElementById('officerCropChart');
        if (!el) return;
        const ctx = el.getContext('2d');
        if (officerCharts.crop) officerCharts.crop.destroy();
        officerCharts.crop = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                    backgroundColor: ['#00ff88', '#ffb800', '#ff4b4b', '#4834d4', '#eb4d4b', '#6ab04c', '#f0932b', '#7ed6df'],
                    borderWidth: 0
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#fff', font: { size: 10 } }
                    }
                },
                maintainAspectRatio: false
            }
        });
    });

    // 2. Adoption Trend Chart (Mocking trend data based on current adoption)
    const elTrend = document.getElementById('adoptionTrendChart');
    if (elTrend) {
        const ctxTrend = elTrend.getContext('2d');
        if (officerCharts.trend) officerCharts.trend.destroy();
        officerCharts.trend = new Chart(ctxTrend, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: 'Adoption %',
                    data: [15, 28, 42, 58], // Mocked upward trend
                    borderColor: '#00ff88',
                    backgroundColor: 'rgba(0, 255, 136, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: {
                    y: { min: 0, max: 100, grid: { color: '#222' }, ticks: { color: '#888' } },
                    x: { grid: { display: false }, ticks: { color: '#888' } }
                },
                maintainAspectRatio: false
            }
        });
    }
}

async function initOfficerMap() {
    if (map) {
        setTimeout(() => map.invalidateSize(), 200);
        return;
    }

    const mapEl = document.getElementById('map');
    if (mapEl) {
        map = L.map('map').setView([17.68, 74.00], 11);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '© OpenStreetMap'
        }).addTo(map);

        // Load all farmers as dots
        try {
            const res = await fetch('/api/officer/farmers');
            const farmers = await res.json();

            farmers.forEach(f => {
                if (f.lat && f.lng) {
                    const color = f.risk_score > 70 ? '#ff4b4b' : (f.risk_score > 40 ? '#ffb800' : '#00ff88');
                    const marker = L.circleMarker([f.lat, f.lng], {
                        radius: 5,
                        fillColor: color,
                        color: "#fff",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).addTo(map);

                    marker.bindPopup(`
                        <div style="background:#111; color:#fff; padding:5px; border-radius:5px;">
                            <strong>${f.name}</strong><br>
                            Crop: ${f.crop_type}<br>
                            Risk: <span style="color:${color}">${f.risk_score}%</span>
                        </div>
                    `);
                }
            });
        } catch (e) { console.error("Map Load Error", e); }
    }
}

async function loadAIReviewQueue() {
    try {
        const res = await fetch('/api/officer/pending-recs');
        const recs = await res.json();
        const container = document.getElementById('ai-review-queue');
        if (container) {
            if (recs.length === 0) { container.innerHTML = '<p style="color:#888; padding: 10px;">No pending items.</p>'; return; }
            let html = '';
            recs.forEach(r => {
                html += `
                    <div class="card" style="background: rgba(255,255,255,0.05); margin-bottom: 12px; border-left: 3px solid var(--accent); padding: 12px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><strong>${r.type}</strong><small>${r.farmer}</small></div>
                        <textarea id="refine-${r.id}" style="width:100%; height:60px; background:#000; color:#00ff88; border:1px solid #333; padding:8px; border-radius:4px; font-size:0.85rem; margin-bottom:8px; outline:none;">${r.recommendation}</textarea>
                        <div style="text-align:right;"><button class="action-btn small" onclick="validateAI('${r.id}')" style="background:#00ff88; color:#000;">Refine & Approve</button></div>
                    </div>`;
            });
            container.innerHTML = html;
        }
    } catch (e) { console.error(e); }
}

async function validateAI(id) {
    const newText = document.getElementById(`refine-${id}`).value;
    const res = await fetch(`/api/officer/validate-rec/${id}?new_text=${encodeURIComponent(newText)}`, { method: 'POST' });
    if (res.ok) { alert("Refined and Sent!"); loadAIReviewQueue(); }
}

async function loadOfficerPriorityList() {
    try {
        const res = await fetch('/api/officer/priority-list');
        const data = await res.json();
        const container = document.getElementById('farmer-list');
        if (container) {
            const list = data.priority_list || [];

            if (list.length === 0) { container.innerHTML = '<p style="color:#888; padding:10px;">No high-risk farmers.</p>'; return; }

            let html = '<table style="width:100%; border-collapse:collapse; font-size:0.85rem;">';
            html += '<tr style="color:#888; border-bottom:1px solid #333;"><th style="padding:5px">Farmer</th><th style="padding:5px">Risk</th><th style="padding:5px">Reason</th></tr>';
            list.forEach(f => {
                html += `<tr style="border-bottom:1px solid #222;">
                    <td style="padding:8px"><strong>${f.name}</strong><br><small>${f.phone}</small></td>
                    <td style="padding:8px; color:#ff4b4b; font-weight:bold;">${f.risk_score}</td>
                    <td style="padding:8px"><small>${f.reason}</small></td>
                </tr>`;
            });
            html += '</table>';
            container.innerHTML = html;
        }
    } catch (e) { }
}

async function sendAdvisory() {
    const msg = document.getElementById('adv-msg').value;
    const type = document.getElementById('adv-type').value;
    const farmers = ["9876543210"]; // Demo: targeted selection normally
    const advisory = { type: type, message: msg, valid_until: "2026-12-31" };

    const res = await fetch('/api/officer/send-advisory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phones: farmers, advisory: advisory })
    });
    if (res.ok) { alert("Advisory Sent!"); document.getElementById('adv-msg').value = ''; }
}

// --- 4. Market & Weather ---
async function loadMarketData() {
    const lang = (typeof currentLang !== 'undefined') ? currentLang : 'en';
    try {
        const response = await fetch(`/api/market/prices?lang=${lang}`);
        const prices = await response.json();
        let html = '';
        prices.forEach(item => {
            const up = item.trend === 'up';
            html += `
            <div class="card">
                <div style="display:flex; justify-content:space-between;"><span>${up ? '📈' : '📉'}</span><span style="color:${up ? '#00ff88' : '#ff4b4b'}; font-size: 0.7rem;">${item.trend.toUpperCase()}</span></div>
                <h4 style="margin-top:10px;">${item.crop}</h4>
                <p style="font-size:1.3rem; font-weight:bold;">₹${item.price}</p>
                <small style="color:#666">per ${item.unit}</small>
            </div>`;
        });
        document.getElementById('market-prices-list').innerHTML = html;

        const newsRes = await fetch(`/api/market/news?lang=${lang}`);
        const news = await newsRes.json();
        let nHtml = ''; news.forEach(n => { nHtml += `<li><strong>${n.source}:</strong> ${n.title}</li> `; });
        document.getElementById('news-list').innerHTML = nHtml;

        const subRes = await fetch(`/api/subsidy/check?lang=${lang}`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ land_size: 2.5, category: "General" })
        });
        const schemes = await subRes.json();
        let sHtml = '';
        schemes.forEach(s => {
            sHtml += `<li class="subsidy-item"><strong>${s.name}</strong>: ${s.benefit} <button class="apply-btn small">Apply</button></li>`;
        });
        document.querySelector('.subsidy-list').innerHTML = sHtml;
    } catch (e) { }
}

async function loadWeatherWidget(lang) {
    try {
        const res = await fetch(`/api/weather/forecast?location=Satara&days=1&lang=${lang}`);
        const data = await res.json();
        const card = document.getElementById('weather-card');
        if (card) { card.innerHTML = `<div class="stat-icon">🌤️</div><div><h4>Weather</h4><h2>${data.current.temp}°C</h2><small>${data.current.condition}</small></div>`; }
    } catch (e) { }
}

async function loadIrrigationRec(crop, soil, lang) {
    try {
        const wRes = await fetch(`/api/weather/forecast?location=Satara&days=1&lang=en`);
        const wData = await wRes.json();
        const res = await fetch(`/api/weather/irrigation-schedule?crop=${crop}&soil_type=${soil}&lang=${lang}`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(wData.current)
        });
        const rec = await res.json();
        const card = document.getElementById('irrig-card');
        if (card) { card.innerHTML = `<div class="stat-icon">💧</div><div><h4>Irrigation</h4><h2>${rec.schedule}</h2><small>${rec.reason}</small></div>`; }
    } catch (e) { }
}

// --- 5. Photo Diagnosis ---
const fileInput = document.getElementById('file-input');
if (fileInput) fileInput.addEventListener('change', (e) => { if (e.target.files[0]) uploadFile(e.target.files[0]); });

async function uploadFile(file) {
    const lang = (typeof currentLang !== 'undefined') ? currentLang : 'en';
    const resultArea = document.getElementById('diag-result');
    const loading = document.getElementById('diag-loading');
    const content = document.getElementById('diag-content');
    resultArea.classList.remove('hidden'); loading.classList.remove('hidden'); content.innerHTML = '';
    try {
        const res = await fetch(`/api/diagnose/leaf?lang=${lang}`, { method: 'POST' });
        const result = await res.json();
        loading.classList.add('hidden');
        content.innerHTML = `
            <div style="text-align:center;">
                <img src="${URL.createObjectURL(file)}" style="max-height:150px; border-radius:8px; margin-bottom:15px; border:2px solid var(--primary);">
                <h4 style="color:#ff4b4b;">⚠️ ${result.name}</h4>
                <p style="font-size:0.9rem; margin-bottom:10px;">${result.remedy}</p>
                <div style="background:rgba(0,0,0,0.3); padding:8px; border-radius:4px; font-size:0.8rem;">
                    Confidence: ${Math.round(result.confidence * 100)}% (${result.model})
                </div>
            </div>`;
    } catch (e) { }
}

// --- 6. Chatbot ---
let isChatOpen = false;
function toggleChat() {
    const widget = document.getElementById('chat-widget');
    isChatOpen = !isChatOpen;
    widget.classList.toggle('closed', !isChatOpen);
    document.getElementById('chat-toggle-icon').innerText = isChatOpen ? '▼' : '▲';
}
async function sendChat() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;
    appendMsg(msg, 'user'); input.value = '';
    const typingId = appendMsg('...', 'bot');
    try {
        const lang = (typeof currentLang !== 'undefined') ? currentLang : 'en';
        const res = await fetch('/api/chat/ask', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, lang: lang })
        });
        const data = await res.json();
        const typingEl = document.getElementById(typingId); if (typingEl) typingEl.remove();
        appendMsg(data.response, 'bot');
        if (data.action === "open_market") showModule('market');
    } catch (e) { appendMsg("Error", 'bot'); }
}
function appendMsg(text, sender) {
    const body = document.getElementById('chat-body');
    const div = document.createElement('div');
    div.id = 'msg-' + Date.now(); div.className = `chat-msg ${sender}`; div.innerText = text;
    body.appendChild(div); body.scrollTop = body.scrollHeight; return div.id;
}

window.refreshData = function () {
    const activeModule = document.querySelector('.module:not(.hidden)');
    if (activeModule) {
        if (activeModule.id === 'market') loadMarketData();
        if (activeModule.id === 'officer') loadOfficerDashboard();
        if (activeModule.id === 'dashboard') loadDashboard();
    }
}
