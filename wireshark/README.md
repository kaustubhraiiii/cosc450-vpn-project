# Wireshark OpenVPN Analysis

## Capture Files

- baseline_no_vpn.pcapng  
  Captured on interface enp0s3 without OpenVPN enabled.  
  Shows plaintext ARP, TCP, DNS, and ICMP traffic.

- with_vpn.pcapng  
  Captured on interface enp0s3 with OpenVPN enabled.  
  Only encrypted UDP tunnel traffic is visible; no application-layer payloads.

## Conclusion

These captures demonstrate that OpenVPN successfully encrypts network traffic
and prevents exposure of application-layer data on the physical interface.

