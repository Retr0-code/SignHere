# SignHere
--
<b>Introduction</b>
<b>CVE-2017-11882</b> - The unique vulnerability identifier of Microsoft Office 2007 Service Pack 3, Microsoft Office 2010 Service Pack 2, Microsoft Office 2013 Service Pack 1, and Microsoft Office 2016 allows an attacker to run code in the context of the current user without properly handling objects in memory, the so-called "Microsoft Office Memory corruption vulnerability".
The implementation includes creating a program for building malicious rtf documents and payloads in VBScript
--
<b>The principle of operation</b>
It is rtf documents that are vulnerable for the reason that they can be "programmed" by knowing special commands-RTF Headers. Thus, a binary (executable) object is created in the body of the document, in fact, it is a Microsoft Equation formula with the code that contains the cmd command. Then you can generate the payload in VBScript and use the command " mshta link to the payload file” to execute the hta file.

<br>

# Installation
The program requires [Python 3](https://www.python.org) for executing.
--
<b>Linux</b>
--
You can use <b>Termux</b>, but execution of program requires <b>root</b>

```sh
git clone https://github.com/Retr0-code/SignHere/
cd SignHere/
chmod +x SignHere.py
./SignHere.py --help
```
<br>

<b>Windows</b>
--
First, you need to download the [archive](https://github.com/Retr0-code/SignHere/archive/main.zip). Then unpack it and open a PowerShell window in this folder and write:
```sh
.\SignHere.py
```
