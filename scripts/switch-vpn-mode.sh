#!/bin/bash
   
   # Script to switch between full tunnel and split tunnel VPN
   # Usage: ./switch-vpn-mode.sh [full|split]
   
   MODE=$1
   
   if [ -z "$MODE" ]; then
       echo "Usage: $0 [full|split]"
       echo ""
       echo "  full  - All traffic through VPN (default)"
       echo "  split - Only specific routes through VPN"
       exit 1
   fi
   
   if [ "$MODE" == "full" ]; then
       echo "Switching to FULL TUNNEL mode..."
       sudo systemctl stop openvpn-server@server-split 2>/dev/null
       sudo systemctl start openvpn-server@server
       echo "✓ Full tunnel mode activated"
       
   elif [ "$MODE" == "split" ]; then
       echo "Switching to SPLIT TUNNEL mode..."
       sudo systemctl stop openvpn-server@server 2>/dev/null
       sudo systemctl start openvpn-server@server-split
       echo "✓ Split tunnel mode activated"
       
   else
       echo "Error: Invalid mode '$MODE'"
       echo "Use 'full' or 'split'"
       exit 1
   fi
   
   echo ""
   echo "Current VPN server status:"
   sudo systemctl status openvpn-server@* --no-pager | grep -E "Loaded|Active"
   echo ""
   echo "Clients will need to reconnect to VPN"
