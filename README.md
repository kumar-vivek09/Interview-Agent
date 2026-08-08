# The Interview Agent

This project is an Interview Operating System that uses a deterministic planner to control the interview structure, coverage, and progression, while utilizing Gemini 2.5 Pro for natural language interactions and evaluations.

## Prerequisites
- Python 3.10+
- Node.js & npm

---

## 1. Environment Setup

Before starting the application, you must provide your Gemini API key.

1. Open the file `backend/.env` (or create it if it doesn't exist).
2. Add your API key like so:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

---

## 2. Starting the Backend Server

The backend is built with FastAPI and runs on port `8000`.

1. Open a terminal and navigate to the backend folder:
   ```powershell
   cd backend
   ```
2. Activate the Python virtual environment:
   ```powershell
   .\venv\Scripts\activate
   ```
3. Start the FastAPI server using uvicorn:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   *The backend will now be accessible at http://localhost:8000*

---

## 3. Starting the Frontend Server

The frontend is built with React, Vite, TailwindCSS, and Shadcn UI. It runs on port `5173`.

1. Open a **new** separate terminal and navigate to the frontend folder:
   ```powershell
   cd frontend
   ```
2. Start the Vite development server:
   ```powershell
   npm run dev
   ```
   *The frontend will now be accessible at http://localhost:5173*

---

## Accessing the Application
Once both servers are running, open your web browser and navigate to:
**http://localhost:5173**

Click "Start Interview" to begin your mock session!
