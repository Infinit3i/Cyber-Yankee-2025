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
- krazcoin exfil of $
- cobalt strike info of files > csv

---

## Phishing

- RepoSync.msi (Service as SYSTEM)

#### [X] Cobalt Strike beacon

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




#### Detect Access to Wallet Files

#### Detect Dumping or Sending via CLI or RPC



#### Detect Outbound Exfil to Suspicious IPs or Ports



#### Detect Crypto Clipboard Hijacking or Wallet Replacement



#### Detect Process Spawning Related to Wallet Theft


#### [X] Detect KrazCoin Encryption of 

```kql
message:"Creating Scriptblock text" and winlog.task: "Execute a Remote Command" AND powershell.file.script_block_text
```

#### Detect TOR or Proxy Usage Post-Wallet Access

### cobalt strike info of files > csv

#### Detect Creation of Suspicious .csv Files

#### Detect Use of Recon Commands Writing to CSV

