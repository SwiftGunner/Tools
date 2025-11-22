# Port & Service Command Reference Tool - Feature Overview

## 📊 What You Get

### Target Configuration (NEW!)
```
✓ Set Target IP Once
✓ Auto-Replace <target> Placeholder
✓ Auto-Replace <domain> Placeholder
✓ Auto-Replace <user> Placeholder
✓ Toggle On/Off as Needed
✓ See Original & Final Command
```

### Pre-Loaded Database
```
✓ 20+ Common Ports (21-8080)
✓ 100+ Security Commands
✓ 4 Command Categories
✓ Professional Descriptions
✓ Instant Access
```

### Command Categories
```
[Reconnaissance]    - Initial information gathering
[Enumeration]       - Detailed service enumeration
[Exploitation]      - Active exploitation commands
[Post-Exploitation] - Post-compromise activities
```

### Included Services & Tools

**File Transfer & Remote Access**
- FTP (21) - ftp, nmap scripts, hydra
- SSH (22) - ssh, ssh-keyscan, port forwarding
- Telnet (23) - telnet, brute force
- RDP (3389) - xfreerdp, rdesktop, hydra

**Web Services**
- HTTP (80) - nikto, gobuster, ffuf, sqlmap
- HTTPS (443) - sslscan, testssl.sh, web scanners
- HTTP-Proxy (8080) - alternative HTTP testing

**Email Services**
- SMTP (25) - smtp-user-enum, swaks
- POP3 (110) - connection, enumeration
- IMAP (143) - capabilities, authentication

**Directory & Authentication**
- LDAP (389) - ldapsearch, enumeration
- Kerberos (88) - ASREPRoast, Kerberoasting
- DNS (53) - dig, zone transfers, dnsenum

**File Sharing**
- SMB (445) - smbclient, enum4linux, crackmapexec, EternalBlue
- NetBIOS (139) - nbtscan, nmblookup
- NFS (2049) - showmount, mount

**Databases**
- MySQL (3306) - mysql client, brute force
- MSSQL (1433) - mssqlclient.py, sqsh
- PostgreSQL (5432) - psql
- Oracle (1521) - tnscmd, odat
- Redis (6379) - redis-cli

**Network & Monitoring**
- SNMP (161) - snmpwalk, onesixtyone
- VNC (5900) - vncviewer, password brute force

---

## 🎨 User Interface

### Layout
```
┌─────────────────────────────────────────────────────────┐
│     ⚡ PORT & SERVICE COMMAND REFERENCE ⚡              │
├─────────────────────────────────────────────────────────┤
│ TARGET CONFIGURATION                                    │
│ Target IP: [10.10.10.50] Domain: [example.com]         │
│ Username: [admin] ☑ Auto-replace placeholders          │
├──────────────────────┬──────────────────────────────────┤
│  [Search: ______]    │  Category: ○All ●Recon ○Enum    │
│                      │  ○Exploit ○Post-Exploit         │
│  PORT | SERVICE      │                                  │
│  ──────────────────  │  ════════════════════════════    │
│  21   | FTP         │  Port 80 - HTTP                  │
│  22   | SSH         │  ════════════════════════════    │
│  80   | HTTP  ◄─────┤                                  │
│  443  | HTTPS       │  [Reconnaissance]                │
│  445  | SMB         │  ────────────────────────────    │
│                      │                                  │
│  [Add] [Edit] [Del]  │  nmap -sV -p 80 10.10.10.50     │
│                      │  [📋 Copy]                       │
│                      │  Description: Version detection  │
│                      │                                  │
│                      │  nikto -h http://10.10.10.50    │
│                      │  [📋 Copy]                       │
│                      │  Description: Web vuln scanner   │
│                      │                                  │
│                      │  [Add Cmd] [Edit] [Delete]       │
└──────────────────────┴──────────────────────────────────┘
│   SwiftGunner © 2024 | Streamline Your Enumeration     │
└─────────────────────────────────────────────────────────┘
```

### Color Scheme
```
Background:     #1a1a1a (Dark Black)
Text:           #cccccc (Light Gray)
Accent:         #00cc00 (Green)
Highlights:     #00ff00 (Bright Green)
Secondary:      #2d2d2d (Dark Gray)
Selected:       #003300 (Dark Green)
```

---

## ⚡ Quick Actions

### Search & Filter
```bash
Type in search box:
→ "22"        # Shows SSH
→ "http"      # Shows HTTP/HTTPS services
→ "sql"       # Shows database services
→ "transfer"  # Shows file transfer services
```

### Category Filtering
```
Click radio buttons to filter commands:
→ All                  # Shows everything
→ Reconnaissance       # Initial scans only
→ Enumeration         # Detailed enumeration
→ Exploitation        # Active attacks
→ Post-Exploitation   # Post-compromise
```

### Copy Commands
```
Click [📋 Copy] button next to any command
→ Instantly copies to clipboard
→ Paste directly into terminal
→ No manual typing needed
```

---

## 🔧 Customization Examples

### Add Custom Port
```
Port: 9200
Service: Elasticsearch
Description: Elasticsearch REST API

Result: New searchable entry in database
```

### Add Custom Command
```
Category: Enumeration
Command: curl -XGET http://<target>:9200/_cluster/health?pretty
Description: Check Elasticsearch cluster health

Result: Available in commands for port 9200
```

---

## 📈 Workflow Integration

### Enhanced Recon Workflow (with Target Config)
```
1. Run nmap scan → Identify open ports
2. Open Port & Service Tool
3. Enter target IP: 192.168.1.50 (set once!)
4. Search for each open port
5. Copy relevant commands (auto-filled with IP)
6. Paste & execute - NO manual editing
7. Add findings to notes
```

### Without Target Config (Old Way)
```
Copy:  nmap -sV -p 80 <target>
Paste: nmap -sV -p 80 <target>
Edit:  nmap -sV -p 80 192.168.1.50  ← Manual typing
Run:   Command ready
```

### With Target Config (New Way)
```
Set:   Target IP = 192.168.1.50
Copy:  nmap -sV -p 80 <target>
Paste: nmap -sV -p 80 192.168.1.50  ← Auto-filled!
Run:   Command ready immediately
```

### Typical Recon Workflow
```
1. Run nmap scan
2. Identify open ports
3. Open Port & Service Tool
4. Search for each port
5. Copy relevant commands
6. Execute enumeration
7. Add findings to notes
```

### Custom Toolset Building
```
1. Discover new tool/technique
2. Open relevant port
3. Add custom command
4. Available for future engagements
5. Build your personal arsenal
```

---

## 💾 Data Persistence

### Automatic Database
```
File: port_service_commands.db
Type: SQLite
Location: Same directory as script

What's Stored:
→ All default ports/services
→ All default commands
→ Your custom additions
→ Your edits/modifications
```

### Backup Recommendation
```bash
# Before major changes
cp port_service_commands.db port_service_commands.backup

# Restore if needed
cp port_service_commands.backup port_service_commands.db
```

---

## 🎯 Use Case Examples

### Web Application Testing
```
Search: "80"
Filter: Enumeration
Copy: gobuster, nikto, whatweb, ffuf commands
Deploy in testing environment
```

### Active Directory Assessment
```
Search: "88", "389", "445"
Filter: All categories
Copy: Kerberos, LDAP, SMB enumeration
Execute domain reconnaissance
```

### Database Security Audit
```
Search: "1433", "3306", "5432"
Filter: Exploitation
Copy: Database connection commands
Test authentication and permissions
```

### Network Infrastructure
```
Search: "161", "53"
Filter: Enumeration
Copy: SNMP, DNS commands
Map network devices and services
```

---

## ⚙️ Technical Specifications

```
Language:         Python 3.6+
GUI Framework:    tkinter
Database:         SQLite3
Dependencies:     pyperclip
Platform:         Cross-platform (Windows, Linux, Mac)
Database Size:    ~50KB (grows with additions)
Memory Usage:     ~20-30MB
Startup Time:     <1 second
```

---

## 🚀 Performance Features

```
✓ Instant Search (real-time filtering)
✓ Fast Category Switching
✓ Efficient Database Queries
✓ Minimal Memory Footprint
✓ No Network Dependencies
✓ Offline Operation
✓ Quick Clipboard Access
```

---

## 📚 Learning Resource

**Perfect for:**
- Memorizing common enumeration commands
- Learning service-specific techniques
- Building command muscle memory
- Quick reference during engagements
- Training and certification prep (OSCP, CEH, etc.)

---

## 🔒 Ethical Use Reminder

```
⚠️  AUTHORIZED TESTING ONLY  ⚠️

This tool provides powerful commands that can:
- Scan networks
- Enumerate services
- Attempt authentication
- Exploit vulnerabilities

ALWAYS:
✓ Obtain written authorization
✓ Define clear scope
✓ Follow rules of engagement
✓ Document all activities
✓ Report findings responsibly

NEVER:
✗ Test without permission
✗ Exceed authorized scope
✗ Cause system damage
✗ Access unauthorized data
```

---

**Built by SwiftGunner for the security community**

**Efficiency. Organization. Professionalism.** 🎯
