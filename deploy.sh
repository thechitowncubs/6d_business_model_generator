#!/bin/bash
# 🧊 3D Data Cube - All-In-One Automated Production Deployment

# Exit immediately if a command exits with a non-zero status
set -e

APP_DIR=$(pwd)
USER_NAME=$(whoami)
SERVICE_NAME="cube_bot"
PORT=5000
ENV_FILE="$APP_DIR/.env"
REQ_FILE="$APP_DIR/requirements.txt"

echo "🧊 Initializing Production Environment..."

# 1. Generate requirements.txt inline
echo "-> Creating requirements.txt..."
cat << 'EOF' > "$REQ_FILE"
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
pandas==2.1.1
google-genai
gunicorn==21.2.0
EOF

# 2. Virtual Environment & Dependencies
echo "-> Creating Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo "-> Installing dependencies from generated requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. API Key Management
if [ ! -f "$ENV_FILE" ]; then
    echo "--------------------------------------------------------"
    read -p "Enter your Google Gemini API Key: " api_key
    echo "--------------------------------------------------------"
    echo "GEMINI_API_KEY=$api_key" > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    echo "-> Created secure .env file."
fi

# 4. Systemd Service Creation
echo "-> Writing Systemd Service file..."
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Gunicorn daemon for 3D Data Cube Business Plan Bot
After=network.target

[Service]
User=$USER_NAME
Group=www-data
WorkingDirectory=$APP_DIR
EnvironmentFile=$ENV_FILE
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:$PORT app:app

[Install]
WantedBy=multi-user.target
EOF

# 5. Boot the Engine
echo "-> Reloading systemd daemon and starting service..."
sudo systemctl daemon-reload
sudo systemctl start $SERVICE_NAME
sudo systemctl enable $SERVICE_NAME

echo "========================================================"
echo "✅ Deployment Complete!"
echo "-> Gunicorn is running internally on 127.0.0.1:$PORT"
echo "-> requirements.txt was successfully written and processed."
echo "========================================================"
