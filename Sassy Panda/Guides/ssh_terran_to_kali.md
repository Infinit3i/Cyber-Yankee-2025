## SSH Proxy Chain

### Terran (104.55.222.106)

```bash
ssh -N -R 5555:localhost:22 -L 4444:102.214.90.13:22 -D 1080 kali@102.214.90.13
```

### Djibouti (102.214.90.13)

```bash
ssh -p 5555 localhost   # connect back to target's SSH
```

### Terran (104.55.222.106)

```bash
ssh -p 4444 localhost   # tunnel to Kali's SSH
```
