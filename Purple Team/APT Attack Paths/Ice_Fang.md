# Ice Fang

- `terran` -> `Denmark` -> `Kali` -|external|> `dns` -> `windows workstation` -> `DC`

## Dns

- [x] bloodhound

## windows workstation

- [X] dropping tools
- [X] golden ticket attack
- [X] password hash
- [X] login with domain admin

- persistence
  - [X] sticky keys
  - [X] wmi event subscription
  - [X] sysmon config file
- [X] enumerate all user generated files
- [X] stego to encrypt all files into a image
- [x] upload image to c2(twitter)

## DC

`login with elevated creds`

----
----

### BloodHound

### Excessive LDAP Enumeration



### BloodHound/SharpHound triggers burst lookup

### Spike in lookups for AD computers/users

### dropping tools

#### File Creation on Endpoint

```kql
event.module: "windows" and event.action: "file_created"
and file.path: ("C:\\Users\\*", "C:\\ProgramData\\*", "C:\\Temp\\*", "C:\\Windows\\Tasks\\*", "C:\\Windows\\System32\\*")
and file.extension: ("exe", "dll", "ps1", "bat", "vbs")
```

#### Network-based file downloads

```kql
event.module: "suricata"
and fileinfo.filename: ("*.exe", "*.dll", "*.ps1", "*.bat")
```

#### detect SMB/NetBIOS Downloads

```kql
event.dataset: "zeek.smb_files"
and file.name: ("*.exe", "*.dll", "*.bat", "*.ps1")
```

### golden ticket attack

#### Process Execution of Known Mimikatz Names or Paths

```kql
event.module: "windows" and event.action: "process_start"
and process.name: ("mimikatz.exe", "mimidrv.sys", "mimi.exe", "pwdump.exe")
```

#### Privilege Use (SeDebugPrivilege, SeTcbPrivilege)

```kql
event.code: ("4673", "4674")
and winlog.event_data.PrivilegeList: ("SeDebugPrivilege", "SeTcbPrivilege")
```

```kql
```

### Login With Domain Admin

#### Multiple Kerberos Tickets for Same Account Across Hosts

#### Detect ticketer.py

```kql
event.code: "4624"
and winlog.event_data.AuthenticationPackageName: "Kerberos"
and winlog.event_data.LogonType: "3"
and (winlog.event_data.WorkstationName: "-" or winlog.event_data.WorkstationName: "")
and (winlog.event_data.AccountDomain: "NT AUTHORITY" or winlog.event_data.AccountName: "*admin*")
```

### Sticky Keys



### WMI

#### Detect Creation of EventFilter, EventConsumer, or FilterToConsumerBinding


#### Detect wmic or PowerShell Used to Create Subscription



#### Detect Use of MOFComp.exe (WMI Compilation Tool)


### Sysmon Config

#### Detect Process Command Line Updating Sysmon Config



#### Detect Dropping of XML Files Named sysmon.xml or Similar



#### Detect Registry Tampering of Sysmon Service


#### Enumeration of User-Generated Files via Command Line

```kql
process where event.type == "start" and (
  (process.name : ("cmd.exe", "powershell.exe", "pwsh.exe")) and
  (process.command_line : (
    "*\\Users\\*\\Documents\\*", 
    "*\\Users\\*\\Downloads\\*",
    "*\\Users\\*\\Desktop\\*",
    "*\\Users\\*\\Pictures\\*",
    "*\\Users\\*\\Videos\\*",
    "*\\Users\\*\\OneDrive\\*"
  )) and
  process.command_line : ("*dir*", "*tree*", "*Get-ChildItem*", "*ls*", "*cat*", "*type*")
)
```

#### File Access Events

```kql
file where file.path : (
  "C:\\Users\\*\\Documents\\*", 
  "C:\\Users\\*\\Downloads\\*", 
  "C:\\Users\\*\\Desktop\\*"
) and event.action == "open"
and process.name : ("cmd.exe", "powershell.exe", "python.exe", "7z.exe", "rar.exe")
```

### Stego

### Detect Large Writes to Image files

```kql
file where file.extension in ("jpg", "png", "bmp")
and event.action == "file_write"
and file.size > 5000000
and process.name : ("python.exe", "custom_stego.exe", "powershell.exe")
```

#### Detect Encryption Activity

```
process where process.name : ("python.exe", "custom_stego.exe")
and process.command_line has_any ("AES", "Fernet", "Crypto.Cipher", "Rijndael")
```
