# Phase 1: Exploit PanOS

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

Post-Exploitation:
● Upgrade shell if necessary.
● Identify internal routes/interfaces.
● Upload a simple proxy (e.g., socat or chisel) if needed for tunneling
