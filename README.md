<p align="center">
  <img src="https://img.shields.io/badge/VANI-Transparent%20Nepal%20AI-6366f1?style=for-the-badge&logo=openai&logoColor=white" alt="VANI Badge"/>
  <img src="https://img.shields.io/badge/Languages-Nepali%20%7C%20English-ec4899?style=for-the-badge" alt="Languages"/>
  <img src="https://img.shields.io/badge/Focus-Governance%20%26%20Tourism-c084fc?style=for-the-badge" alt="Focus"/>
  <img src="https://img.shields.io/badge/Architecture-RAG%20%2B%20Voice%20AI-22c55e?style=for-the-badge" alt="Architecture"/>
</p>

<h1 align="center">🇳🇵 VANI – AI Voice Assistant for Transparent Governance & Smart Tourism in Nepal</h1>

<p align="center">
  <strong>Empowering citizens and tourists through multilingual AI-driven voice assistance.</strong>
<<<<<<< HEAD
</p>

<p align="center">
  <em>Supporting transparency, accountability, accessibility, and digital inclusion across Nepal.</em>
=======
>>>>>>> 81c7aaa (pre-initialized project structure)
</p>

---

## 🌟 Overview

<<<<<<< HEAD
**VANI (Voice Assistant for Nepal Intelligence)** is a multilingual AI-powered virtual assistant designed to improve transparency, accessibility, and citizen engagement across Nepal. Built specifically for the Nepali context, VANI enables citizens, tourists, and government stakeholders to access information and services using natural voice or text conversations in **Nepali and English**.

The platform addresses one of Nepal's major digital challenges: making public services and information accessible to everyone regardless of language proficiency or digital literacy. Through conversational AI, citizens can inquire about government services, track applications, submit complaints, receive official updates, and access public information instantly.

At the same time, VANI serves as an intelligent tourism assistant, helping domestic and international travelers discover destinations, transportation options, cultural heritage sites, permits, emergency services, and local recommendations through multilingual voice interactions.

By combining **Multilingual NLP**, **Retrieval-Augmented Generation (RAG)**, **Voice AI**, and **Government Knowledge Systems**, VANI creates a unified digital gateway that promotes transparency, accountability, and smarter public service delivery while enhancing Nepal's tourism ecosystem.

---

## 🎯 Vision

To make government services and tourism information accessible to every citizen and visitor through natural multilingual conversations.

---

## 🏆 Theme Alignment: Tech for Transparent Nepal

VANI directly supports transparent governance by:

- 🏛️ Providing instant access to public information
- 📄 Enabling real-time government service tracking
- 📢 Simplifying complaint registration and follow-up
- 🔍 Reducing information asymmetry between citizens and authorities
- 🌍 Increasing accessibility for rural and underserved communities
- 🗣️ Supporting multilingual communication across government offices
- 🤝 Promoting accountability through transparent information access

Through AI-powered interactions, VANI helps build a more open, accountable, and citizen-centric digital Nepal.

---

=======
**VANI (Voice Assistant for Nepal Intelligence)** is a multilingual AI-powered virtual assistant designed to improve transparency, accessibility, and citizen engagement across Nepal. Built for the Nepali context, VANI enables citizens, tourists, and government stakeholders to access information and services using natural voice or text conversations in **Nepali and English**.

By combining **Multilingual NLP**, **Retrieval-Augmented Generation (RAG)**, **Voice AI**, and **Multi-Agent Architecture**, VANI creates a unified digital gateway for transparent governance and smart tourism.

---

>>>>>>> 81c7aaa (pre-initialized project structure)
## ✨ Core Features

| Feature | Description |
|----------|-------------|
| 🎙️ Voice Assistant | Natural voice interaction in Nepali and English |
| 🏛️ Government Service Tracking | Track applications, requests, and public services |
| 📢 Complaint Management | Register and monitor citizen complaints |
| 🌐 Multilingual Communication | Nepali, English, and code-mixed language support |
| 📚 RAG Knowledge Engine | Accurate responses from verified government and tourism data |
| 🗺️ Tourism Guide | Travel recommendations and destination assistance |
<<<<<<< HEAD
| 🧠 Context-Aware Conversations | Maintains conversation history and user context |
| 🔍 Intelligent Search | Semantic retrieval from government documents and tourism resources |
| 📱 Multi-Platform Access | Web, mobile, and future voice-device integration |
| 🔒 Transparent Information Access | Reliable and explainable responses from trusted sources |
=======
| 🧠 Multi-Agent System | 6 specialized agents for different business domains |
| 📱 Web Dashboard | Full management UI with 6 pages |

---

## 🏗️ Architecture

```
User Voice → Noise Reduction → Whisper ASR → Language Detection
→ Intent Classifier → Entity Extractor → Master Agent
→ Sub-Agent (Sales/CRM/HR/Invoice/Inventory/Analytics)
→ PostgreSQL → RAG Knowledge Base → LLM → TTS → Voice Response
```

---

## 📁 Project Structure

```
VANI/
├── frontend/              # Next.js UI (6 pages)
│   └── app/
│       ├── page.js               # Dashboard
│       ├── sales/                # Sales analytics
│       ├── inventory/            # Stock management
│       ├── customers/            # Customer database
│       ├── invoices/             # Invoice tracking
│       └── voice-assistant/      # Main VANI interface
│
├── backend/               # FastAPI backend
│   └── main.py            # API server with 6+ endpoints
│
├── ai/
│   ├── asr/               # Whisper ASR + noise reduction
│   ├── nlp/               # Intent classification + entity extraction
│   ├── rag/               # Document chunking, embedding, retrieval
│   ├── tts/               # Coqui TTS + ElevenLabs
│   └── agents/            # Multi-agent system (6 agents + master)
│
├── database/
│   ├── schema.sql          # PostgreSQL schema (8 tables)
│   └── seed/               # Synthetic data generators
│
├── datasets/
│   ├── intents/            # 9 JSON files × 1000 examples = 9,000 utterances
│   ├── synthetic/          # 120,500 records (CSV)
│   ├── knowledge_base/     # 5 Nepal government/tourism documents
│   └── speech/             # Voice command directories
│
├── deployment/             # Docker, nginx configs
├── docs/                   # Architecture, API, dataset, deployment docs
├── research/               # VANI-SME-Commands dataset paper
└── requirements.txt
```

---

## 🚀 Quick Start

### Backend
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Generate Datasets
```bash
python database/seed/generate_data.py    # 120,500 synthetic records
python database/seed/generate_intents.py  # 9,000 intent utterances
```

### Docker
```bash
cd deployment
docker-compose up -d
```

---

## 📊 Datasets Generated

| Dataset | Records | Location |
|---------|---------|----------|
| Customers | 10,000 | `datasets/synthetic/customers.csv` |
| Products | 5,000 | `datasets/synthetic/products.csv` |
| Sales | 100,000 | `datasets/synthetic/sales.csv` |
| Invoices | 5,000 | `datasets/synthetic/invoices.csv` |
| Employees | 500 | `datasets/synthetic/employees.csv` |
| Intent Utterances | 9,000 | `datasets/intents/*.json` |
| Knowledge Base | 5 docs | `datasets/knowledge_base/*.txt` |
>>>>>>> 81c7aaa (pre-initialized project structure)

---

## 💬 Example Citizen Interaction

<<<<<<< HEAD
**Citizen:**

> मेरो नागरिकता आवेदनको स्थिति के छ?

**VANI:**

> तपाईंको नागरिकता आवेदन हाल जिल्ला प्रशासन कार्यालयमा समीक्षा प्रक्रियामा छ। अनुमानित पूरा हुने समय ३ दिन बाँकी छ।

---

## 💬 Example Tourist Interaction

**Tourist:**

> How can I reach Swayambhunath from Thamel?

**VANI:**

> You can take a taxi, local bus, or walk. The journey takes approximately 15–20 minutes depending on traffic.

---

## 🎯 Real-World Applications

### 🏛️ Smart Governance Assistant

- Citizenship application tracking
- Passport and license status inquiries
- Government service guidance
- Public grievance registration
- Municipality information access
- Official announcement dissemination

### 🗺️ Smart Tourism Assistant

- Destination recommendations
- Transportation guidance
- Permit and visa information
- Cultural heritage exploration
- Emergency contact assistance
- Local business and accommodation support

### 🌐 Digital Inclusion

- Voice-based interaction for non-technical users
- Support for Nepali and English speakers
- Improved accessibility for rural populations
- Reduced dependence on physical government visits

### 📊 Public Transparency Platform

- Access to public policies and regulations
- Government scheme awareness
- Service process explanations
- Citizen feedback collection
- Accountability through service-status visibility

---

## 🚀 Why VANI Matters

In Nepal, millions of citizens still face challenges accessing government services due to language barriers, limited digital literacy, and fragmented information systems. Similarly, tourists often struggle to obtain reliable local information efficiently.

VANI addresses these challenges by providing a single multilingual AI platform where users can simply speak or type their queries and instantly receive accurate, context-aware, and trustworthy responses.

By making information accessible to everyone, VANI contributes directly to:

- Transparent Governance
- Digital Inclusion
- Citizen Empowerment
- Tourism Promotion
- Public Accountability
- Smart Nation Development
=======
| Layer | Technology |
|-------|-----------|
| Frontend | Next.js, Vanilla CSS |
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| Vector DB | ChromaDB / Qdrant |
| ASR | Faster Whisper |
| NLP | sentence-transformers, MiniLM |
| TTS | Coqui TTS / ElevenLabs |
| Deployment | Docker, Nginx |

---

## 📄 License

MIT License
>>>>>>> 81c7aaa (pre-initialized project structure)

---

<p align="center">
  <strong>🇳🇵 Built for Transparent Nepal • Powered by AI • Designed for Everyone</strong>
</p>
