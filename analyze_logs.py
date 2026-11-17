with open("access.log", "r") as file:
    logs = file.readlines()

print("=== Scanning Logs for Suspicious Activity ===")

for line in logs:
    clean_line = line.strip()
    labels = []

    if " 500 " in clean_line:
        labels.append("[500 Internal Server Error] Backend database crashed/errored, input reached the query")
    if " 400 " in clean_line:
        labels.append("[400 Bad Request] Malformed request rejected by server")
    if " 401 " in clean_line:
        labels.append("[401 Unauthorized] Attacker probing restricted pages without valid login credentials")
    if " 403 " in clean_line:
        labels.append("[403 Forbidden] Blocked login attempt, single request is not brute force")

    if "UNION SELECT" in clean_line:
        labels.append("[SQL Injection] Attacker trying to dump user credentials from database via UNION")
    elif "SELECT *" in clean_line:
        labels.append("[SQL Injection] Attacker trying to extract and enumerate account data records")

    if labels:
        print(f"{clean_line} -> {' | '.join(labels)}")
