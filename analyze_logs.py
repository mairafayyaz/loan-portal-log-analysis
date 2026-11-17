with open("access.log", "r") as file:
    logs = file.readlines()

print("=== Scanning Logs for Suspicious Activity ===")

for line in logs:
    clean_line = line.strip()
    labels = []

    # Check status codes first
    if " 500 " in clean_line:
        labels.append("[500 Internal Server Error] Backend database crashed/errored — input reached the query")
    if " 400 " in clean_line:
        labels.append("[400 Bad Request] Malformed request rejected by server")
    if " 401 " in clean_line:
        labels.append("[401 Unauthorized] Attacker probing restricted pages without valid login credentials")
    if " 403 " in clean_line:
        labels.append("[403 Forbidden] Attacker attempting unauthorized actions on login endpoint")

    # Check SQL injection patterns separately so both labels get attached
    if "UNION SELECT" in clean_line or "SELECT *" in clean_line:
        labels.append("[SQL Injection] Attacker trying to dump user credentials or bank account data")

    if labels:
        print(f"{clean_line} -> {' | '.join(labels)}")
