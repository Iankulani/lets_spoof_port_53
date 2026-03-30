#!/bin/bash
# install.sh - Linux installation script for LETS-SPOOF-PORT-53

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LETS-SPOOF-PORT-53 - Linux Installation                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root (sudo ./install.sh)${NC}"
    exit 1
fi

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
else
    echo -e "${RED}❌ Cannot detect Linux distribution${NC}"
    exit 1
fi

echo -e "${GREEN}📋 Detected: $OS $VER${NC}"

# Install system dependencies based on distribution
install_dependencies() {
    echo -e "${YELLOW}📦 Installing system dependencies...${NC}"
    
    case $OS in
        ubuntu|debian)
            apt-get update
            apt-get install -y \
                python3 python3-pip python3-dev python3-venv \
                git curl wget vim \
                nmap hping3 traceroute dnsutils whois net-tools \
                iproute2 arp-scan ettercap-text-only dsniff \
                libpcap-dev libffi-dev libssl-dev \
                build-essential \
                chromium-browser chromium-chromedriver \
                sqlite3 \
                tcpdump \
                iptables \
                netcat-openbsd \
                openssh-client
            ;;
        
        rhel|centos|fedora)
            if command -v dnf &> /dev/null; then
                dnf install -y epel-release
                dnf install -y \
                    python3 python3-pip python3-devel \
                    git curl wget vim \
                    nmap hping3 traceroute bind-utils whois net-tools \
                    iproute arp-scan ettercap dsniff \
                    libpcap-devel libffi-devel openssl-devel \
                    gcc gcc-c++ make \
                    chromium chromium-headless chromedriver \
                    sqlite \
                    tcpdump \
                    iptables \
                    nc \
                    openssh-clients
            else
                yum install -y epel-release
                yum install -y \
                    python3 python3-pip python3-devel \
                    git curl wget vim \
                    nmap hping3 traceroute bind-utils whois net-tools \
                    iproute arp-scan ettercap dsniff \
                    libpcap-devel libffi-devel openssl-devel \
                    gcc gcc-c++ make \
                    chromium chromium-headless chromedriver \
                    sqlite \
                    tcpdump \
                    iptables \
                    nc \
                    openssh-clients
            fi
            ;;
        
        arch)
            pacman -S --noconfirm \
                python python-pip \
                git curl wget vim \
                nmap hping traceroute bind-tools whois net-tools \
                iproute2 arp-scan ettercap dsniff \
                libpcap libffi openssl \
                base-devel \
                chromium chromedriver \
                sqlite \
                tcpdump \
                iptables \
                gnu-netcat \
                openssh
            ;;
        
        *)
            echo -e "${RED}❌ Unsupported distribution: $OS${NC}"
            exit 1
            ;;
    esac
}

# Create virtual environment
setup_venv() {
    echo -e "${YELLOW}🐍 Setting up Python virtual environment...${NC}"
    
    cd /opt
    if [ ! -d "lets-spoof-port-53" ]; then
        git clone https://gitlab.com/your-repo/lets-spoof-port-53.git
    fi
    
    cd lets-spoof-port-53
    python3 -m venv venv
    source venv/bin/activate
    
    echo -e "${GREEN}✅ Virtual environment created${NC}"
}

# Install Python requirements
install_python_requirements() {
    echo -e "${YELLOW}📚 Installing Python packages...${NC}"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        pip install \
            scapy \
            colorama \
            requests \
            psutil \
            paramiko \
            flask \
            flask-socketio \
            python-telegram-bot \
            discord.py \
            slack-sdk \
            twilio \
            python-whois \
            qrcode \
            pyshorteners \
            shodan \
            python-hunter \
            phonenumbers \
            selenium \
            pandas \
            matplotlib \
            seaborn \
            numpy \
            reportlab \
            aiohttp \
            websockets \
            cryptography
    fi
    
    echo -e "${GREEN}✅ Python packages installed${NC}"
}

# Configure system
configure_system() {
    echo -e "${YELLOW}⚙️  Configuring system...${NC}"
    
    # Create application user
    if ! id "spoof53" &>/dev/null; then
        useradd -m -s /bin/bash spoof53
        echo "spoof53 ALL=(ALL) NOPASSWD: /usr/sbin/arp" >> /etc/sudoers
        echo "spoof53 ALL=(ALL) NOPASSWD: /usr/sbin/iptables" >> /etc/sudoers
    fi
    
    # Create directories
    mkdir -p /opt/lets-spoof-port-53/.lets-spoof-port-53
    mkdir -p /opt/lets-spoof-port-53/reports
    mkdir -p /var/log/spoof53
    
    # Set permissions
    chown -R spoof53:spoof53 /opt/lets-spoof-port-53
    chown -R spoof53:spoof53 /var/log/spoof53
    
    # Enable IP forwarding for better spoofing
    echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
    sysctl -p
    
    echo -e "${GREEN}✅ System configured${NC}"
}

# Create systemd service
create_service() {
    echo -e "${YELLOW}🔧 Creating systemd service...${NC}"
    
    cat > /etc/systemd/system/spoof53.service << EOF
[Unit]
Description=LETS-SPOOF-PORT-53 Security Tool
After=network.target

[Service]
Type=simple
User=spoof53
WorkingDirectory=/opt/lets-spoof-port-53
Environment="PATH=/opt/lets-spoof-port-53/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/opt/lets-spoof-port-53/venv/bin/python3 /opt/lets-spoof-port-53/lets_spoof_port_53.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable spoof53
    
    echo -e "${GREEN}✅ Service created${NC}"
}

# Create desktop entry (for GUI)
create_desktop_entry() {
    echo -e "${YELLOW}🖥️  Creating desktop entry...${NC}"
    
    cat > /usr/share/applications/spoof53.desktop << EOF
[Desktop Entry]
Name=LETS-SPOOF-PORT-53
Comment=Ultimate Multi-Platform Cybersecurity Command & Control Center
Exec=sudo /opt/lets-spoof-port-53/venv/bin/python3 /opt/lets-spoof-port-53/lets_spoof_port_53.py
Icon=/opt/lets-spoof-port-53/icon.png
Terminal=true
Type=Application
Categories=Network;Security;
EOF

    echo -e "${GREEN}✅ Desktop entry created${NC}"
}

# Setup completion script
setup_completion() {
    echo -e "${YELLOW}📝 Setting up command completion...${NC}"
    
    cat > /etc/bash_completion.d/spoof53 << 'EOF'
_spoof53_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="spoof_dns53 spoof_ip spoof_mac arp_spoof stop_spoof nmap ping traceroute dig whois icmp_flood syn_flood udp_flood phish status history help"
    
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}
complete -F _spoof53_completion spoof53
EOF

    echo -e "${GREEN}✅ Command completion configured${NC}"
}

# Create alias
create_alias() {
    echo -e "${YELLOW}🔗 Creating command alias...${NC}"
    
    cat >> /etc/profile.d/spoof53.sh << 'EOF'
alias spoof53='sudo /opt/lets-spoof-port-53/venv/bin/python3 /opt/lets-spoof-port-53/lets_spoof_port_53.py'
alias spoof53-cli='sudo /opt/lets-spoof-port-53/venv/bin/python3 /opt/lets-spoof-port-53/lets_spoof_port_53.py'
EOF

    chmod +x /etc/profile.d/spoof53.sh
    
    echo -e "${GREEN}✅ Alias created${NC}"
}

# Main installation
main() {
    install_dependencies
    setup_venv
    install_python_requirements
    configure_system
    create_service
    create_desktop_entry
    setup_completion
    create_alias
    
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    Installation Complete!                       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${GREEN}✅ LETS-SPOOF-PORT-53 has been installed successfully!${NC}"
    echo -e ""
    echo -e "${YELLOW}To start the tool:${NC}"
    echo -e "  spoof53"
    echo -e ""
    echo -e "${YELLOW}To run as a service:${NC}"
    echo -e "  sudo systemctl start spoof53"
    echo -e ""
    echo -e "${YELLOW}To view logs:${NC}"
    echo -e "  sudo journalctl -u spoof53 -f"
    echo -e ""
    echo -e "${YELLOW}Configuration files:${NC}"
    echo -e "  /opt/lets-spoof-port-53/.lets-spoof-port-53/"
    echo -e ""
    echo -e "${BLUE}🔮 Happy Spoofing!${NC}"
}

main