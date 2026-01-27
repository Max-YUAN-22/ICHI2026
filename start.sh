#!/bin/bash

echo "🚀 Starting AI Cancer Navigation Agent..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# 安装依赖
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# 启动服务器
echo ""
echo "✅ Starting Flask server..."
echo "🌐 Open http://localhost:5000 in your browser"
echo ""
python3 app.py

