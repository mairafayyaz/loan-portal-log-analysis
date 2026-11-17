with open("access.log", "r") as file:
    logs = file.readlines()
for line in logs:
    if "401" in line or "403" in line or "UNION" in line or "SELECT" in line:
        print(line.strip())
