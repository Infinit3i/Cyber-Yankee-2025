# Ice Fang

- `terran` -> `Denmark` -> `Kali` -> `windows workstation` -> `DC`

## windows workstation
`dropping tools, golden ticket attack, password hash, login with domain admin`

- persistence
    - [X] sticky keys
    - [X] wmi event subscription
    - [X] sysmon config file
- enumerate all user generated files
- stego to encrypt all files into a image
- upload image to c2(twitter)

## DC
`login with elevated creds`


### Sticky Keys
```kql
DeviceFileEvents
| where FileName == "sethc.exe"
| where ActionType in ("FileRenamed", "FileCreated", "FileModified", "FileDeleted")
| where InitiatingProcessFileName != "TrustedInstaller.exe"
| project Timestamp, DeviceName, FileName, FolderPath, InitiatingProcessFileName, InitiatingProcessCommandLine
```

### WMI

#### Detect Creation of EventFilter, EventConsumer, or FilterToConsumerBinding
```kql
DeviceRegistryEvents
| where RegistryKey contains @"WMI\\Autologger" or RegistryKey contains @"WMI\\Subscription"
| project Timestamp, DeviceName, RegistryKey, RegistryValueName, RegistryValueData, InitiatingProcessCommandLine
```

#### Detect wmic or PowerShell Used to Create Subscription
```kql
DeviceProcessEvents
| where ProcessCommandLine has_any ("EventConsumer", "EventFilter", "FilterToConsumerBinding")
| where InitiatingProcessCommandLine has_any ("wmic", "powershell", "winmgmts:")
| project Timestamp, DeviceName, InitiatingProcessFileName, InitiatingProcessCommandLine, AccountName
```

#### Detect Use of MOFComp.exe (WMI Compilation Tool)
```kql
DeviceProcessEvents
| where FileName == "mofcomp.exe"
| project Timestamp, DeviceName, InitiatingProcessFileName, InitiatingProcessCommandLine, AccountName
```

### Sysmon Config

#### Detect Process Command Line Updating Sysmon Config
```kql
DeviceProcessEvents
| where ProcessCommandLine has "sysmon"
| where ProcessCommandLine has "-c"
| project Timestamp, DeviceName, FileName, ProcessCommandLine, InitiatingProcessFileName, AccountName
```

#### Detect Dropping of XML Files Named sysmon.xml or Similar
```kql
DeviceFileEvents
| where FileName has "sysmon.xml" or FolderPath has "sysmon"
| where ActionType in ("FileCreated", "FileModified", "FileDeleted")
| project Timestamp, DeviceName, FileName, FolderPath, InitiatingProcessCommandLine
```

#### Detect Registry Tampering of Sysmon Service
```kql
DeviceRegistryEvents
| where RegistryKey has "System\\CurrentControlSet\\Services\\Sysmon"
| where RegistryValueName in~ ("ImagePath", "Start", "Type")
| project Timestamp, DeviceName, RegistryKey, RegistryValueName, RegistryValueData, InitiatingProcessCommandLine
```

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
