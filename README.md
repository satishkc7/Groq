# FoodPass Chatbot

A conversational AI chatbot built with Streamlit and Groq that provides information about the FoodPass investment offering on StartEngine.

## Features

- 🤖 Conversational AI powered by Groq's Llama3-8b model
- 🔍 Web scraping of FoodPass StartEngine page
- 📚 RAG (Retrieval-Augmented Generation) for accurate responses
- 💬 Interactive chat interface
- 🎨 Modern, responsive UI

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq (Llama3-8b-8192)
- **Embeddings**: OpenAI
- **Vector Store**: FAISS
- **Web Scraping**: BeautifulSoup
- **Framework**: LangChain

## Local Development

### Prerequisites

- Python 3.8+
- Groq API key
- OpenAI API key

### Quick Setup (Recommended)

1. **Run the setup script**:
```bash
cd Groq
./venv_setup.sh
```

2. **Edit the `.env` file** with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Activate virtual environment and run**:
```bash
source venv/bin/activate
streamlit run streamlit_chatbot.py
```

### Manual Setup

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd Groq
```

2. **Create and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create `.env` file**:
```bash
cp env_example.txt .env
# Edit .env with your actual API keys
```

5. **Run the application**:
```bash
streamlit run streamlit_chatbot.py
```

## Deployment

### Streamlit Cloud (Recommended)

**No virtual environment needed** - Streamlit Cloud handles this automatically!

1. **Push to GitHub**: Ensure your code is in a GitHub repository

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and branch
   - Set the main file path: `Groq/streamlit_chatbot.py`
   - Add your secrets in the advanced settings:
     ```
     GROQ_API_KEY = your_groq_api_key_here
     OPENAI_API_KEY = your_openai_api_key_here
     ```
   - Click "Deploy"

### Alternative Deployment Options

#### Heroku
1. Create a `Procfile`:
```
web: streamlit run streamlit_chatbot.py --server.port=$PORT --server.address=0.0.0.0
```

2. Set environment variables in Heroku dashboard

#### Railway
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |
| `OPENAI_API_KEY` | Your OpenAI API key for embeddings | Yes |

## Usage

1. Open the deployed application
2. Click "🚀 Setup FoodPass Chatbot" in the sidebar
3. Wait for the model to initialize
4. Start chatting about FoodPass!

## Project Structure

```
Groq/
├── streamlit_chatbot.py    # Main application
├── requirements.txt        # Python dependencies
├── venv_setup.sh          # Quick setup script
├── env_example.txt        # Environment variables template
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── README.md              # This file
├── Procfile               # Heroku deployment
├── runtime.txt            # Python version
└── .env                   # Environment variables (local only)
```

## Virtual Environment Management

### Local Development
- **Activate**: `source venv/bin/activate`
- **Deactivate**: `deactivate`
- **Install new package**: `pip install package_name`
- **Update requirements**: `pip freeze > requirements.txt`

### Streamlit Cloud
- **No setup needed** - automatically managed
- **Dependencies**: Installed from `requirements.txt`
- **Environment**: Isolated per app

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 