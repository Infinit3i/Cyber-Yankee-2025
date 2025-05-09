# Ghost Hand

- `terran` -> `South Africa` -> `IT Admin` -> `Windows DC` -> `Many Endpoints` -> `infostealer`

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
- drop cryptominer
- run cryptominer
- krazcoin exfil of $

```kql
message:"Creating Scriptblock text" and winlog.task: "Execute a Remote Command" AND powershell.file.script_block_text
```
- cobalt strike info of files > csv
