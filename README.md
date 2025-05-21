
---

# 🚀 `gestalt_app` Setup Instructions

> **Tested With:**
>
> * Python **3.13.1**
> * Node.js **v22.14.0**
>

> ⚠️ *Note*: These are bleeding-edge versions. Some dependencies may not be fully compatible. If you encounter issues, try:
>
> * Python **3.10–3.11**
> * Node.js **18–20**
>
> 🛠️ If you run into build tool issues on Windows, refer to:
> [Visual Studio Build Tools Guide](https://devblogs.microsoft.com/cppblog/introducing-the-visual-studio-build-tools/)

---

## 🗂️ Project Structure (inside `/src`)

| Folder         | Description                                                                       |
| -------------- | --------------------------------------------------------------------------------- |
| `ai_workspace` | AI tools and components used in the platform                                      |
| `backend`      | FastAPI-based backend server                                                      |
| `gestalt`      | Frontend React application                                                        |
| `htmltool`     | HTML processing tools *(currently being refactored)*                              |
| `schemas`      | Pydantic models for FastAPI and the code generator *(currently being refactored)* |

---

## 🐍 Backend Setup

### 1. **Create and activate a virtual environment**:

```bash
python -m venv .venv
```

* **Windows**:

  ```
  .venv\Scripts\activate
  ```
* **macOS/Linux**:

  ```
  source .venv/bin/activate
  ```

### 2. **Install required Python packages**:

```bash
pip install -r requirements.txt
```

### 3. **Run the backend server**:

```bash
python -m backend.main
```

### 4. **Open the API documentation**:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 Environment Configuration

### 1. **Create a `.env` file** in the root directory:

```bash
echo. > .env
```

### 2. **Add the following to `.env`**:

```
OPENAI_API_KEY=your_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_api_key_here
LANGCHAIN_PROJECT="Engineering_Tutor"
```

---

## 💻 Frontend Setup

### 1. **Navigate to the frontend folder**:

```bash
cd src/gestalt
```

### 2. **Install dependencies**:

```bash
npm install
```

### 3. **Start the frontend development server**:

```bash
npm run dev
```

---

## 🔄 Running Everything Together

* Open **two terminal windows**:

  * **Terminal 1 (Backend)**:

    ```bash
    python -m backend.main
    ```
  * **Terminal 2 (Frontend)**:

    ```bash
    cd src/gestalt
    npm run dev
    ```

> On first run, a database will be created at `src/backend/data/database.db`.
> Other database files may exist for separate features or testing purposes.

---

## 📚 Resources

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [OpenAI Cookbook](https://cookbook.openai.com/)
* [LangGraph (LangChain)](https://www.langchain.com/langgraph)
* [React Documentation](https://react.dev/)

---

