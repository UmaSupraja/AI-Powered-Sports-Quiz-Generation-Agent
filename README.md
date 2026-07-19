# AI-Powered Sports Quiz Generation Agent

### [View the Live AI-Powered Sports Quiz Generation Agent !](https://umasupraja-ai-powered-sports-quiz-generation-agent-app-qg3mia.streamlit.app/)


An intelligent Sports Quiz application built using **Google Gemini**, **ChromaDB**, **DuckDuckGo Search**, and **Streamlit** that generates dynamic multiple-choice quizzes using Retrieval-Augmented Generation (RAG).

The application combines **historical sports knowledge stored locally in ChromaDB** with **live sports news retrieved from the web**, enabling users to practice quizzes that are both educational and up to date.

---

## Features

- Generate quizzes for multiple sports
- Difficulty Levels (Easy, Medium, Hard)
- AI-generated Multiple Choice Questions (MCQs)
- Retrieval-Augmented Generation (RAG)
- Historical Sports Facts using ChromaDB
- Live Sports News using DuckDuckGo Search
- Performance Dashboard
- Quiz History Tracking
- Instant Score Evaluation
- Question-wise Explanation
- View Retrieved RAG Context
- Download Retrieved Context
- Clean Streamlit User Interface

---

# System Architecture

```
                User
                  │
                  ▼
          Streamlit Application
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
 Historical Facts       Live Sports News
   (ChromaDB)          (DuckDuckGo Search)
        │                   │
        └─────────┬─────────┘
                  ▼
          Context Aggregation
                  ▼
          Google Gemini API
                  ▼
         AI Quiz Generation
                  ▼
        Interactive Quiz UI
                  ▼
     Performance Dashboard
```

---

# Project Structure

```
sports-quiz-agent/

│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── chroma_db/
│
├── data/
│   └── sports_facts.json
│
├── src/
│   ├── config.py
│   ├── database.py
│   ├── generator.py
│   └── search.py
│
└── venv/
```

---

# Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | Web Application |
| Google Gemini | Quiz Generation |
| ChromaDB | Vector Database |
| DuckDuckGo Search | Live Sports News |
| Sentence Transformers | Text Embeddings |
| ONNX Runtime | Fast Embedding Inference |
| dotenv | Environment Variables |

---

# Retrieval-Augmented Generation (RAG)

The application follows a Retrieval-Augmented Generation workflow.

### Step 1

Retrieve historical sports facts from **ChromaDB**.

### Step 2

Retrieve the latest sports news using **DuckDuckGo Search**.

### Step 3

Merge both contexts.

### Step 4

Provide the combined context to **Google Gemini**.

### Step 5

Generate an intelligent sports quiz.

---

# Supported Sports

- Cricket
- Football
- Basketball
- Badminton
- Tennis

---

# User Workflow

```
Select Sport
        │
        ▼
Select Difficulty
        │
        ▼
Generate Quiz
        │
        ▼
Answer Questions
        │
        ▼
Submit Quiz
        │
        ▼
Score Evaluation
        │
        ▼
Performance Dashboard
        │
        ▼
Generate New Quiz
```

---

# Performance Dashboard

The application maintains quiz history during the active session.

Dashboard includes:

- Current Score
- Previous Score
- Average Score
- Best Score
- Improvement
- Quiz History
- Correct Answers
- User Answers
- Detailed Explanations

---

# Retrieved RAG Context

Users can inspect the exact information retrieved before quiz generation.

The retrieved context includes:

- Historical Sports Facts
- Latest Sports News

This improves transparency and explains how the AI generated the quiz.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/sports-quiz-agent.git

cd sports-quiz-agent
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

# Sample Quiz

```
Sport : Football

Difficulty : Hard

Question 1

Which country won the first FIFA World Cup?

A. Brazil

B. Uruguay

C. Germany

D. France

Correct Answer : B

Explanation :
Uruguay won the inaugural FIFA World Cup in 1930.
```

---

# Future Enhancements

- User Authentication
- Leaderboards
- Timer Based Quiz
- Multiplayer Quiz
- Difficulty Adaptation using AI
- PDF Score Report
- Email Quiz Reports
- Voice-based Quiz Generation
- Support for More Sports
- Cloud Deployment

---

# Author

**Supraja Putrevu**

B.Tech – Computer Science & Engineering (Data Science)

Python Developer | AI Enthusiast | Data Science | Machine Learning

GitHub: https://github.com/UmaSupraja


# License

This project is developed for educational and learning purposes.

---
