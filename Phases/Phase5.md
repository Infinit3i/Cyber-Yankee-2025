# Phase 5: Target Discovery Inside Orange Space

Assuming pivot success to internal hosts:

## Scan internal subnets for DC or LDAP

```bash
nmap -p 389,445,88,135,139,389,636,3268,3269 -sV -Pn 172.20.0.0/16
```

- Look for the Domain Controller (likely in orange-servers or orange-users).
