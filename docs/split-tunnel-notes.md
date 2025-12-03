# Split Tunneling Configuration
   
   ## Overview
   Split tunneling allows selective routing of traffic. Only specified
   networks go through VPN, rest goes through local gateway.
   
   ## Use Cases
   - Reduce VPN load for general internet browsing
   - Route only application traffic through VPN
   - Maintain local network access while on VPN
   - Improve performance for non-sensitive traffic
   
   ## Configuration
   
   ### Server Files
   - Full tunnel: `/etc/openvpn/server/server.conf`
   - Split tunnel: `/etc/openvpn/server/server-split.conf`
   
   ### Switching Modes
```bash
   ~/cosc450-vpn-project/scripts/switch-vpn-mode.sh [full|split]
```
   
   ### Routes Pushed in Split Mode
   - 10.8.0.0/24 - VPN subnet
   - 192.168.56.0/24 - Lab network
   
   ## Testing
   
   ### Full Tunnel
   - Default route through tun0
   - All internet traffic via VPN server
   - Public IP shows server's IP
   
   ### Split Tunnel
   - No default route through tun0
   - Only specified networks via VPN
   - Public IP shows client's real IP
   - Local gateway used for internet
   
   ## Performance Comparison
   [To be filled after testing]
