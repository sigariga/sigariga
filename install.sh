#!/bin/bash

echo "🚀 Setting up Work Instruction Creator..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install client dependencies
echo "📦 Installing client dependencies..."
cd client
npm install
cd ..

# Install server dependencies
echo "📦 Installing server dependencies..."
cd server
npm install

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating environment file..."
    cp .env.example .env
    echo "📝 Please edit server/.env to add your OpenAI API key (optional)"
fi

cd ..

echo "🎉 Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. (Optional) Edit server/.env to add your OpenAI API key for AI features"
echo "2. Run 'npm run dev' to start the development server"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "🔧 Available commands:"
echo "  npm run dev     - Start both frontend and backend"
echo "  npm run client  - Start only frontend"
echo "  npm run server  - Start only backend"
echo "  npm run build   - Build for production"
echo ""
echo "📖 See README.md for detailed documentation"