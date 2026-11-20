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
