# Phase 0: Initial Setup for Kill Chain

Background: Sassy Panda is an Eastonian government affiliated cyber group falling under the Eastonian Cyber Agency (ECA) and comprised of Easton’s most sophisticated capabilities and equipment. Sassy Panda typically focuses on espionage and information gathering and has targeted critical infrastructure in the U.S. including the New England region. Having been active for over 15 years in the computer network exploitation game, the group has emphasized stealth in operations using web shells, living-off-the-land (LOTL) binaries, hands-on-keyboard activities, and stolen credentials.

TTPS:

Enterprise:

Account Discovery: Domain Account, Archive Collected Data: Archive via Utility, Command and Scripting Interpreter: PowerShell, Command and Scripting Interpreter: Windows Command Shell, Compromise Infrastructure: Server, Compromise Infrastructure: Botnet, Credentials from Password Stores, Data from Local System, Data Staged, Local Data Staging, Encrypted Channel: Symmetric Cryptography, Exploit Public-Facing Application, Indicator Removal: File Deletion, Indicator Removal: Clear Network Connection History and Configurations, Lateral Tool Transfer, Log Enumeration, Masquerading: Match Legitimate Name or Location, Masquerading: Masquerade File Type, Obtain Capabilities: Tool, OS Credential Dumping: LSASS Memory, OS Credential Dumping: NTDS, Permission Groups Discovery: Local Groups, Permission Groups Discovery: Domain Groups, Process Discovery, Proxy, Internal Proxy, Query Registry, Remote System Discovery, Server Software Component: Web Shell, Software Discovery, System Information Discovery, System Network Configuration Discovery, System Network Connections Discovery, System Owner/User Discovery, Valid Accounts: Domain Accounts, Virtualization/Sandbox Evasion: System Checks, Windows Management Instrumentation



Target: Palo Alto firewall management interface at XXX.XXX.XXX.XXX
Exploit Used: PoC.py
CVE: CVE-2024-0012 and CVE-2024-9474

*Exploit Setup:*

1. Create a new folder on your attack box as this will be used to stage all of the required files and scripts.
2. Open a text editor on the attack machine (preferably nano).
3. Copy and paste the PoC.py script into the text editor (best case of doing this is utilizing ClickPaste and keep the name the same)
4. If using nano, press ctrl+O and then enter to write out the file, then press ctrl+X to exit the program
5. chmod +x PoC.py
