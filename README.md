# COSC 450 Final Project: OpenVPN Infrastructure

**Team:** Kaustubh Rai and Longyu Tang  
**Course:** COSC 450 - Computer Networks  
**Semester:** Fall 2025

## Project Overview
Advanced OpenVPN infrastructure with custom networked applications, featuring performance analysis and security evaluation.

## Components
1. ✅ OpenVPN Server/Client Infrastructure (Complete - Split Tunnel Mode)
2. ✅ Multi-Client Chat Application (Complete - Kaustubh)
3. 🔄 File Transfer Application (In Progress - Longyu)
4. 🔄 Performance Testing Framework (In Progress - Longyu)

## Project Structure
```
cosc450-vpn-project/
├── chat/               # Multi-client chat application
│   ├── server/        # Chat server (Kaustubh)
│   ├── client/        # Chat client (Kaustubh)
│   └── venv/          # Shared Python virtual environment
├── file-transfer/      # File transfer application
│   ├── server/        # File server (Longyu)
│   ├── client/        # File client (Longyu)
│   ├── shared/        # Protocol modules (Longyu)
│   └── venv/          # Python virtual environment
├── performance-tests/  # Performance testing scripts (Longyu)
├── scripts/           # Utility scripts
└── docs/              # Documentation
```

## Setup Instructions

### Prerequisites
- Ubuntu Desktop 22.04 LTS
- Python 3.10+
- OpenVPN installed and configured

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/cosc450-vpn-project.git
cd cosc450-vpn-project
```

2. **Set up Python virtual environment:**
```bash
cd file-transfer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

3. **Link virtual environment for chat:**
```bash
cd ../chat
ln -s ../file-transfer/venv venv
```

## Usage

### Chat Application

**Start Server:**
```bash
cd chat
source venv/bin/activate
python3 server/chat_server.py --host 0.0.0.0 --port 8888
```

**Start Client:**
```bash
cd chat
source venv/bin/activate
python3 client/chat_client.py --host 127.0.0.1 --username YourName
```

**Commands:**
- Type messages and press Enter to send
- `/quit` - Exit the chat

### File Transfer Application
[To be completed by Longyu - See implementation document]

## Team Responsibilities
- **Kaustubh Rai:** 
  - VPN infrastructure setup
  - OpenVPN configuration (split tunnel)
  - Multi-client chat application
  - Documentation

- **Longyu Tang:** 
  - File transfer application
  - Performance testing framework
  - Data collection and analysis
  - Results visualization

## Current Status
- **Week 1:** ✅ VPN infrastructure complete (split tunnel mode working)
- **Week 2:** ✅ Chat app complete, 🔄 File transfer in progress
- **Week 3:** 🔄 Integration testing planned
- **Week 4:** 🔄 Performance analysis & final report

## VPN Configuration
- **Mode:** Split Tunnel
- **VPN Subnet:** 10.8.0.0/24
- **Server IP:** 10.8.0.1
- **Client IP:** 10.8.0.2
- **Encryption:** AES-256-CBC
- **Authentication:** SHA256

## Testing
All applications tested over both:
- Direct connection (192.168.56.0/24)
- VPN connection (10.8.0.0/24)

## Documentation
See `/docs` directory for detailed setup and configuration notes.

## License
Academic project for COSC 450 - Computer Networks.
