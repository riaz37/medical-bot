# Medical Bot AI Application

An AI-powered medical question answering system using Retrieval Augmented Generation (RAG) with Google Generative AI and Pinecone vector database.

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - For the backend API
- **Node.js 18+** - For the frontend application
- **npm** - Node package manager
- **Google AI API Key** - For the language model
- **Pinecone API Key** - For vector database

### 🎯 One-Command Setup & Run

#### For Linux/macOS:

```bash
# Full setup with checks and error handling
./run-app.sh

# OR quick development start
./dev.sh
```

#### For Windows:

```batch
# Double-click or run from command prompt
run-app.bat
```

## 📋 Manual Setup

If you prefer to set up manually or the scripts don't work:

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv ../venv

# Activate virtual environment
source ../venv/bin/activate  # Linux/macOS
# OR
../venv/Scripts/activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env file with your API keys
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 3. Environment Configuration

Create a `.env` file in the `backend` directory with:

```env
# Google AI API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=medical-bot-index

# Application Configuration
APP_NAME=Medical Bot API
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
MAX_DOCUMENTS=1000
```

### 4. Manual Start

#### Backend:
```bash
cd backend
source ../venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend:
```bash
cd frontend
npm run dev
```

## 🌐 Access Points

Once running, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **AI Model**: Google Generative AI (Gemini)
- **Vector Database**: Pinecone
- **Document Processing**: LangChain
- **API Documentation**: Automatic OpenAPI/Swagger

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Query
- **HTTP Client**: Axios

## 📁 Project Structure

```
medical-bot/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration & logging
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment template
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API services
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node dependencies
│   └── vite.config.ts     # Vite configuration
├── data/                  # Document storage
├── venv/                  # Python virtual environment
├── run-app.sh            # Linux/macOS startup script
├── run-app.bat           # Windows startup script
├── dev.sh                # Quick development script
└── README.md             # This file
```

## 🔧 Development

### Adding Documents

Place PDF or text files in the `data/` directory. The backend will automatically process them on startup.

### API Endpoints

- `POST /api/v1/query` - Submit medical questions
- `GET /api/v1/search` - Search similar documents
- `POST /api/v1/upload` - Upload new documents
- `GET /api/v1/health` - Health check

### Frontend Development

```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run type-check   # TypeScript type checking
```

### Backend Development

```bash
cd backend
source ../venv/bin/activate
python -m uvicorn app.main:app --reload  # Development server
pytest                                   # Run tests (when implemented)
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**: The scripts will automatically kill processes on ports 3000 and 8000
2. **Virtual environment issues**: Delete `venv` folder and run the script again
3. **API key errors**: Make sure your `.env` file has valid API keys
4. **Node modules issues**: Delete `frontend/node_modules` and run `npm install`

### Getting Help

1. Check the console output for error messages
2. Verify all prerequisites are installed
3. Ensure API keys are valid and have proper permissions
4. Check that ports 3000 and 8000 are available

## 📝 License

This project is for educational and development purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
