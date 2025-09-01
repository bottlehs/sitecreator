To block an IP that accesses your server multiple times in a short period using **Nginx** along with **Fail2Ban**, you can set up Fail2Ban to monitor Nginx log files for suspicious activity and block offending IP addresses. Here’s how you can do this:

### 1. **Install Fail2Ban**
If you haven't already installed Fail2Ban, do so with the following commands:

```bash
sudo apt-get update
sudo apt-get install fail2ban
```

### 2. **Configure Nginx to Log Access Attempts**
Ensure Nginx is logging access attempts. Typically, Nginx logs are stored in `/var/log/nginx/access.log` and `/var/log/nginx/error.log`. Make sure your Nginx configuration includes these logs:

- Open your Nginx configuration file:
  ```bash
  sudo nano /etc/nginx/nginx.conf
  ```
- Ensure the `access_log` and `error_log` directives are correctly configured:
  ```nginx
  http {
      log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
      
      access_log /var/log/nginx/access.log main;
      error_log /var/log/nginx/error.log;
      ...
  }
  ```

- Save the file and exit the editor. Restart Nginx to apply changes:
  ```bash
  sudo systemctl restart nginx
  ```

### 3. **Configure Fail2Ban to Monitor Nginx Logs**
Now, configure Fail2Ban to monitor these logs and block IPs that show abusive behavior.

- Create a new configuration file for Nginx within Fail2Ban:
  ```bash
  sudo nano /etc/fail2ban/jail.d/nginx.conf
  ```

- Add the following configuration:

  ```ini
  [nginx-http-auth]
  enabled = true
  filter = nginx-http-auth
  action = iptables[name=HTTP, port=http, protocol=tcp]
  logpath = /var/log/nginx/error.log
  findtime = 300
  bantime = 600
  maxretry = 3

  [nginx-botsearch]
  enabled = true
  filter = nginx-botsearch
  action = iptables-multiport[name=NoBots, port="http,https"]
  logpath = /var/log/nginx/access.log
  bantime = 86400
  findtime = 300
  maxretry = 10
  ```

  **Explanation:**
  - **nginx-http-auth**: Monitors failed authentication attempts in `nginx/error.log`.
  - **nginx-botsearch**: Blocks bots and potential attackers by monitoring `nginx/access.log`.
  - **bantime**: IP is blocked for 10 minutes for `nginx-http-auth` and 1 day for `nginx-botsearch`.
  - **findtime**: If `maxretry` failures happen within 5 minutes, the IP is banned.

- Save the file and exit the editor.

### 4. **Create Custom Filters**
You may need to create custom filters to define what patterns Fail2Ban should look for in the Nginx logs.

- For HTTP auth failures (if not already present):
  ```bash
  sudo nano /etc/fail2ban/filter.d/nginx-http-auth.conf
  ```

  Add the following:
  ```ini
  [Definition]
  failregex = no user/password was provided for basic authentication.*client: <HOST>
              user .* was not found in .*client: <HOST>
  ignoreregex =
  ```

- For bot searches:
  ```bash
  sudo nano /etc/fail2ban/filter.d/nginx-botsearch.conf
  ```

  Add the following:
  ```ini
  [Definition]
  failregex = ^<HOST> .* "(GET|POST).*" (404|444|403|400|500|501|502|503|504) .*$
  ignoreregex =
  ```

  **Explanation**: This looks for specific HTTP response codes (like 404, 403, 500) that are often returned by bots or attackers.

- Save and exit both files.

### 5. **Restart Fail2Ban**
After configuring everything, restart the Fail2Ban service to apply the changes:

```bash
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban
```

### 6. **Verify Fail2Ban is Working**
You can check the status of Fail2Ban and see which jails are active:

```bash
sudo fail2ban-client status
```

To check the status of a specific jail (e.g., `nginx-botsearch`):

```bash
sudo fail2ban-client status nginx-botsearch
```

This setup ensures that any IP that accesses your server multiple times in a short period and matches the defined patterns in the Nginx logs will be automatically blocked by Fail2Ban, effectively protecting your server from brute force attacks, bots, and other malicious activities.