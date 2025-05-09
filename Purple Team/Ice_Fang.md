# Ice Fang

- `terran` -> `Denmark` -> `Kali` -> `windows workstation` -> `DC`

## windows workstation
  
`dropping tools, golden ticket attack, password hash, login with domain admin`

- persistence
    - [X] sticky keys
    - [X] wmi event subscription
    - sysmon config file
- enumerate all user generated files
- stego to encrypt all files into a image
- upload image to c2(twitter)

## DC
    login with elevated creds


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
