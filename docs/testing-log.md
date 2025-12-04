# COSC 450 Final Project - Integration Testing Log
Author: Longyu Tang

## Test Environment
- OS: Ubuntu Linux
- Python Version: 3.12
- File Size Tested: 5 MB
- Application: File Transfer + Chat
- Encryption: TLS/SSL (Python ssl module)

---

| Scenario | VPN | SSL | File Transfer Result | Transfer Time | Notes |
|----------|-----|-----|----------------------|---------------|-------|
| A. Baseline | No  | No  | ✅ Success | ~0.8s  | Plain TCP, localhost |
| B. VPN Only | Yes | No  | ⚠️ Partial | ~0.5s  | Connection reset after ~40%, server tried to decode binary as UTF-8 |
| C. SSL Only | No  | Yes | ✅ Success | ~1.0s  | TLS enabled, localhost |
| D. VPN + SSL | Yes | Yes | ✅ Success | ~1.3s | VPN tunnel combined with TLS encryption |

---

## Observations
-## Observations

- In the VPN-only scenario, the file transfer failed at around 40% because the server attempted to decode raw binary data as UTF-8. This bug is independent of the VPN itself and highlights the importance of treating file payloads as bytes rather than text.
- SSL-only and VPN+SSL scenarios both completed successfully and verified checksums, showing that application-layer encryption does not break functionality, but adds some overhead.

