# Rules with too many alerts

Time of Each Attack



## Rule Sets

### Suricata

Alert: `GPL ATTACK_RESPONSE id check returned root`

- Reason: Shows if user does `whoami` or `id`

Alert: `ET INFO RDP - Response To External Host`

- Reason: Shows RDP Connections

Alert: `ET MALWARE Cobalt Strike Beacon Observed`

- Reason: Shows Cobalt Strike Persistence

Alert: `ET INFO Windows Powershell User-Agent Usage`

- Reason: Finds iex downloads from powershell

### Sigma

Alert: `CobaltStrike Service Installations - System`

- Reason: Finds Ghost Hand's Cobalt strike beacon right away

Alert: `Antivirus Ecploitation Framework Detection`

- Reason: Sees malicious file downloaded from Ghost Hand

### Yara/Strelka

Alert `Sliver_Implant_32bit`

- Reason: Sports Sliver Beacon

### Sysmon
