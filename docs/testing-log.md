# COSC 450 Final Project - Integration Testing Log  
Author: Longyu Tang

---

## Test Environment

- OS: Ubuntu Linux (VirtualBox VM)
- Python Version: 3.12
- File Size Tested: 5 MB
- Application: File Transfer Application
- VPN: OpenVPN (TUN interface)
- Application-layer Encryption: TLS/SSL (Python `ssl` module)

---

## Test Scenarios

| Scenario | VPN | SSL | File Transfer Result | Notes |
|---------|-----|-----|----------------------|-------|
| A. Baseline (Plain TCP) | No | No | ✅ Success | Localhost transfer over plain TCP |
| B. VPN Only | Yes | No | ✅ Success | File transfer over OpenVPN tunnel (tun0) |
| C. SSL Only | No | Yes | ✅ Success | TLS-enabled file transfer over localhost |
| D. VPN + SSL | Yes | Yes | ✅ Success | TLS-encrypted file transfer tunneled through OpenVPN |

---

## Detailed Observations

### A. Baseline (No VPN, No SSL)
- Server and client communicated over `127.0.0.1`
- File transferred successfully with checksum verification
- Served as the performance and correctness baseline

### B. VPN Only
- OpenVPN client established a tunnel (`tun0`) with IP `10.8.0.x`
- Client connected to server via VPN address `10.8.0.1`
- File transfer completed successfully without application-layer encryption
- Confirms that the VPN tunnel does not break raw TCP file transfer

### C. SSL Only
- TLS/SSL enabled using Python `ssl` module
- Communication conducted over `127.0.0.1`
- File transferred and checksum verified successfully
- Demonstrates correct application-layer encryption independently of VPN

### D. VPN + SSL
- OpenVPN tunnel active (`tun0`)
- TLS-enabled file transfer performed over VPN IP
- File transfer completed successfully with verified checksum
- Confirms that VPN (network-layer encryption) and TLS (application-layer encryption) can be safely combined

---

## Key Takeaways

- The file transfer application functions correctly in all four scenarios
- OpenVPN introduces a secure tunneled interface without breaking application behavior
- TLS encryption adds security at the application layer and works both with and without a VPN
- Combining VPN + SSL provides layered security with minimal functional impact

---

## Conclusion

These integration tests demonstrate that the file transfer system is robust across different security configurations.  
Both OpenVPN and TLS independently and jointly preserve correctness, validating the system’s design for secure network communication.

