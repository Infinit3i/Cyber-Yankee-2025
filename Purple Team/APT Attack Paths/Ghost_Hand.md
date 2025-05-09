# Ghost Hand

- `terran` -> `South Africa` -> `IT Admin` -> `Windows DC` -> `Many Endpoints` -> `infostealer`

## Phishing

- RepoSync.msi (Service as SYSTEM)
- Cobalt Strike beacon
- Cobalt Strike port scan
- Dump Credentials - ntds.dit

## DC

- Dump Credentials - ntds.dit
- deploy sliver

## Many Endpoints

- deploy sliver
- drop cryptominer
- run cryptominer
- [x] krazcoin exfil of $
- [x] cobalt strike info of files > csv

---

## Phishing

- RepoSync.msi (Service as SYSTEM)

- Cobalt Strike beacon

```kql
message:"Creating Scriptblock text" and winlog.task: "Execute a Remote Command" and FromBase64String
```

- Cobalt Strike port scan
- Dump Credentials - ntds.dit

## DC

- Dump Credentials - ntds.dit
- deploy sliver

## Many Endpoints

- deploy sliver

#### 
```kql
```

#### 
```kql
```

- drop cryptominer


#### 
```kql
```

#### 
```kql
```

- run cryptominer

#### 
```kql
```

#### 
```kql
```


#### Detect Access to Wallet Files

```kql
DeviceFileEvents
| where FileName endswith "wallet.dat" or FileName has "kraz"
| where ActionType in ("FileDeleted", "FileCreated", "FileModified")
| project Timestamp, DeviceName, FileName, FolderPath, ActionType, InitiatingProcessFileName, InitiatingProcessCommandLine
```

#### Detect Dumping or Sending via CLI or RPC

```kql
DeviceProcessEvents
| where ProcessCommandLine has_any ("dumpprivkey", "sendtoaddress", "backupwallet", "getbalance")
| where ProcessCommandLine has "kraz"
| project Timestamp, DeviceName, ProcessCommandLine, InitiatingProcessFileName, AccountName
```

#### Detect Outbound Exfil to Suspicious IPs or Ports

```kql
DeviceNetworkEvents
| where RemotePort in (8333, 8332, 9050, 9150) // 8333: Bitcoin, 9050/9150: Tor
| where RemoteIPType != "Private"
| where InitiatingProcessCommandLine has_any ("kraz", "wallet", "crypto")
| project Timestamp, DeviceName, RemoteIP, RemotePort, InitiatingProcessFileName, InitiatingProcessCommandLine
```

#### Detect Crypto Clipboard Hijacking or Wallet Replacement

```kql
DeviceEvents
| where ActionType == "ClipboardContentAccessed"
| where AdditionalFields has_any ("Kraz", "wallet", "address", "crypto")
| project Timestamp, DeviceName, ReportId, InitiatingProcessCommandLine
```

#### Detect Process Spawning Related to Wallet Theft

```kql
DeviceProcessEvents
| where ProcessCommandLine has_any ("AppData\\Roaming\\Krazcoin", "wallet.dat", "seed.txt")
| where InitiatingProcessFileName in~ ("powershell.exe", "python.exe", "curl.exe", "cmd.exe")
| project Timestamp, DeviceName, InitiatingProcessFileName, ProcessCommandLine
```

#### [X] Detect KrazCoin Encryption of 

```kql
message:"Creating Scriptblock text" and winlog.task: "Execute a Remote Command" AND powershell.file.script_block_text
```

#### Detect TOR or Proxy Usage Post-Wallet Access

```kql
DeviceNetworkEvents
| where InitiatingProcessCommandLine has_any ("kraz", "wallet")
| join kind=inner (
    DeviceNetworkEvents
    | where RemotePort in (9050, 9150)
    | where RemoteIPType != "Private"
) on DeviceName
| project Timestamp, DeviceName, InitiatingProcessCommandLine, RemoteIP, RemotePort
```

### cobalt strike info of files > csv

#### Detect Creation of Suspicious .csv Files

```kql
DeviceFileEvents
| where FileName endswith ".csv"
| where FolderPath !has "Documents" and FolderPath !has "Downloads" // Exclude normal paths
| where InitiatingProcessFileName in~ ("powershell.exe", "cmd.exe", "rundll32.exe", "regsvr32.exe")
| project Timestamp, DeviceName, FileName, FolderPath, InitiatingProcessFileName, InitiatingProcessCommandLine, ReportId
```

#### Detect Use of Recon Commands Writing to CSV

```kql
DeviceProcessEvents
| where ProcessCommandLine has_any (">", "Out-File")
| where ProcessCommandLine has ".csv"
| where ProcessCommandLine has_any ("tasklist", "net user", "systeminfo", "whoami", "nltest", "dir", "quser")
| where InitiatingProcessFileName in~ ("powershell.exe", "cmd.exe")
| project Timestamp, DeviceName, InitiatingProcessFileName, ProcessCommandLine, FileName
```
