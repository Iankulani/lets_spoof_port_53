#!/bin/bash
# quickstart.sh - Quick start script

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                     LETS-SPOOF-PORT-53 - Quick Start                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check platform
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=linux;;
    Darwin*)    PLATFORM=mac;;
    CYGWIN*)    PLATFORM=windows;;
    MINGW*)     PLATFORM=windows;;
    *)          PLATFORM=unknown;;
esac

echo -e "${GREEN}📋 Detected platform: $PLATFORM${NC}"

# Choose installation method
echo ""
echo -e "${YELLOW}Choose installation method:${NC}"
echo "1) Docker (Recommended)"
echo "2) Native Installation"
echo "3) Python Virtual Environment"
echo "4) Quick Test (Run without install)"
echo ""
read -p "Select option [1-4]: " choice

case $choice in
    1)
        echo -e "${GREEN}🐳 Installing with Docker...${NC}"
        if command -v docker &> /dev/null; then
            docker pull lets-spoof-port-53:latest
            docker run --rm -it --network host --privileged lets-spoof-port-53:latest
        else
            echo -e "${RED}❌ Docker not installed!${NC}"
            echo "Install Docker: https://docs.docker.com/get-docker/"
            exit 1
        fi
        ;;
    2)
        echo -e "${GREEN}💻 Installing natively...${NC}"
        case $PLATFORM in
            linux)
                curl -sSL https://gitlab.com/your-repo/lets-spoof-port-53/raw/main/install.sh | sudo bash
                ;;
            mac)
                echo "Mac installation coming soon"
                ;;
            windows)
                powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://gitlab.com/your-repo/lets-spoof-port-53/raw/main/install.ps1'))"
                ;;
        esac
        ;;
    3)
        echo -e "${GREEN}🐍 Setting up Python virtual environment...${NC}"
        python3 -m venv spoof53-env
        source spoof53-env/bin/activate
        pip install -r requirements.txt
        python3 lets_spoof_port_53.py
        ;;
    4)
        echo -e "${GREEN}🚀 Running quick test...${NC}"
        python3 -c "import sys; print('LETS-SPOOF-PORT-53 Quick Test')"
        python3 lets_spoof_port_53.py --help
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Done!${NC}"