# STRIDE Threat Model: Roshan Microfinance Loan Portal

This threat model covers the loan portal architecture (`system_diagram.drawio.png` and `components.txt`) across the User Interface (Client), Webserver, and Database, grounded in the sample log analysis from `access.log` and `findings.txt`.

## Identified STRIDE Threats

### 1. Tampering (SQL Injection on Account and Transfer Endpoints)
* **Category:** Tampering
* **Target Component and Flow:** Webserver to Database (`SQL Queries` and `Query Result`) on `/portal/transfer` and `/portal/admin`
* **Risk Level:** High
* **Description:** Attackers can inject SQL payloads into query parameters, such as `UNION SELECT` in `access.log` (producing a `500` error) and `SELECT *` on `/portal/transfer` (producing a `400` error). If unvalidated input reaches the query engine, an attacker can alter or extract database data.
* **Proposed Mitigation:** Use parameterized queries or prepared statements for all database calls, strictly validate and sanitize input parameters on the webserver, and keep detailed database error messages hidden from client responses.

### 2. Information Disclosure (Exposure of Credentials and Account Balances)
* **Category:** Information Disclosure
* **Target Component and Flow:** Database and Webserver (`Query Result` and `HTTP Response`)
* **Risk Level:** High
* **Description:** The Database stores sensitive tables (`User Credentials` and `Account Data`), while `access.log` shows attempts targeting `/portal/balance`, `/portal/admin`, and `/portal/transfer`. A successful `UNION SELECT` query or verbose `500` server error could expose user credentials, account balances, or internal system details.
* **Proposed Mitigation:** Hash passwords using a strong algorithm like bcrypt or Argon2, enforce least-privilege database accounts so the web app only accesses needed tables, return generic error pages for `400` and `500` responses, and enforce HTTPS on all traffic.

### 3. Spoofing (Unauthorized Access and Login Probing)
* **Category:** Spoofing
* **Target Component and Flow:** User Interface (Client) to Webserver (`HTTP REQUEST` and `HTTP Response`) on `/portal/login`, `/portal/balance`, and `/portal/settings`
* **Risk Level:** Medium
* **Description:** Log entries show `401 Unauthorized` requests probing restricted routes (`/portal/balance`, `/portal/settings`) without valid credentials, alongside a `403 Forbidden` response on `POST /portal/login` (a single blocked login attempt, not brute force on its own). An attacker could still attempt credential guessing, session hijacking, or repeated login attempts from the same source IP.
* **Proposed Mitigation:** Require strong authentication and session checks on every protected route, add rate limiting and account lockout or delay controls on `/portal/login`, and monitor logs for repeated failed attempts from the same IP address.

### 4. Elevation of Privilege (Unauthorized Access to Admin Functions)
* **Category:** Elevation of Privilege
* **Target Component and Flow:** User Interface (Client) to Webserver and Database on `/portal/admin` and `/portal/transfer`
* **Risk Level:** Medium
* **Description:** Loan officers and standard users should only access permitted portal actions, while administrative functions and fund transfers carry higher impact. Improper role checks or exploited injection flaws could let a lower-privileged user or unauthenticated caller reach administrative endpoints or trigger unauthorized transfers.
* **Proposed Mitigation:** Enforce server-side role-based access control (RBAC) on every endpoint including `/portal/admin` and `/portal/transfer`, verify user permissions on each request rather than trusting client-side UI state, and require re-authentication or approval checks for high-value actions.

### 5. Denial of Service (Log Flooding, Heavy Queries, or Repeated Login Attempts)
* **Category:** Denial of Service
* **Target Component and Flow:** User Interface (Client) to Webserver (`HTTP REQUEST`) and Webserver to Database (`SQL Queries`)
* **Risk Level:** Low
* **Description:** High volumes of malformed requests, repeated login attempts, heavy `SELECT *` queries, or `500` errors can tie up webserver workers, slow down database reads, or fill up `access.log` storage, making the portal slow or unavailable to loan officers.
* **Proposed Mitigation:** Apply request rate limiting at the webserver or reverse proxy, set query timeouts and pagination on database lookups, and configure log rotation and alerting on spikes in `400`, `401`, `403`, and `500` status codes.
