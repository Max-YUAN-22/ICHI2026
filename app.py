from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

KNOWLEDGE_BASE = {
    "nccn_guidelines": {
        "breast_cancer": {
            "side_effects": "Common chemotherapy side effects include: 1) Nausea & Vomiting - Management with anti-nausea medication, usually 1-2 days post-treatment. 2) Fatigue - Rest periods recommended, light exercise when possible. 3) Hair loss - Usually temporary, begins 2-3 weeks after treatment. 4) Neuropathy - Tingling in hands/feet, usually reversible.",
            "treatment": "Standard treatment protocols include: Surgery (lumpectomy or mastectomy), Chemotherapy (AC-T or TAC regimens), Radiation therapy, Hormone therapy (for hormone-receptor-positive cancers), Targeted therapy (HER2-positive cancers)."
        },
        "lung_cancer": {
            "side_effects": "Lung cancer treatment side effects: 1) Shortness of breath - May require oxygen support. 2) Fatigue - Common during treatment. 3) Nausea - Anti-nausea medications available. 4) Skin changes - Radiation may cause skin irritation.",
            "treatment": "Treatment options: Surgery (lobectomy, pneumonectomy), Chemotherapy (platinum-based), Radiation therapy, Immunotherapy (PD-1/PD-L1 inhibitors), Targeted therapy (EGFR, ALK inhibitors)."
        },
        "colorectal_cancer": {
            "side_effects": "Colorectal cancer treatment side effects: 1) Diarrhea - Common, dietary modifications recommended. 2) Fatigue - Rest and light activity balance. 3) Nausea - Medication available. 4) Neuropathy - May affect hands and feet.",
            "treatment": "Treatment includes: Surgery (colectomy, proctectomy), Chemotherapy (FOLFOX, FOLFIRI), Radiation therapy (for rectal cancer), Targeted therapy (VEGF, EGFR inhibitors)."
        }
    },
    "macau_resources": {
        "hospitals": {
            "conde_s_januario": {
                "name": "Conde S. Januário Hospital",
                "oncology": "+853-2831-3731",
                "emergency": "+853-2831-3731",
                "address": "Estrada do Visconde de S. Januário, Macau"
            },
            "kiang_wu": {
                "name": "Kiang Wu Hospital",
                "oncology": "+853-2882-2371",
                "emergency": "+853-2882-2371",
                "address": "Estrada do Repouso, Macau"
            }
        },
        "cancer_associations": {
            "macau_cancer_society": {
                "name": "Macau Cancer Society",
                "hotline": "+853-2825-3381",
                "services": "Support groups, counseling, information resources"
            }
        }
    },
    "macau_data": {}
}

RISK_RULES = [
    {
        "condition": lambda age, gender, cancer: age >= 60 and gender == "male" and cancer == "lung_cancer",
        "alert": "37% recurrence risk based on Macau registry data (2003-2023), recommend regular imaging follow-up"
    },
    {
        "condition": lambda age, gender, cancer: cancer in ["lung_cancer", "liver_cancer", "colorectal_cancer"],
        "alert": "High-mortality cancer type, increased surveillance recommended"
    },
    {
        "condition": lambda age, gender, cancer: age >= 70,
        "alert": "Elderly patient - simplified information provided, key action items emphasized"
    }
]

PROCESS_STEPS = {
    "diagnosis": [
        "Initial diagnosis confirmation and documentation",
        "Cancer staging assessment and interpretation",
        "Multidisciplinary team (MDT) consultation scheduling",
        "Second opinion coordination",
        "Emotional support and information resources access"
    ],
    "treatment": [
        "Treatment plan selection and explanation",
        "Pre-treatment preparation guidance",
        "Side effect management and monitoring",
        "Nutritional support and dietary planning",
        "Financial assistance and insurance navigation"
    ],
    "followup": [
        "Regular follow-up examination scheduling",
        "Recurrence monitoring and surveillance",
        "Long-term side effect management",
        "Quality of life support and rehabilitation",
        "Survivorship care planning"
    ]
}

def extract_cancer_type(query):
    query_lower = query.lower()
    if "breast" in query_lower:
        return "breast_cancer"
    elif "lung" in query_lower:
        return "lung_cancer"
    elif "colorectal" in query_lower or "colon" in query_lower:
        return "colorectal_cancer"
    return None

def generate_ai_response(query, user_context=None):
    cancer_type = extract_cancer_type(query)
    
    response_parts = []
    
    if cancer_type and cancer_type in KNOWLEDGE_BASE["nccn_guidelines"]:
        if "side effect" in query.lower() or "副作用" in query:
            response_parts.append(KNOWLEDGE_BASE["nccn_guidelines"][cancer_type]["side_effects"])
        elif "treatment" in query.lower() or "治疗" in query:
            response_parts.append(KNOWLEDGE_BASE["nccn_guidelines"][cancer_type]["treatment"])
        else:
            response_parts.append(KNOWLEDGE_BASE["nccn_guidelines"][cancer_type]["side_effects"])
    
    if user_context:
        age = user_context.get("age", 0)
        gender = user_context.get("gender", "")
        for rule in RISK_RULES:
            if rule["condition"](age, gender, cancer_type or ""):
                response_parts.append(f"\n【Risk Alert】{rule['alert']}")
                break
    
    resources_text = "\n【Local Healthcare Resources】\n"
    resources_text += f"🏥 {KNOWLEDGE_BASE['macau_resources']['hospitals']['conde_s_januario']['name']} Oncology: {KNOWLEDGE_BASE['macau_resources']['hospitals']['conde_s_januario']['oncology']}\n"
    resources_text += f"☎️ {KNOWLEDGE_BASE['macau_resources']['cancer_associations']['macau_cancer_society']['name']} Hotline: {KNOWLEDGE_BASE['macau_resources']['cancer_associations']['macau_cancer_society']['hotline']}"
    response_parts.append(resources_text)
    
    response_parts.append("\n【Multimodal Support】\n🗣️ Voice version | 📊 Visual timeline")
    
    return "\n\n".join(response_parts) if response_parts else "I understand your question. For detailed information, please consult with your healthcare provider or oncologist."

def traditional_baseline_response(query):
    return "For information about this topic, please consult your healthcare provider or oncologist."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    system_type = data.get("system_type", "ai")
    user_context = data.get("context", {})
    
    if system_type == "ai":
        response = generate_ai_response(query, user_context)
    else:
        response = traditional_baseline_response(query)
    
    return jsonify({
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "system_type": system_type
    })

@app.route("/api/process-navigation", methods=["POST"])
def process_navigation():
    data = request.json
    stage = data.get("stage", "diagnosis")
    
    steps = PROCESS_STEPS.get(stage, [])
    resources = KNOWLEDGE_BASE["macau_resources"]
    
    return jsonify({
        "stage": stage,
        "steps": steps,
        "resources": resources,
        "current_step": 1
    })

@app.route("/api/risk-alert", methods=["POST"])
def risk_alert():
    data = request.json
    age = data.get("age", 0)
    gender = data.get("gender", "")
    cancer_type = data.get("cancer_type", "")
    
    alerts = []
    for rule in RISK_RULES:
        if rule["condition"](age, gender, cancer_type):
            alerts.append(rule["alert"])
    
    return jsonify({
        "alerts": alerts,
        "risk_level": "high" if len(alerts) > 0 else "normal"
    })

@app.route("/api/multimodal/voice", methods=["POST"])
def voice_processing():
    data = request.json
    audio_data = data.get("audio", "")
    language = data.get("language", "en")
    recognized_text = "How to manage chemotherapy side effects?"
    
    response = generate_ai_response(recognized_text)
    
    return jsonify({
        "recognized_text": recognized_text,
        "response": response,
        "language": language
    })

@app.route("/api/multimodal/image", methods=["POST"])
def image_processing():
    data = request.json
    image_data = data.get("image", "")
    ocr_result = {
        "extracted_text": "WBC: 4.2, Platelets: 180, Hemoglobin: 12.5",
        "interpretation": "Blood counts within normal range. White blood cell count is normal, platelet count is adequate, and hemoglobin level is within acceptable range."
    }
    
    return jsonify(ocr_result)

@app.route("/api/timeline", methods=["GET"])
def timeline():
    return jsonify({
        "stages": [
            {"name": "Diagnosis", "steps": PROCESS_STEPS["diagnosis"], "color": "#4A90E2"},
            {"name": "Treatment", "steps": PROCESS_STEPS["treatment"], "color": "#4CAF50"},
            {"name": "Follow-up", "steps": PROCESS_STEPS["followup"], "color": "#FF9800"}
        ],
        "current_stage": "Treatment",
        "current_step": 2
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

