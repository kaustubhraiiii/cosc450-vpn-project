#!/bin/bash
   
   echo "=========================================="
   echo "Current Routing Table"
   echo "=========================================="
   ip route show
   echo ""
   
   echo "=========================================="
   echo "VPN Interface Status"
   echo "=========================================="
   if ip addr show tun0 &>/dev/null; then
       ip addr show tun0 | grep -E "inet |state"
       echo "VPN: CONNECTED"
   else
       echo "VPN: DISCONNECTED"
   fi
   echo ""
   
   echo "=========================================="
   echo "Default Gateway"
   echo "=========================================="
   ip route | grep default
   echo ""
   
   echo "=========================================="
   echo "DNS Servers"
   echo "=========================================="
   resolvectl status | grep -A 3 "DNS Servers"
