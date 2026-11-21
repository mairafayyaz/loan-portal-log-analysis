# Secure the Loan Portal: Log Analysis and Threat Model

Simulated security log analysis, system architecture mapping, and STRIDE threat modeling project for the **Roshan Microfinance** loan portal using sample data only.

## Repository Contents

* `access.log` - Sample web server log containing normal activity and simulated attack traffic (`400`, `401`, `403`, and `500` responses plus SQL injection patterns).
* `analyze_logs.py` - Python script that scans `access.log` and flags suspicious HTTP status codes and SQL injection strings.
* `findings.txt` - Output generated from reviewing suspicious log entries in `access.log`.
* `system_diagram.drawio.png` - System architecture diagram showing the User Interface (Client), Webserver, and Database along with HTTP and SQL data flows.
* `components.txt` - Short description of each component in the loan portal diagram and its role.
* `threat_model.md` - STRIDE threat model ranking risks (`High`, `Medium`, `Low`) and listing proposed mitigations.

## How to Run the Log Analysis Script

1. Make sure Python 3 is installed and `access.log` is in the same directory as `analyze_logs.py`.
2. Run the script from your terminal or command prompt:

```bash
python analyze_logs.py
## Threat Model Summary

Using the 3-tier portal diagram and log findings from `access.log`, five STRIDE threats were identified, ranked by risk level, and paired with mitigations (full details in `threat_model.md`):

* **Tampering (High):** SQL injection payloads (`UNION SELECT` and `SELECT *`) targeting `/portal/admin` and `/portal/transfer`, mitigated with parameterized queries and strict input validation.
* **Information Disclosure (High):** Potential exposure of `User Credentials`, `Account Data`, or internal server details via SQL injection or verbose `500` responses, mitigated with strong password hashing, least-privilege database accounts, generic error pages, and HTTPS.
* **Spoofing (Medium):** Unauthenticated probing (`401`) on `/portal/balance` and `/portal/settings` plus a blocked login attempt (`403` on `POST /portal/login`), mitigated with strict session checks, login rate limiting, and monitoring for repeated failed attempts from the same IP.
* **Elevation of Privilege (Medium):** Potential unauthorized access to administrative endpoints (`/portal/admin`) or fund transfers (`/portal/transfer`), mitigated with server-side role-based access control (RBAC) on every request.
* **Denial of Service (Low):** Heavy queries, malformed requests, or repeated login attempts affecting portal availability or filling up logs, mitigated with rate limiting, database query timeouts, and log rotation.
