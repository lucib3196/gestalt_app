
# 🚀 Setup Instructions for `gestalt_app`

> 🧠 **Note**: This project has been tested with:
>
> - **Python 3.13.1**
> - **Node.js v22.14.0**
>
> These are very recent versions. While they should work fine, be aware that **some dependencies may not yet fully support these versions**. If you run into issues, consider switching to:
> - Python 3.10–3.11
> - Node.js 18–20

---

## 📦 Backend Setup

1. **Navigate to the root directory**:
   ```
   cd gestalt_app
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   ```

   - **On Windows**:
     ```
     .venv\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```
     source .venv/bin/activate
     ```

3. **Install required Python packages**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the backend server** from the root directory:
   ```bash
   python -m backend.main
   ```

5. **Access the API documentation**:
   ```
   http://127.0.0.1:8000/docs
   ```

---

## 🔐 Create `.env` File

1. **In the root directory**, create a `.env` file:
   ```bash
   echo. > .env
   ```

2. **Paste the following into `.env`**:
   ```
   OPENAI_API_KEY=your_api_key_here
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your_api_key_here
   LANGCHAIN_PROJECT="Engineering_Tutor"
   ```

---

## 💻 Frontend Setup

1. **Navigate to the frontend folder**:
   ```bash
   cd gestalt
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

---

## 🔄 Running Everything Together

- Open **two terminal windows**:
  - One for the backend (`python -m backend.main`)
  - One for the frontend (`npm run dev` inside `gestalt/`)

- On first startup, a **database file will be created** automatically in the at `backend\data\database.db` this will store all the generated data. There are other databases present however these have different uses. 
