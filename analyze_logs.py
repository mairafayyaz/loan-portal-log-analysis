# Open and read the access log file
with open("access.log", "r") as file:
    logs = file.readlines()

print("=== Scanning Logs for Suspicious Activity ===")

# Updated keywords list including 400, 500, SELECT, and UNION
keywords = ['401', '403', '400', '500', 'SELECT', 'UNION']

for line in logs:
    if any(key in line for key in keywords):
        print(line.strip())
