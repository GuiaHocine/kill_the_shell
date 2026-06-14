# 🧠 #KillTheAbstraction: Linux VMS Visualizer

A real-time, interactive educational visualizer that demystifies the invisible mechanics of the Linux operating system. It translates text commands in a Bash shell into physical, spatial, and animated memory states.

## 🏗️ Architecture
This project uses a decoupled, modern web stack:
* **Frontend:** React, Vite, Tailwind CSS v4, and React Flow.
* **Backend:** Python, FastAPI.
* **Bridge:** WebSockets (for real-time, step-by-step kernel event streaming).

---

## 🚀 Quick Start Installation Guide

To run this project locally, you will need to spin up both the backend server and the frontend development server.

### Prerequisites
* **Python 3.9+** installed on your machine.
* **Node.js (v18+)** and `npm` installed.

### Step 1: Start the Backend (FastAPI)

1. Open a terminal and navigate to the backend folder:
   ```bash
   cd backend
   uv venv .venv
   source .venv/bin/activate  
   uvicorn main:app --reload


### Step 2: Start the Frontend (React + Vite)

1. cd kill-the-abstraction-ui
   ```
   npm install
   npm run dev