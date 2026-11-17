with open("access.log", "r") as file:
    logs = file.readlines()

print("=== Scanning Logs for Suspicious Activity ===")

for line in logs:
    clean_line = line.strip()
    if "UNION" in clean_line or "SELECT" in clean_line:
        print(f"{clean_line} -> [SQL Injection] Attacker is trying to dump user credentials or bank account data from the database.")
    elif "401" in clean_line:
        print(f"{clean_line} -> [Unauthorized Access] Attacker is probing restricted pages without valid login credentials.")
    elif "403" in clean_line:
        print(f"{clean_line} -> [Forbidden Access] Attacker is attempting unauthorized actions on the login endpoint.")
    elif "400" in clean_line or "500" in clean_line:
        print(f"{clean_line} -> [Server/Request Error] Malformed input or backend query crash indicating active probing.")
