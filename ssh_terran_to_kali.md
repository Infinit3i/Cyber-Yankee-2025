# Terran

```bash
ssh -N -L 4444:104.55.222.106:22 -R 5555:localhost:22 -D 1080 kaliuser@102.214.90.13
```


## Terran (102.214.90.13)**:

```bash
ssh -p 5555 localhost   # connect back to target's SSH
```

## Djibouti (104.55.222.106)**:

```bash
ssh -p 4444 localhost   # tunnel to Kali's SSH
```
