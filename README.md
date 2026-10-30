# 🎓 AI-Powered Study Assistant

An intelligent AI-powered learning platform built using Python and Streamlit that helps students study smarter through PDF-based question answering, AI-generated quizzes, performance analytics, personalized study planning, and progress tracking.

## 🚀 Project Overview

AI-Powered Study Assistant is an AI-based educational application that helps students understand study materials, evaluate their knowledge, identify weak topics, and manage their preparation efficiently.

The application uses Retrieval-Augmented Generation (RAG), FAISS vector search, and Google Gemini AI to provide context-based answers from uploaded PDF documents.

## ✨ Key Features

### 1. 📚 PDF Upload & AI Question Answering
- Upload PDF study materials.
- Extract and process PDF text.
- Generate text embeddings.
- Store and retrieve relevant information using FAISS.
- Ask questions based on uploaded documents.
- Get AI-generated contextual answers.

### 2. 🧠 AI Quiz Generator
- Generate quizzes using AI.
- Answer multiple-choice questions.
- Automatically calculate quiz scores.
- Display correct answers and explanations.
- Save quiz attempts in SQLite.

### 3. 📊 Student Performance Analytics
- View previous quiz attempts.
- Track quiz scores and performance.
- Analyze learning progress.
- Identify weak topics.
- Receive topic-based study recommendations.

### 4. 🎯 Smart Study Planner
- Create personalized study plans.
- Set examination names and dates.
- Add subjects and study topics.
- Define daily study hours.
- Generate study timetables.
- Download study plans as CSV files.

### 5. ✅ Study Task Tracker
- Add study tasks.
- Mark tasks as completed.
- Monitor daily study progress.
- Track pending and completed tasks.

### 6. 👤 Student Profile Management
- Save student profile information.
- Maintain profile details using SQLite.
- Retrieve saved profile information.

### 7. 📈 Study Plan History
- Save previously generated study plans.
- View historical study plans.
- Maintain study planning records.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | Web application interface |
| Google Gemini AI | AI-powered responses and quiz generation |
| LangChain | Document processing and RAG workflow |
| FAISS | Vector database and similarity search |
| Hugging Face | Text embeddings |
| PyPDFLoader | PDF text extraction |
| SQLite | Student data and progress storage |
| Pandas | Data processing and CSV export |

## 📁 Project Structure

```text
AI-Powered-Study-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   └── db_manager.py
│
├── modules/
│   └── quiz_generator.py
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── assets/
│
└── AI_powered_study_assistant.ipynb
```

## ⚙️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/prajapatiashish85/-AI-Powered-Study-Assistant.git
```

### Step 2: Open Project Directory

```bash
cd -AI-Powered-Study-Assistant
```

### Step 3: Create Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Gemini API Key

Create a `.env` file in the project root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Never upload your API key or `.env` file to GitHub.

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🗄️ Database

The application uses SQLite to maintain:
- Quiz attempts and scores
- Student profiles
- Study plans
- Study task completion records

## 🎯 Project Objectives

- Make learning more interactive and personalized.
- Help students understand PDF study materials.
- Automate quiz generation and evaluation.
- Analyze student performance.
- Identify weak learning areas.
- Improve time management through smart study planning.

## 🔮 Future Enhancements

- Voice-based AI learning assistant.
- Multi-language learning support.
- Advanced learning analytics.
- AI-powered personalized recommendations.
- Student progress visualization.
- Cloud-based student data synchronization.

## 👨‍💻 Author

**Ashish Prajapati**

GitHub: https://github.com/prajapatiashish85

---

⭐ If you find this project useful, consider giving the repository a star!