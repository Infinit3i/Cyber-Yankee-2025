# Ghost Hand

- `terran` -> `South Africa` -> `IT Admin` -> `Windows DC` -> `Many Endpoints` -> `infostealer`

## IPs TODAY

```
safrica-kali-4 - 101.44.253.14
terran-cobalt7 - 104.55.222.146


repotools.net - 104.53.222.99 - FOSS Server
watchdawgz.com - 104.53.222.47 - crypto-miner
sysperform.org - 104.53.222.115 - trojan

172.20.8.104 - mildred.sexton
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
