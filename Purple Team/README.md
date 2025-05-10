# Rules with too many alerts

Time of Each Attack

Ghost Hand
- Start: `0:00`
- End: `0:00`

Sassy Panda
- Start: `0:00`
- End: `0:00`

Ice Fang
- Start: `2025-05-10 13:50`
- End: `0:00`

---

## Rule Sets

### Snort

Alert: `GPL ATTACK_RESPONSE id check returned root`
- Reason: Shows if user does `whoami` or `id`


### Suricata

Alert: `ET INFO RDP - Response To External Host`
- Reason: Shows RDP Connections

Alert: `ET MALWARE Cobalt Strike Beacon Observed`
- Reason: Shows Cobalt Strike Persistence

### Sigma

Alert: `CobaltStrike Service Installations - System`
- Reason: Finds Ghost Hand's Cobalt strike beacon right away

Alert: `Antivirus Ecploitation Framework Detection`
- Reason: Sees malicious file downloaded from Ghost Hand

### Yara/Strelka

Alert `Sliver_Implant_32bit`
- Reason: Sports Sliver Beacon

### Sysmon
