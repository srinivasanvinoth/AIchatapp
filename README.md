# React + FastAPI + DynamoDB Chat

A starter chat UI with:

- React + Vite frontend
- FastAPI backend
- DynamoDB Users table
- DynamoDB Conversations table
- Signup with first name, last name, email, login ID, and password
- Login with login ID and password
- JWT authentication
- User profile in the top-right corner
- Multiple conversations
- Persistent chat messages in DynamoDB

## Project structure

```text
react-fastapi-dynamodb-chat/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── database/
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── routers/
│   │   └── main.py
│   ├── create_tables.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   └── .env.example
└── README.md
```

## 1. Configure AWS

Install/configure AWS CLI, or use an AWS IAM role.

```bash
aws configure
```

Default region in this sample:

```text
ap-south-1
```

## 2. Backend setup

```bash
cd backend

python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example environment file:

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Edit `.env` and change:

```text
JWT_SECRET_KEY
```

to a long random secret.

## 3. Create DynamoDB tables

```bash
python create_tables.py
```

This creates:

### Users

Primary key:

```text
user_id
```

GSIs:

```text
login_id-index
email-index
```

### Conversations

Primary key:

```text
conversation_id
```

GSI:

```text
user_id-index
```

## 4. Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

API:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/swagger
```

ReDoc:

```text
http://localhost:8000/redoc
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

### Using JWT in Swagger

1. Call `POST /api/auth/signup` or `POST /api/auth/login`.
2. Copy the returned `access_token`.
3. Click **Authorize** in Swagger UI.
4. Enter the token as:

```text
Bearer YOUR_ACCESS_TOKEN
```

5. You can now test secured user and conversation endpoints from Swagger.

## 5. Frontend setup

Open another terminal:

```bash
cd frontend
npm install
```

Copy environment config:

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Start:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

## APIs

```text
POST   /api/auth/signup
POST   /api/auth/login
GET    /api/users/me

POST   /api/conversations
GET    /api/conversations
GET    /api/conversations/{conversation_id}
POST   /api/conversations/{conversation_id}/messages
PUT    /api/conversations/{conversation_id}
DELETE /api/conversations/{conversation_id}
```

## Current chat behavior

The Send button stores user messages in DynamoDB.

There is no LLM integration yet. You can later connect Gemini, LangChain, or LangGraph inside the message endpoint and store assistant responses using role `assistant`.

## DynamoDB note

This starter intentionally uses exactly two tables as requested. Messages are embedded in each conversation item. For very large chat histories, a production design should normally move messages into a separate table because DynamoDB items have a size limit.


## LangGraph PDF question answering

The project now contains a PDF RAG workflow using LangGraph.

Flow:

```text
React Chat
   |
   +-- Upload PDF
   |       |
   |       v
   |   FastAPI /api/pdf/upload
   |       |
   |       v
   |   PyPDFLoader
   |       |
   |       v
   |   Recursive text chunking
   |       |
   |       v
   |   Gemini Embeddings
   |       |
   |       v
   |   Local FAISS index per user
   |
   +-- Ask Question
           |
           v
      FastAPI /api/pdf/ask
           |
           v
      LangGraph
       START
         |
         v
      retrieve_pdf_context
         |
         v
      answer_from_pdf
         |
         v
        END
```

The LangGraph system prompt is in:

```text
backend/app/langgraph_pdf/graph.py
```

It instructs the model to use only retrieved PDF context and return a clear
"not enough information" response when the PDF does not contain an answer.

### Required Gemini configuration

Copy `.env.example` to `.env`, then set:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_CHAT_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
PDF_TOP_K=4
```

### New APIs in Swagger

```text
POST /api/pdf/upload
POST /api/pdf/ask
```

Swagger UI:

```text
http://localhost:8000/swagger
```

For `/api/pdf/upload`, authorize with your JWT and select a `.pdf` file.

For `/api/pdf/ask`, example request:

```json
{
  "question": "What are the main findings in the document?"
}
```

The React chat UI now has an **Upload PDF** button. Once a PDF is indexed,
messages entered in the chat are sent to the LangGraph PDF workflow and the
assistant answer is saved into the same DynamoDB conversation.


## Gemini API key

The LangGraph PDF RAG workflow uses Google Gemini for both generation and embeddings.

Configure `backend/.env`:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_CHAT_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
PDF_TOP_K=4
```

The Gemini API key is read only by the FastAPI backend. Do not put the key in the React `.env` file or expose it through `VITE_` variables.
