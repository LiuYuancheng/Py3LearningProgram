import win32com.shell.shell as shell
commands = 'echo hi'
commands = 'Set-MpPreference -DisableRealtimeMonitoring $false'
commands = 'netsh advfirewall set privateprofile state off'
reslt = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
print(reslt)

#import subprocess

#subprocess.call('C:\Windows\System32\powershell.exe Set-MpPreference -DisableRealtimeMonitoring $true', shell=True)