#!/bin/bash

# Virtual Environment Setup Script for FoodPass Chatbot

echo "🚀 Setting up virtual environment for FoodPass Chatbot..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔑 Creating .env file..."
    cp env_example.txt .env
    echo "⚠️  Please edit .env file with your actual API keys!"
fi

echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "source venv/bin/activate"
echo ""
echo "To run the app:"
echo "streamlit run streamlit_chatbot.py"
echo ""
echo "To deactivate:"
echo "deactivate" 