# Ghost Hand

- `terran` -> `South Africa` -> `IT Admin` -> `Windows DC` -> `Many Endpoints` -> `infostealer`

## IPs TODAY

```
```

## Phishing

- RepoSync.msi (Service as SYSTEM)

**Look for reg key HKLM\SOFTWARE\WOW6432Node\wmipmon**

- Cobalt Strike beacon

```kql
message:"Creating Scriptblock text" and winlog.task: "Execute a Remote Command" and FromBase64String
```

**Look for files dropped in C:\Windows\Temp** - app_log, Southerland

- Cobalt Strike port scan
- drop cryptominer
- run cryptominer
- Dump local Credentials

## DC

- Dump Credentials - ntds.dit
- deploy sliver

**Look for powershell -hidden Invoke-WebRequest -Uri**

## Many Endpoints

- deploy sliver
- krazcoin exfil of $

```kql
message:"Creating Scriptblock text" and winlog.task: "Execute a Remote Command" AND powershell.file.script_block_text
```
- cobalt strike info of files > csv
