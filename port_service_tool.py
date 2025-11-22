#!/usr/bin/env python3
"""
Port & Service Command Reference Tool
by SwiftGunner

A comprehensive GUI application for quick access to enumeration and exploitation
commands organized by port, service, and category.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import pyperclip
from datetime import datetime

class PortServiceTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Port & Service Command Reference - SwiftGunner")
        self.root.geometry("1400x950")
        
        # Dark theme colors
        self.bg_color = "#1a1a1a"
        self.fg_color = "#00ff00"
        self.secondary_bg = "#2d2d2d"
        self.accent_color = "#00cc00"
        self.text_color = "#cccccc"
        self.highlight_color = "#003300"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize database
        self.init_database()
        
        # Setup GUI
        self.setup_gui()
        
        # Load initial data
        self.refresh_port_list()
    
    def init_database(self):
        """Initialize SQLite database with schema and default data"""
        self.conn = sqlite3.connect('port_service_commands.db')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                port_number INTEGER NOT NULL,
                service_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(port_number, service_name)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                port_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                command TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (port_id) REFERENCES ports (id) ON DELETE CASCADE
            )
        ''')
        
        # Check if we need to populate default data
        self.cursor.execute('SELECT COUNT(*) FROM ports')
        if self.cursor.fetchone()[0] == 0:
            self.populate_default_data()
        
        self.conn.commit()
    
    def populate_default_data(self):
        """Populate database with common ports, services, and commands"""
        
        default_data = [
            # FTP - Port 21
            {
                'port': 21,
                'service': 'FTP',
                'description': 'File Transfer Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 21 <target>', 'Version detection on FTP service'),
                    ('Enumeration', 'ftp <target>', 'Connect to FTP server'),
                    ('Enumeration', 'nmap --script ftp-anon -p 21 <target>', 'Check for anonymous FTP login'),
                    ('Enumeration', 'nmap --script ftp-* -p 21 <target>', 'Run all FTP NSE scripts'),
                    ('Exploitation', 'hydra -L users.txt -P passwords.txt ftp://<target>', 'Brute force FTP credentials'),
                    ('Exploitation', 'msfconsole -x "use auxiliary/scanner/ftp/ftp_login; set RHOSTS <target>; run"', 'Metasploit FTP login scanner'),
                ]
            },
            # SSH - Port 22
            {
                'port': 22,
                'service': 'SSH',
                'description': 'Secure Shell',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 22 <target>', 'Version detection on SSH service'),
                    ('Enumeration', 'ssh-keyscan -t rsa <target>', 'Retrieve SSH public keys'),
                    ('Enumeration', 'nmap --script ssh-auth-methods -p 22 <target>', 'Enumerate SSH authentication methods'),
                    ('Enumeration', 'nmap --script ssh2-enum-algos -p 22 <target>', 'Enumerate SSH algorithms'),
                    ('Exploitation', 'hydra -L users.txt -P passwords.txt ssh://<target>', 'Brute force SSH credentials'),
                    ('Exploitation', 'ssh <user>@<target>', 'Connect to SSH server'),
                    ('Post-Exploitation', 'ssh -L 8080:localhost:80 <user>@<target>', 'SSH local port forwarding'),
                    ('Post-Exploitation', 'ssh -R 8080:localhost:80 <user>@<target>', 'SSH remote port forwarding'),
                ]
            },
            # Telnet - Port 23
            {
                'port': 23,
                'service': 'Telnet',
                'description': 'Telnet Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 23 <target>', 'Version detection on Telnet service'),
                    ('Enumeration', 'telnet <target> 23', 'Connect to Telnet server'),
                    ('Exploitation', 'hydra -L users.txt -P passwords.txt telnet://<target>', 'Brute force Telnet credentials'),
                    ('Exploitation', 'msfconsole -x "use auxiliary/scanner/telnet/telnet_login; set RHOSTS <target>; run"', 'Metasploit Telnet login scanner'),
                ]
            },
            # SMTP - Port 25
            {
                'port': 25,
                'service': 'SMTP',
                'description': 'Simple Mail Transfer Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 25 <target>', 'Version detection on SMTP service'),
                    ('Enumeration', 'nmap --script smtp-enum-users -p 25 <target>', 'Enumerate SMTP users'),
                    ('Enumeration', 'nmap --script smtp-commands -p 25 <target>', 'Enumerate SMTP commands'),
                    ('Enumeration', 'smtp-user-enum -M VRFY -U users.txt -t <target>', 'SMTP user enumeration via VRFY'),
                    ('Enumeration', 'nc <target> 25', 'Manual SMTP banner grabbing'),
                    ('Exploitation', 'swaks --to <email> --from <email> --server <target>', 'Test SMTP relay'),
                ]
            },
            # DNS - Port 53
            {
                'port': 53,
                'service': 'DNS',
                'description': 'Domain Name System',
                'commands': [
                    ('Reconnaissance', 'nmap -sU -sV -p 53 <target>', 'Version detection on DNS service (UDP)'),
                    ('Enumeration', 'dig @<target> <domain> ANY', 'Query all DNS records'),
                    ('Enumeration', 'dig @<target> <domain> AXFR', 'Attempt DNS zone transfer'),
                    ('Enumeration', 'nmap --script dns-zone-transfer -p 53 <target>', 'NSE DNS zone transfer'),
                    ('Enumeration', 'dnsenum <domain>', 'DNS enumeration tool'),
                    ('Enumeration', 'fierce --domain <domain>', 'DNS reconnaissance tool'),
                    ('Enumeration', 'host -l <domain> <target>', 'Zone transfer attempt with host'),
                ]
            },
            # HTTP - Port 80
            {
                'port': 80,
                'service': 'HTTP',
                'description': 'Hypertext Transfer Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 80 <target>', 'Version detection on HTTP service'),
                    ('Enumeration', 'nikto -h http://<target>', 'Web server vulnerability scanner'),
                    ('Enumeration', 'gobuster dir -u http://<target> -w /usr/share/wordlists/dirb/common.txt', 'Directory brute forcing'),
                    ('Enumeration', 'ffuf -u http://<target>/FUZZ -w /usr/share/wordlists/dirb/common.txt', 'Fast web fuzzer'),
                    ('Enumeration', 'whatweb http://<target>', 'Web technology fingerprinting'),
                    ('Enumeration', 'nmap --script http-enum -p 80 <target>', 'HTTP enumeration script'),
                    ('Enumeration', 'curl -I http://<target>', 'Grab HTTP headers'),
                    ('Exploitation', 'sqlmap -u "http://<target>/page?id=1" --batch', 'SQL injection testing'),
                    ('Exploitation', 'wpscan --url http://<target> --enumerate u,p', 'WordPress security scanner'),
                ]
            },
            # Kerberos - Port 88
            {
                'port': 88,
                'service': 'Kerberos',
                'description': 'Kerberos Authentication',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 88 <target>', 'Version detection on Kerberos service'),
                    ('Enumeration', 'nmap -p 88 --script krb5-enum-users --script-args krb5-enum-users.realm="<domain>" <target>', 'Enumerate Kerberos users'),
                    ('Exploitation', 'GetNPUsers.py <domain>/ -usersfile users.txt -dc-ip <target>', 'ASREPRoast attack'),
                    ('Exploitation', 'GetUserSPNs.py <domain>/<user>:<password> -dc-ip <target> -request', 'Kerberoasting attack'),
                ]
            },
            # POP3 - Port 110
            {
                'port': 110,
                'service': 'POP3',
                'description': 'Post Office Protocol v3',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 110 <target>', 'Version detection on POP3 service'),
                    ('Enumeration', 'nc <target> 110', 'Connect to POP3 server'),
                    ('Enumeration', 'nmap --script pop3-capabilities -p 110 <target>', 'Enumerate POP3 capabilities'),
                    ('Exploitation', 'hydra -L users.txt -P passwords.txt pop3://<target>', 'Brute force POP3 credentials'),
                ]
            },
            # NetBIOS - Port 139
            {
                'port': 139,
                'service': 'NetBIOS',
                'description': 'NetBIOS Session Service',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 139 <target>', 'Version detection on NetBIOS service'),
                    ('Enumeration', 'nbtscan <target>', 'NetBIOS name scanner'),
                    ('Enumeration', 'enum4linux -a <target>', 'SMB/NetBIOS enumeration'),
                    ('Enumeration', 'nmblookup -A <target>', 'NetBIOS name query'),
                    ('Enumeration', 'smbclient -L //<target> -N', 'List SMB shares'),
                ]
            },
            # IMAP - Port 143
            {
                'port': 143,
                'service': 'IMAP',
                'description': 'Internet Message Access Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 143 <target>', 'Version detection on IMAP service'),
                    ('Enumeration', 'nc <target> 143', 'Connect to IMAP server'),
                    ('Enumeration', 'nmap --script imap-capabilities -p 143 <target>', 'Enumerate IMAP capabilities'),
                    ('Exploitation', 'hydra -L users.txt -P passwords.txt imap://<target>', 'Brute force IMAP credentials'),
                ]
            },
            # SNMP - Port 161
            {
                'port': 161,
                'service': 'SNMP',
                'description': 'Simple Network Management Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sU -sV -p 161 <target>', 'Version detection on SNMP service (UDP)'),
                    ('Enumeration', 'snmpwalk -v2c -c public <target>', 'SNMP walk with public community string'),
                    ('Enumeration', 'snmp-check <target>', 'SNMP enumeration tool'),
                    ('Enumeration', 'onesixtyone -c community.txt <target>', 'SNMP community string brute force'),
                    ('Enumeration', 'nmap --script snmp-* -sU -p 161 <target>', 'Run all SNMP NSE scripts'),
                ]
            },
            # LDAP - Port 389
            {
                'port': 389,
                'service': 'LDAP',
                'description': 'Lightweight Directory Access Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 389 <target>', 'Version detection on LDAP service'),
                    ('Enumeration', 'ldapsearch -x -h <target> -s base', 'LDAP anonymous bind'),
                    ('Enumeration', 'ldapsearch -x -h <target> -b "dc=domain,dc=com"', 'LDAP search with base DN'),
                    ('Enumeration', 'nmap --script ldap-search -p 389 <target>', 'LDAP search NSE script'),
                    ('Enumeration', 'nmap --script ldap-rootdse -p 389 <target>', 'LDAP root DSE enumeration'),
                ]
            },
            # HTTPS - Port 443
            {
                'port': 443,
                'service': 'HTTPS',
                'description': 'HTTP over TLS/SSL',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 443 <target>', 'Version detection on HTTPS service'),
                    ('Enumeration', 'nikto -h https://<target>', 'Web server vulnerability scanner (HTTPS)'),
                    ('Enumeration', 'sslscan <target>:443', 'SSL/TLS cipher suite scanner'),
                    ('Enumeration', 'nmap --script ssl-enum-ciphers -p 443 <target>', 'Enumerate SSL/TLS ciphers'),
                    ('Enumeration', 'testssl.sh <target>:443', 'Comprehensive SSL/TLS testing'),
                    ('Enumeration', 'gobuster dir -u https://<target> -w /usr/share/wordlists/dirb/common.txt', 'Directory brute forcing (HTTPS)'),
                    ('Exploitation', 'sqlmap -u "https://<target>/page?id=1" --batch', 'SQL injection testing (HTTPS)'),
                ]
            },
            # SMB - Port 445
            {
                'port': 445,
                'service': 'SMB',
                'description': 'Server Message Block',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 445 <target>', 'Version detection on SMB service'),
                    ('Enumeration', 'smbclient -L //<target> -N', 'List SMB shares (no password)'),
                    ('Enumeration', 'smbmap -H <target>', 'SMB share enumeration'),
                    ('Enumeration', 'enum4linux -a <target>', 'Comprehensive SMB enumeration'),
                    ('Enumeration', 'crackmapexec smb <target> --shares', 'SMB share enumeration with CME'),
                    ('Enumeration', 'nmap --script smb-enum-* -p 445 <target>', 'Run all SMB enumeration scripts'),
                    ('Enumeration', 'nmap --script smb-vuln-* -p 445 <target>', 'Check for SMB vulnerabilities'),
                    ('Exploitation', 'smbclient //<target>/<share> -U <user>', 'Connect to SMB share'),
                    ('Exploitation', 'crackmapexec smb <target> -u <user> -p <password>', 'SMB authentication testing'),
                    ('Exploitation', 'msfconsole -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS <target>; run"', 'EternalBlue exploitation'),
                ]
            },
            # MSSQL - Port 1433
            {
                'port': 1433,
                'service': 'MSSQL',
                'description': 'Microsoft SQL Server',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 1433 <target>', 'Version detection on MSSQL service'),
                    ('Enumeration', 'nmap --script ms-sql-info -p 1433 <target>', 'MSSQL information gathering'),
                    ('Enumeration', 'nmap --script ms-sql-empty-password -p 1433 <target>', 'Check for empty SA password'),
                    ('Exploitation', 'mssqlclient.py <user>:<password>@<target>', 'Connect to MSSQL server (Impacket)'),
                    ('Exploitation', 'sqsh -S <target> -U <user> -P <password>', 'Interactive MSSQL client'),
                    ('Post-Exploitation', 'mssqlclient.py <user>:<password>@<target> -windows-auth', 'MSSQL with Windows authentication'),
                ]
            },
            # Oracle - Port 1521
            {
                'port': 1521,
                'service': 'Oracle',
                'description': 'Oracle Database',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 1521 <target>', 'Version detection on Oracle service'),
                    ('Enumeration', 'tnscmd10g version -h <target>', 'Oracle TNS version query'),
                    ('Enumeration', 'tnscmd10g status -h <target>', 'Oracle TNS status query'),
                    ('Enumeration', 'nmap --script oracle-sid-brute -p 1521 <target>', 'Oracle SID enumeration'),
                    ('Exploitation', 'odat all -s <target> -p 1521', 'Oracle Database Attacking Tool'),
                ]
            },
            # NFS - Port 2049
            {
                'port': 2049,
                'service': 'NFS',
                'description': 'Network File System',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 2049 <target>', 'Version detection on NFS service'),
                    ('Enumeration', 'showmount -e <target>', 'List NFS exports'),
                    ('Enumeration', 'nmap --script nfs-* -p 2049 <target>', 'Run all NFS NSE scripts'),
                    ('Exploitation', 'mount -t nfs <target>:/share /mnt/nfs', 'Mount NFS share'),
                ]
            },
            # MySQL - Port 3306
            {
                'port': 3306,
                'service': 'MySQL',
                'description': 'MySQL Database',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 3306 <target>', 'Version detection on MySQL service'),
                    ('Enumeration', 'nmap --script mysql-info -p 3306 <target>', 'MySQL information gathering'),
                    ('Enumeration', 'nmap --script mysql-empty-password -p 3306 <target>', 'Check for empty root password'),
                    ('Enumeration', 'nmap --script mysql-databases -p 3306 <target>', 'Enumerate MySQL databases'),
                    ('Exploitation', 'mysql -h <target> -u root -p', 'Connect to MySQL server'),
                    ('Exploitation', 'hydra -L users.txt -P passwords.txt mysql://<target>', 'Brute force MySQL credentials'),
                ]
            },
            # RDP - Port 3389
            {
                'port': 3389,
                'service': 'RDP',
                'description': 'Remote Desktop Protocol',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 3389 <target>', 'Version detection on RDP service'),
                    ('Enumeration', 'nmap --script rdp-enum-encryption -p 3389 <target>', 'Enumerate RDP encryption'),
                    ('Enumeration', 'nmap --script rdp-ntlm-info -p 3389 <target>', 'Gather NTLM info via RDP'),
                    ('Exploitation', 'xfreerdp /v:<target> /u:<user> /p:<password>', 'Connect to RDP server (Linux)'),
                    ('Exploitation', 'rdesktop <target>', 'Connect to RDP server'),
                    ('Exploitation', 'hydra -L users.txt -P passwords.txt rdp://<target>', 'Brute force RDP credentials'),
                    ('Exploitation', 'crowbar -b rdp -s <target>/32 -u <user> -C passwords.txt', 'RDP password spraying'),
                ]
            },
            # PostgreSQL - Port 5432
            {
                'port': 5432,
                'service': 'PostgreSQL',
                'description': 'PostgreSQL Database',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 5432 <target>', 'Version detection on PostgreSQL service'),
                    ('Enumeration', 'nmap --script pgsql-brute -p 5432 <target>', 'PostgreSQL brute force'),
                    ('Exploitation', 'psql -h <target> -U postgres', 'Connect to PostgreSQL server'),
                    ('Exploitation', 'psql -h <target> -U <user> -d <database>', 'Connect to specific database'),
                ]
            },
            # VNC - Port 5900
            {
                'port': 5900,
                'service': 'VNC',
                'description': 'Virtual Network Computing',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 5900 <target>', 'Version detection on VNC service'),
                    ('Enumeration', 'nmap --script vnc-info -p 5900 <target>', 'VNC information gathering'),
                    ('Exploitation', 'vncviewer <target>', 'Connect to VNC server'),
                    ('Exploitation', 'hydra -P passwords.txt vnc://<target>', 'Brute force VNC password'),
                ]
            },
            # Redis - Port 6379
            {
                'port': 6379,
                'service': 'Redis',
                'description': 'Redis Key-Value Store',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 6379 <target>', 'Version detection on Redis service'),
                    ('Enumeration', 'redis-cli -h <target> INFO', 'Get Redis server information'),
                    ('Enumeration', 'nmap --script redis-info -p 6379 <target>', 'Redis information gathering'),
                    ('Exploitation', 'redis-cli -h <target>', 'Connect to Redis server'),
                    ('Exploitation', 'redis-cli -h <target> CONFIG GET dir', 'Get Redis configuration'),
                ]
            },
            # HTTP Proxy - Port 8080
            {
                'port': 8080,
                'service': 'HTTP-Proxy',
                'description': 'HTTP Proxy / Alternative HTTP',
                'commands': [
                    ('Reconnaissance', 'nmap -sV -p 8080 <target>', 'Version detection on HTTP-Proxy service'),
                    ('Enumeration', 'nikto -h http://<target>:8080', 'Web server vulnerability scanner'),
                    ('Enumeration', 'gobuster dir -u http://<target>:8080 -w /usr/share/wordlists/dirb/common.txt', 'Directory brute forcing'),
                    ('Enumeration', 'curl -I http://<target>:8080', 'Grab HTTP headers'),
                    ('Exploitation', 'sqlmap -u "http://<target>:8080/page?id=1" --batch', 'SQL injection testing'),
                ]
            },
        ]
        
        # Insert data
        for item in default_data:
            self.cursor.execute(
                'INSERT OR IGNORE INTO ports (port_number, service_name, description) VALUES (?, ?, ?)',
                (item['port'], item['service'], item['description'])
            )
            port_id = self.cursor.lastrowid
            
            # If port already existed, get its ID
            if port_id == 0:
                self.cursor.execute(
                    'SELECT id FROM ports WHERE port_number = ? AND service_name = ?',
                    (item['port'], item['service'])
                )
                port_id = self.cursor.fetchone()[0]
            
            # Insert commands
            for category, command, description in item['commands']:
                self.cursor.execute(
                    'INSERT INTO commands (port_id, category, command, description) VALUES (?, ?, ?, ?)',
                    (port_id, category, command, description)
                )
        
        self.conn.commit()
    
    def setup_gui(self):
        """Setup the main GUI components"""
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        style.configure('TButton', background=self.secondary_bg, foreground=self.fg_color)
        style.map('TButton', background=[('active', self.accent_color)])
        style.configure('Treeview', background=self.secondary_bg, foreground=self.text_color, 
                       fieldbackground=self.secondary_bg, borderwidth=0)
        style.map('Treeview', background=[('selected', self.highlight_color)])
        style.configure('Treeview.Heading', background=self.accent_color, foreground=self.bg_color)
        
        # Header
        header = tk.Frame(self.root, bg=self.accent_color, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="⚡ PORT & SERVICE COMMAND REFERENCE ⚡", 
                              font=('Courier', 20, 'bold'), bg=self.accent_color, 
                              fg=self.bg_color)
        title_label.pack(pady=15)
        
        # Target Configuration Panel
        target_panel = tk.Frame(self.root, bg=self.secondary_bg, height=80)
        target_panel.pack(fill='x', padx=10, pady=(10, 0))
        target_panel.pack_propagate(False)
        
        tk.Label(target_panel, text="TARGET CONFIGURATION", font=('Courier', 10, 'bold'),
                bg=self.secondary_bg, fg=self.fg_color).grid(row=0, column=0, columnspan=6, 
                                                              sticky='w', padx=10, pady=(5, 2))
        
        # Target IP
        tk.Label(target_panel, text="Target IP:", font=('Courier', 9, 'bold'),
                bg=self.secondary_bg, fg=self.text_color).grid(row=1, column=0, sticky='w', padx=(10, 5), pady=5)
        self.target_var = tk.StringVar()
        tk.Entry(target_panel, textvariable=self.target_var, bg=self.bg_color, fg=self.fg_color,
                insertbackground=self.fg_color, font=('Courier', 9), width=18).grid(row=1, column=1, 
                                                                                      sticky='w', pady=5)
        
        # Domain
        tk.Label(target_panel, text="Domain:", font=('Courier', 9, 'bold'),
                bg=self.secondary_bg, fg=self.text_color).grid(row=1, column=2, sticky='w', padx=(15, 5), pady=5)
        self.domain_var = tk.StringVar()
        tk.Entry(target_panel, textvariable=self.domain_var, bg=self.bg_color, fg=self.fg_color,
                insertbackground=self.fg_color, font=('Courier', 9), width=18).grid(row=1, column=3, 
                                                                                      sticky='w', pady=5)
        
        # Username
        tk.Label(target_panel, text="Username:", font=('Courier', 9, 'bold'),
                bg=self.secondary_bg, fg=self.text_color).grid(row=1, column=4, sticky='w', padx=(15, 5), pady=5)
        self.username_var = tk.StringVar()
        tk.Entry(target_panel, textvariable=self.username_var, bg=self.bg_color, fg=self.fg_color,
                insertbackground=self.fg_color, font=('Courier', 9), width=15).grid(row=1, column=5, 
                                                                                      sticky='w', pady=5)
        
        # Auto-replace checkbox
        self.auto_replace_var = tk.BooleanVar(value=True)
        tk.Checkbutton(target_panel, text="Auto-replace placeholders when copying", 
                      variable=self.auto_replace_var, bg=self.secondary_bg, fg=self.text_color,
                      selectcolor=self.bg_color, activebackground=self.secondary_bg,
                      activeforeground=self.fg_color, font=('Courier', 9)).grid(row=2, column=0, 
                                                                                  columnspan=6, 
                                                                                  sticky='w', padx=10, pady=(0, 5))
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Port/Service list
        left_panel = tk.Frame(main_container, bg=self.bg_color, width=400)
        left_panel.pack(side='left', fill='both', padx=(0, 5))
        
        # Search frame
        search_frame = tk.Frame(left_panel, bg=self.bg_color)
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg=self.bg_color, fg=self.fg_color, 
                font=('Courier', 10, 'bold')).pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.refresh_port_list())
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                               bg=self.secondary_bg, fg=self.text_color, 
                               insertbackground=self.fg_color, font=('Courier', 10))
        search_entry.pack(side='left', fill='x', expand=True)
        
        # Port list
        list_frame = tk.Frame(left_panel, bg=self.bg_color)
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.port_tree = ttk.Treeview(list_frame, columns=('Port', 'Service', 'Description'),
                                      show='headings', yscrollcommand=scrollbar.set)
        self.port_tree.heading('Port', text='Port')
        self.port_tree.heading('Service', text='Service')
        self.port_tree.heading('Description', text='Description')
        
        self.port_tree.column('Port', width=60)
        self.port_tree.column('Service', width=100)
        self.port_tree.column('Description', width=240)
        
        self.port_tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.port_tree.yview)
        
        self.port_tree.bind('<<TreeviewSelect>>', self.on_port_select)
        
        # Buttons for port management
        button_frame = tk.Frame(left_panel, bg=self.bg_color)
        button_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(button_frame, text="Add Port/Service", command=self.add_port,
                 bg=self.secondary_bg, fg=self.fg_color, font=('Courier', 9, 'bold'),
                 activebackground=self.accent_color).pack(side='left', padx=2, expand=True, fill='x')
        
        tk.Button(button_frame, text="Edit", command=self.edit_port,
                 bg=self.secondary_bg, fg=self.fg_color, font=('Courier', 9, 'bold'),
                 activebackground=self.accent_color).pack(side='left', padx=2, expand=True, fill='x')
        
        tk.Button(button_frame, text="Delete", command=self.delete_port,
                 bg=self.secondary_bg, fg=self.fg_color, font=('Courier', 9, 'bold'),
                 activebackground=self.accent_color).pack(side='left', padx=2, expand=True, fill='x')
        
        # Right panel - Commands
        right_panel = tk.Frame(main_container, bg=self.bg_color)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Category filter
        filter_frame = tk.Frame(right_panel, bg=self.bg_color)
        filter_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(filter_frame, text="Category:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).pack(side='left', padx=(0, 5))
        
        self.category_var = tk.StringVar(value="All")
        categories = ['All', 'Reconnaissance', 'Enumeration', 'Exploitation', 'Post-Exploitation']
        
        for cat in categories:
            tk.Radiobutton(filter_frame, text=cat, variable=self.category_var, value=cat,
                          bg=self.bg_color, fg=self.text_color, selectcolor=self.secondary_bg,
                          activebackground=self.bg_color, activeforeground=self.fg_color,
                          font=('Courier', 9), command=self.refresh_commands).pack(side='left', padx=5)
        
        # Commands display
        commands_frame = tk.Frame(right_panel, bg=self.bg_color)
        commands_frame.pack(fill='both', expand=True)
        
        self.commands_text = scrolledtext.ScrolledText(commands_frame, wrap=tk.WORD,
                                                        bg=self.secondary_bg, fg=self.text_color,
                                                        font=('Courier', 10), insertbackground=self.fg_color)
        self.commands_text.pack(fill='both', expand=True)
        
        # Command management buttons
        cmd_button_frame = tk.Frame(right_panel, bg=self.bg_color)
        cmd_button_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(cmd_button_frame, text="Add Command", command=self.add_command,
                 bg=self.secondary_bg, fg=self.fg_color, font=('Courier', 9, 'bold'),
                 activebackground=self.accent_color).pack(side='left', padx=2, expand=True, fill='x')
        
        tk.Button(cmd_button_frame, text="Edit Command", command=self.edit_command,
                 bg=self.secondary_bg, fg=self.fg_color, font=('Courier', 9, 'bold'),
                 activebackground=self.accent_color).pack(side='left', padx=2, expand=True, fill='x')
        
        tk.Button(cmd_button_frame, text="Delete Command", command=self.delete_command,
                 bg=self.secondary_bg, fg=self.fg_color, font=('Courier', 9, 'bold'),
                 activebackground=self.accent_color).pack(side='left', padx=2, expand=True, fill='x')
        
        # Footer
        footer = tk.Frame(self.root, bg=self.accent_color, height=30)
        footer.pack(fill='x')
        footer.pack_propagate(False)
        
        footer_label = tk.Label(footer, text="SwiftGunner © 2024 | Streamline Your Enumeration", 
                               font=('Courier', 9), bg=self.accent_color, fg=self.bg_color)
        footer_label.pack(pady=5)
    
    def refresh_port_list(self):
        """Refresh the port/service list"""
        # Clear current items
        for item in self.port_tree.get_children():
            self.port_tree.delete(item)
        
        # Get search term
        search_term = self.search_var.get().lower()
        
        # Query database
        if search_term:
            self.cursor.execute('''
                SELECT id, port_number, service_name, description 
                FROM ports 
                WHERE LOWER(service_name) LIKE ? OR CAST(port_number AS TEXT) LIKE ? OR LOWER(description) LIKE ?
                ORDER BY port_number
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            self.cursor.execute('SELECT id, port_number, service_name, description FROM ports ORDER BY port_number')
        
        # Insert items
        for row in self.cursor.fetchall():
            port_id, port_num, service, desc = row
            self.port_tree.insert('', 'end', values=(port_num, service, desc), tags=(port_id,))
    
    def on_port_select(self, event):
        """Handle port selection"""
        selection = self.port_tree.selection()
        if selection:
            self.current_port_id = self.port_tree.item(selection[0])['tags'][0]
            self.refresh_commands()
    
    def refresh_commands(self):
        """Refresh the commands display"""
        if not hasattr(self, 'current_port_id'):
            return
        
        # Clear text widget
        self.commands_text.delete('1.0', tk.END)
        
        # Get category filter
        category = self.category_var.get()
        
        # Query commands
        if category == 'All':
            self.cursor.execute('''
                SELECT category, command, description 
                FROM commands 
                WHERE port_id = ?
                ORDER BY 
                    CASE category
                        WHEN 'Reconnaissance' THEN 1
                        WHEN 'Enumeration' THEN 2
                        WHEN 'Exploitation' THEN 3
                        WHEN 'Post-Exploitation' THEN 4
                        ELSE 5
                    END
            ''', (self.current_port_id,))
        else:
            self.cursor.execute('''
                SELECT category, command, description 
                FROM commands 
                WHERE port_id = ? AND category = ?
            ''', (self.current_port_id, category))
        
        commands = self.cursor.fetchall()
        
        if not commands:
            self.commands_text.insert('1.0', "No commands found for selected filters.\n\n")
            return
        
        # Get port info
        self.cursor.execute('SELECT port_number, service_name FROM ports WHERE id = ?', (self.current_port_id,))
        port_info = self.cursor.fetchone()
        
        # Display header
        header = f"{'='*80}\n"
        header += f"Port {port_info[0]} - {port_info[1]}\n"
        header += f"{'='*80}\n\n"
        self.commands_text.insert('end', header, 'header')
        
        # Group by category
        current_category = None
        for cat, cmd, desc in commands:
            if cat != current_category:
                self.commands_text.insert('end', f"\n[{cat}]\n", 'category')
                self.commands_text.insert('end', f"{'-'*80}\n", 'separator')
                current_category = cat
            
            # Create clickable command with copy button
            cmd_start = self.commands_text.index('end-1c')
            self.commands_text.insert('end', f"\n{cmd}\n", 'command')
            cmd_end = self.commands_text.index('end-1c')
            
            # Add copy button
            copy_btn = tk.Button(self.commands_text, text="📋 Copy", 
                               command=lambda c=cmd: self.copy_command(c),
                               bg=self.accent_color, fg=self.bg_color, 
                               font=('Courier', 8, 'bold'),
                               cursor='hand2')
            self.commands_text.window_create('end', window=copy_btn)
            
            self.commands_text.insert('end', f"\nDescription: {desc}\n\n", 'description')
        
        # Configure tags
        self.commands_text.tag_config('header', foreground=self.fg_color, font=('Courier', 11, 'bold'))
        self.commands_text.tag_config('category', foreground=self.accent_color, font=('Courier', 10, 'bold'))
        self.commands_text.tag_config('separator', foreground=self.accent_color)
        self.commands_text.tag_config('command', foreground=self.fg_color, font=('Courier', 10, 'bold'))
        self.commands_text.tag_config('description', foreground=self.text_color, font=('Courier', 9))
    
    def copy_command(self, command):
        """Copy command to clipboard with optional placeholder replacement"""
        final_command = command
        
        # Auto-replace placeholders if enabled
        if self.auto_replace_var.get():
            replacements = {
                '<target>': self.target_var.get(),
                '<domain>': self.domain_var.get(),
                '<user>': self.username_var.get(),
            }
            
            # Only replace if value is provided
            for placeholder, value in replacements.items():
                if value.strip():
                    final_command = final_command.replace(placeholder, value.strip())
        
        pyperclip.copy(final_command)
        
        # Show what was copied
        if final_command != command:
            messagebox.showinfo("Copied with Replacements", 
                              f"Original:\n{command}\n\n"
                              f"Copied to clipboard:\n{final_command}")
        else:
            messagebox.showinfo("Copied", f"Command copied to clipboard:\n\n{final_command}")
    
    def add_port(self):
        """Add new port/service"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Port/Service")
        dialog.geometry("500x300")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Port number
        tk.Label(dialog, text="Port Number:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        port_entry = tk.Entry(dialog, bg=self.secondary_bg, fg=self.text_color, 
                             insertbackground=self.fg_color, font=('Courier', 10))
        port_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        # Service name
        tk.Label(dialog, text="Service Name:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        service_entry = tk.Entry(dialog, bg=self.secondary_bg, fg=self.text_color,
                                insertbackground=self.fg_color, font=('Courier', 10))
        service_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        # Description
        tk.Label(dialog, text="Description:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=2, column=0, sticky='nw', padx=10, pady=5)
        desc_text = tk.Text(dialog, bg=self.secondary_bg, fg=self.text_color,
                           insertbackground=self.fg_color, font=('Courier', 10), height=5)
        desc_text.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def save_port():
            port = port_entry.get().strip()
            service = service_entry.get().strip()
            description = desc_text.get('1.0', 'end-1c').strip()
            
            if not port or not service:
                messagebox.showerror("Error", "Port number and service name are required!")
                return
            
            try:
                port_num = int(port)
                self.cursor.execute(
                    'INSERT INTO ports (port_number, service_name, description) VALUES (?, ?, ?)',
                    (port_num, service, description)
                )
                self.conn.commit()
                self.refresh_port_list()
                dialog.destroy()
                messagebox.showinfo("Success", f"Port {port_num} - {service} added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Port number must be a valid integer!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "This port/service combination already exists!")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Save", command=save_port, bg=self.accent_color,
                 fg=self.bg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg=self.secondary_bg,
                 fg=self.fg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
    
    def edit_port(self):
        """Edit selected port/service"""
        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a port to edit!")
            return
        
        port_id = self.port_tree.item(selection[0])['tags'][0]
        
        # Get current data
        self.cursor.execute('SELECT port_number, service_name, description FROM ports WHERE id = ?', (port_id,))
        current_data = self.cursor.fetchone()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Port/Service")
        dialog.geometry("500x300")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Port number
        tk.Label(dialog, text="Port Number:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        port_entry = tk.Entry(dialog, bg=self.secondary_bg, fg=self.text_color,
                             insertbackground=self.fg_color, font=('Courier', 10))
        port_entry.insert(0, current_data[0])
        port_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        # Service name
        tk.Label(dialog, text="Service Name:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        service_entry = tk.Entry(dialog, bg=self.secondary_bg, fg=self.text_color,
                                insertbackground=self.fg_color, font=('Courier', 10))
        service_entry.insert(0, current_data[1])
        service_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        # Description
        tk.Label(dialog, text="Description:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=2, column=0, sticky='nw', padx=10, pady=5)
        desc_text = tk.Text(dialog, bg=self.secondary_bg, fg=self.text_color,
                           insertbackground=self.fg_color, font=('Courier', 10), height=5)
        desc_text.insert('1.0', current_data[2] if current_data[2] else '')
        desc_text.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def update_port():
            port = port_entry.get().strip()
            service = service_entry.get().strip()
            description = desc_text.get('1.0', 'end-1c').strip()
            
            if not port or not service:
                messagebox.showerror("Error", "Port number and service name are required!")
                return
            
            try:
                port_num = int(port)
                self.cursor.execute(
                    'UPDATE ports SET port_number = ?, service_name = ?, description = ? WHERE id = ?',
                    (port_num, service, description, port_id)
                )
                self.conn.commit()
                self.refresh_port_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Port/service updated successfully!")
            except ValueError:
                messagebox.showerror("Error", "Port number must be a valid integer!")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Update", command=update_port, bg=self.accent_color,
                 fg=self.bg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg=self.secondary_bg,
                 fg=self.fg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
    
    def delete_port(self):
        """Delete selected port/service"""
        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a port to delete!")
            return
        
        port_id = self.port_tree.item(selection[0])['tags'][0]
        port_info = self.port_tree.item(selection[0])['values']
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Delete Port {port_info[0]} - {port_info[1]}?\n\nThis will also delete all associated commands."):
            self.cursor.execute('DELETE FROM ports WHERE id = ?', (port_id,))
            self.conn.commit()
            self.refresh_port_list()
            self.commands_text.delete('1.0', tk.END)
            messagebox.showinfo("Success", "Port/service deleted successfully!")
    
    def add_command(self):
        """Add command to selected port"""
        if not hasattr(self, 'current_port_id'):
            messagebox.showwarning("Warning", "Please select a port first!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Command")
        dialog.geometry("600x400")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Category
        tk.Label(dialog, text="Category:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        category_var = tk.StringVar(value='Reconnaissance')
        category_menu = ttk.Combobox(dialog, textvariable=category_var,
                                    values=['Reconnaissance', 'Enumeration', 'Exploitation', 'Post-Exploitation'],
                                    state='readonly', font=('Courier', 10))
        category_menu.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        # Command
        tk.Label(dialog, text="Command:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=1, column=0, sticky='nw', padx=10, pady=5)
        cmd_text = tk.Text(dialog, bg=self.secondary_bg, fg=self.text_color,
                          insertbackground=self.fg_color, font=('Courier', 10), height=8)
        cmd_text.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        # Description
        tk.Label(dialog, text="Description:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=2, column=0, sticky='nw', padx=10, pady=5)
        desc_text = tk.Text(dialog, bg=self.secondary_bg, fg=self.text_color,
                           insertbackground=self.fg_color, font=('Courier', 10), height=5)
        desc_text.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def save_command():
            category = category_var.get()
            command = cmd_text.get('1.0', 'end-1c').strip()
            description = desc_text.get('1.0', 'end-1c').strip()
            
            if not command or not description:
                messagebox.showerror("Error", "Command and description are required!")
                return
            
            self.cursor.execute(
                'INSERT INTO commands (port_id, category, command, description) VALUES (?, ?, ?, ?)',
                (self.current_port_id, category, command, description)
            )
            self.conn.commit()
            self.refresh_commands()
            dialog.destroy()
            messagebox.showinfo("Success", "Command added successfully!")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Save", command=save_command, bg=self.accent_color,
                 fg=self.bg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg=self.secondary_bg,
                 fg=self.fg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
    
    def edit_command(self):
        """Edit command - simplified selection"""
        if not hasattr(self, 'current_port_id'):
            messagebox.showwarning("Warning", "Please select a port first!")
            return
        
        # Get all commands for current port
        self.cursor.execute('''
            SELECT id, category, command, description 
            FROM commands 
            WHERE port_id = ?
        ''', (self.current_port_id,))
        
        commands = self.cursor.fetchall()
        
        if not commands:
            messagebox.showinfo("Info", "No commands to edit for this port!")
            return
        
        # Selection dialog
        select_dialog = tk.Toplevel(self.root)
        select_dialog.title("Select Command to Edit")
        select_dialog.geometry("800x400")
        select_dialog.configure(bg=self.bg_color)
        select_dialog.transient(self.root)
        select_dialog.grab_set()
        
        tk.Label(select_dialog, text="Select a command to edit:", bg=self.bg_color, 
                fg=self.fg_color, font=('Courier', 11, 'bold')).pack(pady=10)
        
        listbox_frame = tk.Frame(select_dialog, bg=self.bg_color)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        command_list = tk.Listbox(listbox_frame, bg=self.secondary_bg, fg=self.text_color,
                                 font=('Courier', 9), yscrollcommand=scrollbar.set,
                                 selectbackground=self.highlight_color)
        command_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=command_list.yview)
        
        # Populate list
        for cmd_id, cat, cmd, desc in commands:
            display_text = f"[{cat}] {cmd[:60]}..."
            command_list.insert('end', display_text)
        
        def on_select():
            selection = command_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a command!")
                return
            
            cmd_id = commands[selection[0]][0]
            select_dialog.destroy()
            self.show_edit_command_dialog(cmd_id)
        
        tk.Button(select_dialog, text="Edit Selected", command=on_select, bg=self.accent_color,
                 fg=self.bg_color, font=('Courier', 10, 'bold')).pack(pady=10)
    
    def show_edit_command_dialog(self, cmd_id):
        """Show dialog to edit a specific command"""
        # Get command data
        self.cursor.execute('SELECT category, command, description FROM commands WHERE id = ?', (cmd_id,))
        current_data = self.cursor.fetchone()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Command")
        dialog.geometry("600x400")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Category
        tk.Label(dialog, text="Category:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        category_var = tk.StringVar(value=current_data[0])
        category_menu = ttk.Combobox(dialog, textvariable=category_var,
                                    values=['Reconnaissance', 'Enumeration', 'Exploitation', 'Post-Exploitation'],
                                    state='readonly', font=('Courier', 10))
        category_menu.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        # Command
        tk.Label(dialog, text="Command:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=1, column=0, sticky='nw', padx=10, pady=5)
        cmd_text = tk.Text(dialog, bg=self.secondary_bg, fg=self.text_color,
                          insertbackground=self.fg_color, font=('Courier', 10), height=8)
        cmd_text.insert('1.0', current_data[1])
        cmd_text.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        # Description
        tk.Label(dialog, text="Description:", bg=self.bg_color, fg=self.fg_color,
                font=('Courier', 10, 'bold')).grid(row=2, column=0, sticky='nw', padx=10, pady=5)
        desc_text = tk.Text(dialog, bg=self.secondary_bg, fg=self.text_color,
                           insertbackground=self.fg_color, font=('Courier', 10), height=5)
        desc_text.insert('1.0', current_data[2])
        desc_text.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        dialog.grid_columnconfigure(1, weight=1)
        
        def update_command():
            category = category_var.get()
            command = cmd_text.get('1.0', 'end-1c').strip()
            description = desc_text.get('1.0', 'end-1c').strip()
            
            if not command or not description:
                messagebox.showerror("Error", "Command and description are required!")
                return
            
            self.cursor.execute(
                'UPDATE commands SET category = ?, command = ?, description = ? WHERE id = ?',
                (category, command, description, cmd_id)
            )
            self.conn.commit()
            self.refresh_commands()
            dialog.destroy()
            messagebox.showinfo("Success", "Command updated successfully!")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Update", command=update_command, bg=self.accent_color,
                 fg=self.bg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg=self.secondary_bg,
                 fg=self.fg_color, font=('Courier', 10, 'bold'), width=10).pack(side='left', padx=5)
    
    def delete_command(self):
        """Delete command - simplified selection"""
        if not hasattr(self, 'current_port_id'):
            messagebox.showwarning("Warning", "Please select a port first!")
            return
        
        # Get all commands for current port
        self.cursor.execute('''
            SELECT id, category, command, description 
            FROM commands 
            WHERE port_id = ?
        ''', (self.current_port_id,))
        
        commands = self.cursor.fetchall()
        
        if not commands:
            messagebox.showinfo("Info", "No commands to delete for this port!")
            return
        
        # Selection dialog
        select_dialog = tk.Toplevel(self.root)
        select_dialog.title("Select Command to Delete")
        select_dialog.geometry("800x400")
        select_dialog.configure(bg=self.bg_color)
        select_dialog.transient(self.root)
        select_dialog.grab_set()
        
        tk.Label(select_dialog, text="Select a command to delete:", bg=self.bg_color,
                fg=self.fg_color, font=('Courier', 11, 'bold')).pack(pady=10)
        
        listbox_frame = tk.Frame(select_dialog, bg=self.bg_color)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        command_list = tk.Listbox(listbox_frame, bg=self.secondary_bg, fg=self.text_color,
                                 font=('Courier', 9), yscrollcommand=scrollbar.set,
                                 selectbackground=self.highlight_color)
        command_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=command_list.yview)
        
        # Populate list
        for cmd_id, cat, cmd, desc in commands:
            display_text = f"[{cat}] {cmd[:60]}..."
            command_list.insert('end', display_text)
        
        def on_delete():
            selection = command_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a command!")
                return
            
            cmd_id = commands[selection[0]][0]
            cmd_preview = commands[selection[0]][2][:60]
            
            if messagebox.askyesno("Confirm Delete", f"Delete this command?\n\n{cmd_preview}..."):
                self.cursor.execute('DELETE FROM commands WHERE id = ?', (cmd_id,))
                self.conn.commit()
                self.refresh_commands()
                select_dialog.destroy()
                messagebox.showinfo("Success", "Command deleted successfully!")
        
        tk.Button(select_dialog, text="Delete Selected", command=on_delete, bg=self.accent_color,
                 fg=self.bg_color, font=('Courier', 10, 'bold')).pack(pady=10)
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = PortServiceTool(root)
    root.mainloop()
