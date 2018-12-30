Dim hostname
hostname = "<VPN GATEWAY NAME>"


Set WshShell = WScript.CreateObject("WScript.Shell")

'Check if you are connecrted to Internet by using ping'

Ping = WshShell.Run("ping -n 1 " & hostname, 0, True)
if (Ping) then

	'For a sucessfull ping open the VPN software'
	Set WshShell = WScript.CreateObject("WScript.Shell")

	WshShell.Run """%PROGRAMFILES(x86)%\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe"""

	WScript.Sleep 300

	WshShell.AppActivate "Cisco AnyConnect Secure Mobility Client"

	WshShell.SendKeys "{TAB}"
	WshShell.SendKeys "{TAB}"
	WshShell.SendKeys "{ENTER}"

	WScript.Sleep 5000

	WshShell.SendKeys "<VPM PASSWORD>" 
	WshShell.SendKeys "{ENTER}"
	WScript.Sleep 5000

	else

	WScript.Echo "You are connected to VPN"

End if

'Open up application after you are connected to ping in this case IRC'

Dim exeName 
Dim statusCode
Dim hexFound 
hexFound= False
exeName = "%windir%/hex"
Dim service, Process
Set service = GetObject ("winmgmts:")
For each Process in Service.InstancesOf ("Win32_Process")
	If LCase(Process.Name) = "hexchat.exe" Then
		hexFound = True 
	End If
Next
if not hexFound Then
statusCode = WshShell.Run (exeName, 1, true)
End if