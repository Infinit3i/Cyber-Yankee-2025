# Phase 2: Internal Reconnaissance & Enumeration
Once inside the firewall OS:
### Identify internal interfaces and routes

```bash
ip addr
ip route
cat /etc/resolv.conf
```

# Look for management configs or logs

```bash
cat /config/config.xml | grep -i 'mgmt\|admin\|ldap\|radius'
```