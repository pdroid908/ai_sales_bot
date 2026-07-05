# 🤖 AI Sales Assistant

An intelligent sales assistant API built with **FastAPI** and **Python** to automate customer interactions, qualify leads, and answer frequently asked questions.

Instead of relying on a Large Language Model (LLM), this project uses a custom rule-based conversation engine, fuzzy keyword matching, and conversation state management to provide fast, predictable, and business-oriented responses.

---

## ✨ Features

- Intelligent FAQ System
- Fuzzy Intent Matching
- Lead Qualification Flow
- Conversation State Management
- Rule-based Chat Engine
- Chat History Logging
- REST API
- Fast Response Time
- Easy Knowledge Base Expansion

---

## 🛠 Tech Stack

- Python
- FastAPI
- Pydantic
- TheFuzz
- Uvicorn

---

## 📂 Project Structure

```text
ai_sales_bot/
│
├── main.py
├── requirements.txt
├── chat_history.txt
├── Dockerfile
└── .gitignore
```

---

## 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/pdroid908/ai_sales_bot.git

cd ai_sales_bot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn main:app --reload
```

The API will be available at

```
http://localhost:8000
```

Interactive API Documentation

```
http://localhost:8000/docs
```

---

## 💬 Conversation Flow

```text
User

│

▼

Normalize Message

│

▼

Intent Detection

│

▼

Knowledge Base Matching

│

▼

Lead Qualification

│

▼

Response Generator

│

▼

Chat History
```

---

## 📌 Main Capabilities

- Answer company information
- Introduce available services
- Guide customers through service selection
- Collect sales leads
- Recommend suitable services
- Store conversation history
- Maintain conversation context
- Handle multi-step conversations

---

## 🧠 Conversation Engine

The chatbot uses a custom conversational engine consisting of:

- Keyword Knowledge Base
- Fuzzy Matching (TheFuzz)
- Intent Detection
- State Machine
- Lead Scoring
- Context Memory

This approach provides deterministic responses while remaining lightweight and easy to maintain.

---

## 🔒 Highlights

- Lightweight architecture
- Fast response without external AI services
- Expandable knowledge base
- Context-aware conversations
- Simple deployment
- Business-oriented chatbot

---

## 🎯 Project Goals

- Automate customer support
- Qualify potential clients
- Reduce manual customer service workload
- Practice conversational AI architecture
- Build scalable chatbot APIs

---

## 📌 Future Improvements

- Database Integration
- Admin Knowledge Base
- Multi-language Support
- LLM Hybrid Mode
- User Authentication
- Analytics Dashboard
- Vector Search
- Redis Cache

---

## 👨‍💻 Author

**Putra Rohman**

Backend Developer

**Core Skills**

- Go
- Python
- FastAPI
- TypeScript
- PostgreSQL
- Redis
- Docker
- REST API
- AI Integration

GitHub

https://github.com/pdroid908

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

---

## License

MIT License
