# Ice Fang

- `terran` -> `Denmark` -> `Kali` -|external|> `dns` -> `windows workstation` -> `DC`


### IPs TODAY

```
Terran
terran-kali-1 = 104.55.222.100
terran-kali-2 = 104.55.222.101
terran-kali-3 = 104.55.222.102
terran-kali-4 = 104.55.222.103
terran-kali-5 = 104.55.222.104

GreySpace - IT
bull-it-kali-1 = 172.17.3.69
bull-it-kali-2 = 172.17.3.70
bull-it-kali-3 = 172.17.3.71
bull-it-kali-4 = 172.17.3.72
bull-it-kali-5 = 172.17.3.73

Orange
orng-hr11 = 172.20.7.11
orng-hr2 = 172.20.7.2
orng-hr3 = 172.20.7.3
orng-hr4 = 172.20.7.4
```

## Dns

- bloodhound

## windows workstation

- dropping tools
- golden ticket attack
- password hash
- login with domain admin

- persistence
  - sticky keys
  - wmi event subscription

#### When users log in their credentials are saved to C2

```kql
winlog.task:"Execute a Remote Command"  AND message:*vssadmin list shadows* AND event.dataset:"windows.powershell_operational" 
```

  - sysmon config file
- enumerate all user generated files
- stego to encrypt all files into a image
- upload image to c2(twitter)

## DC

`login with elevated creds`
