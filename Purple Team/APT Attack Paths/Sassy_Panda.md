# Sassy Panda

- `terran` -> `Djibouti` -> `Palo Alto Firewall` -> `router` -> `Windows DC` -> `OT`

### IPs TODAY

```
1.33.170.2
1.33.170.6
1.33.170.37
172.20.0.18
172.20.0.26
172.20.0.14

102.214.90.12   attacker 
```

## Palo Alto
`initial exploit`, `whoami`, `pwd`, `cd ~`, `ls`


### Detect Meterpreter

```kql
172.20.0.18 and message:*FromBase64String*
```

### Detect external IPs connecting to routers

**Look for zeek traffic from outside range to routers**
