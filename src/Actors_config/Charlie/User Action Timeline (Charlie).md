### Charlie is a senior penetration tester in the company. He logged into his desktop at 9:00am.

The typical day of a penetration tester varies but may include planning and launching penetration tests, writing reports and giving presentations after a penetration test, and making recommendations for security improvements. The penetration tester work environment is typically a standard office, but many work remotely.

| Time | Action | Action Time (TestCase Setting) | Current Progress | Remarks |
| ----- | ------ | ------------------------------- | ----------------- | ------- |
| 9:00 | Check for new emails in outlook (emailActor.py) | 15 min | Done | Review emails to obtain project details and deadlines from clients. <br><br>Obtained: target URL/IP address, user credentials.
| 9:15 | Open word to record down tasks for the day | 10 min | Done | funcActor.py |
| 9:25 | Ping ip address to check for connectivity. | 2 min | Done | pingActor.py |
| 9:27 | Perform Google search on target | 5 min | Done | webDownload.py |
| 9:32 | Visit whois.com to enumerate on ip address. | 8 min | Done | functionActors.py<br>Visit website with browser via browserActor class. |
| 9:40 | Visit robtex.com/dns-lookup/\<domain> to enumerate on website. | 5 min | Done | functionActors.py<br>Visit website with browser via browserActor class. |
| 9:45 | Open word to record down information gathered | 15 min | Done | funcActor.py |
| 10:00 | Execute Nmap to find target address's open ports and vulnerabilities<br> | 10 min | Done | Can use (python-nmap lib) or nmap pre-installed. <br> `nmap -sC -sV \<ip-address>`
| 10:10 | Perform subdomain web enumeration using Gobuster | 5 min | Done | Execute: <br>`gobuster -u \<target-url> -w \`<wordlist> |
| 10:15 | Perform Google search on port weaknesses and exploits | 15 min | Done | webDownload.py |
| 10:30 | Zoom meeting to discuss with clients and colleagues about information gathered, and exploitation methods to be executed. | 90 min | Done | zoomActor.py | 
| 12:00 | Lunch | 60 min | Done | - |
| 13:00 | Run sqlmap on target | 20 min | Done | funcActor.py or os.system()<br><br>`sqlmap -u "target address url" --cookie="" --schema --bath`<br><br>`sqlmap -u "target address url" --cookie="" --columns -T users --bath` |
| 13:20 | Visit https://gchq.github.io/CyberChef/ to crack DB hashes | 5 min | Done | funcActor.py <br>Create webActor object |
| 13:25 | SSH to open port using cracked credentials from DB | 5 min | Done | SSHconnector<br>`ssh \<username>@ip`|
| 13:30 | Run "sudo -l" to check for sudo privileges | 5 min | Done | os.system() |
| 13:35 | Visit https://book.hacktricks.xyz/ for privilege escalation | 10 min | Done | funcActor.py <br>Create webActor object |
| 13:45 | Visit https://gtfobins.github.io/ for privilege escalation | 15 min | Done | funcActor.py <br>Create webActor object |
| 14:00 | Watch YouTube video and take a break | 15 min | Done | funcActor.py<br> Create webActor object |
| 14:15 | Download WinPEAS from https://github.com/carlospolop/PEASS-ng/releases/download/20230212/winPEASx64.exe | 10 min | Done | webDownload.py |
| 14:25 | Transfer WinPEAS file over | 5 min | Done | `os.system("python -m SimpleHTTPServer 80")`<br><br>Note: On target run wget |
| 14:30 | Visit exploit-db.com to download exploit | 5 min | Done | webDownload.py |
| 14:35 | Run searchsploit for suitable exploits | 5 min | Done | `os.system("searchsploit ___")` |
| 14:40 | Run msfvenom | 10 min | Done | `os.system("msfvenom")` |
| 14:50 | Open word to document findings | 30 min | Done | funcActor.py |
| 15:20 | Design Powerpoint slides for presentation | 60 min | Done | funcActor.py -> msPPTedit |
| 16:20 | Zoom meeting to discuss security findings to colleagues and clients | 100 min | Done | zoomActor.py |
| 18:00 | End work | - | Done | Nil | 

<br>  

More tools to consider implementing:  
<br>
john the ripper  
netcat  
hydra  
crunch  
postman  
burpsuite  
searchsploit  