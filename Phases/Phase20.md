# Phase 20: Teardown
## 🧼 Teardown (DC)

```powershell
sc stop WinDefMon
sc delete WinDefMon
Remove-Item C:\ProgramData\winmon.ps1 -Force
```