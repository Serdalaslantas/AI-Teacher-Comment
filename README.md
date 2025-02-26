# Student Progress Report Generator

An AI-powered application that generates personalized student progress reports using FastAPI, SQLite, and OpenAI's GPT-3.5. Teachers can provide sample comments and get AI-generated reports highlighting strengths, improvement areas, and academic targets.

![API Demo](https://img.shields.io/badge/Docs-Swagger%20UI-blue?style=flat&logo=swagger)

## Features

- 📝 Student management with grades tracking
- 🎓 AI-generated progress reports
- 📈 Short-term and long-term target suggestions
- 📚 One-shot learning with teacher-provided examples
- 📊 RESTful API endpoints for easy integration
- 🛠️ SQLite database with SQLAlchemy ORM

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- pip package manager

1. **Clone the repository**
```bash
git clone https://github.com/Serdalaslantas/AI-Teacher-Comment.git
cd student-report-generator

2. **Install dependencies**

bash

pip install fastapi uvicorn sqlalchemy python-dotenv openai
Set up environment variables
Create a .env file:

env

OPENAI_API_KEY=your_openai_api_key_here
Configuration
Get OpenAI API Key

Create account at OpenAI Platform

Generate API key in API Keys section

Initialize Database

The SQLite database will be automatically created on first run

Usage
Start the server

bash

uvicorn main:app --reload
Access API Documentation

Open Swagger UI: http://localhost:8000/docs

Alternative: Redoc at http://localhost:8000/redoc

Sample Workflow
Create a student

bash

curl -X POST "http://localhost:8000/students/" \
-H "Content-Type: application/json" \
-d '{"name": "John Doe"}'
Add grades

bash

curl -X POST "http://localhost:8000/students/1/grades/" \
-H "Content-Type: application/json" \
-d '{"subject": "Mathematics", "grade": 88}'
Save sample comment template

bash

curl -X POST "http://localhost:8000/sample-comment/" \
-H "Content-Type: application/json" \
-d '{"comment": "[Name] has shown strength in [subject]. Needs improvement in [area]. Targets: [short-term] and [long-term]"}'
Generate progress report

bash

curl -X POST "http://localhost:8000/generate-comment/1"
API Endpoints
Method	Endpoint	Description
POST	/students/	Create new student
POST	/students/{id}/grades/	Add grade for student
GET	/students/	List all students
POST	/sample-comment/	Save teacher's sample comment
GET	/sample-comment/	Get current sample comment
POST	/generate-comment/{id}	Generate AI-powered progress report

Example Response
json

{
  "student_id": 1,
  "comment": "John has demonstrated strong analytical skills in Mathematics... Short-term target: Improve geometry scores by 15%. Long-term target: Master calculus fundamentals."
}
Frontend Integration
While this repository focuses on the backend API, you can:

Create a React/Vue frontend using the provided endpoints

Use the Swagger UI for direct testing

Integrate with existing school management systems

License
MIT License - see LICENSE file

Note: Ensure your OpenAI API key has sufficient credits and the openai package is updated to avoid compatibility issues.
