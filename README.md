# Port & Service Command Reference Tool

**by SwiftGunner**

A comprehensive GUI application for penetration testers providing quick access to enumeration and exploitation commands organized by port, service, and category.

![Version](https://img.shields.io/badge/version-1.0-green.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)

---

## 🎯 Features

### Core Functionality
- **Target Configuration Panel** - Set target IP, domain, and username once for automatic placeholder replacement
- **Auto-Replace Placeholders** - Commands automatically filled with your target info when copied
- **Comprehensive Port Database** - Pre-loaded with 20+ common ports and services
- **Command Categories** - Commands organized by: Reconnaissance, Enumeration, Exploitation, Post-Exploitation
- **Quick Search** - Instant filtering by port number, service name, or description
- **Copy to Clipboard** - One-click command copying for rapid deployment
- **Dark Theme** - Professional security-focused interface

### Customization
- **Add Custom Ports** - Extend the database with your own port/service combinations
- **Add Custom Commands** - Add commands specific to your workflow
- **Edit Existing Entries** - Update ports, services, and commands
- **Delete Entries** - Remove outdated or unnecessary data
- **Persistent Storage** - SQLite database maintains all customizations

### Pre-loaded Services
The tool comes pre-populated with commands for:
- FTP (21)
- SSH (22)
- Telnet (23)
- SMTP (25)
- DNS (53)
- HTTP (80)
- Kerberos (88)
- POP3 (110)
- NetBIOS (139)
- IMAP (143)
- SNMP (161)
- LDAP (389)
- HTTPS (443)
- SMB (445)
- MSSQL (1433)
- Oracle (1521)
- NFS (2049)
- MySQL (3306)
- RDP (3389)
- PostgreSQL (5432)
- VNC (5900)
- Redis (6379)
- HTTP-Proxy (8080)

---

## 📋 Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python)
- pyperclip

---

## 🚀 Installation

### 1. Clone or Download

```bash
git clone <repository-url>
cd port-service-tool
```

### 2. make it executable
```
chmod +x port_service_tool.py
```



### 3. Run the Application

```bash
python3 port_service_tool.py
```



---

## 💻 Usage Guide

### Target Configuration (NEW!)

**Set Your Target Once:**
1. Enter your target IP in the "Target IP" field (e.g., `10.10.10.50`)
2. Optionally enter domain name (e.g., `example.com`)
3. Optionally enter username (e.g., `admin`)
4. Ensure "Auto-replace placeholders when copying" is checked

**When You Copy Commands:**
- `<target>` automatically replaced with your IP
- `<domain>` automatically replaced with your domain
- `<user>` automatically replaced with your username
- You'll see both original and final command in the confirmation

**Example:**
```
You enter:    Target IP: 192.168.1.100

Original:     nmap -sV -p 80 <target>
Copied:       nmap -sV -p 80 192.168.1.100

Original:     ssh <user>@<target>
Copied:       ssh admin@192.168.1.100
```

**Toggle Auto-Replace:**
- Uncheck the box to copy commands with placeholders intact
- Useful when you need the template for documentation

### Basic Workflow

1. **Select a Port/Service**
   - Browse the left panel for available ports
   - Use the search bar to filter by port number, service name, or description
   - Click on any entry to view its commands

2. **View Commands**
   - Commands are displayed in the right panel
   - Filter by category using radio buttons (All, Reconnaissance, Enumeration, Exploitation, Post-Exploitation)
   - Each command includes a description and copy button

3. **Copy Commands**
   - Click the "📋 Copy" button next to any command
   - Command is instantly copied to your clipboard
   - Paste directly into your terminal

### Adding Custom Content

#### Add a New Port/Service
1. Click "Add Port/Service" button
2. Enter:
   - Port number (required)
   - Service name (required)
   - Description (optional)
3. Click "Save"

#### Add a Command
1. Select the target port/service from the list
2. Click "Add Command"
3. Select category from dropdown
4. Enter the command
5. Enter description
6. Click "Save"

### Editing Content

#### Edit Port/Service
1. Select the port from the list
2. Click "Edit" button
3. Modify the details
4. Click "Update"

#### Edit Command
1. Select the port containing the command
2. Click "Edit Command"
3. Choose the command from the list
4. Modify as needed
5. Click "Update"

### Deleting Content

#### Delete Port/Service
1. Select the port from the list
2. Click "Delete" button
3. Confirm deletion
   - **Warning**: This deletes ALL associated commands

#### Delete Command
1. Select the port containing the command
2. Click "Delete Command"
3. Choose the command from the list
4. Confirm deletion

---

## 🎨 Interface Guide

### Left Panel - Port/Service List
- **Search Bar**: Filter entries in real-time
- **Port List**: Displays Port | Service | Description
- **Management Buttons**: Add, Edit, Delete ports/services

### Right Panel - Commands Display
- **Category Filter**: Radio buttons to filter by command category
- **Commands Area**: Scrollable display with syntax highlighting
- **Copy Buttons**: Quick clipboard access for each command
- **Management Buttons**: Add, Edit, Delete commands

---

## 🔧 Database Structure

The application uses SQLite with two main tables:

### Ports Table
- `id` - Primary key
- `port_number` - Integer port number
- `service_name` - Service identifier
- `description` - Service description

### Commands Table
- `id` - Primary key
- `port_id` - Foreign key to ports table
- `category` - Command category
- `command` - The actual command
- `description` - Command description

Database file: `port_service_commands.db` (created automatically on first run)

---

## 🎯 Command Placeholders

Commands use the following placeholders:
- `<target>` - Target IP address or hostname
- `<domain>` - Domain name
- `<user>` - Username
- `<password>` - Password
- `<email>` - Email address
- `<share>` - SMB share name
- `<database>` - Database name

Replace these when using commands in your engagements.

---

## 💡 Tips & Best Practices

1. **Customize for Your Workflow**: Add your most-used commands and variations
2. **Keep It Organized**: Use consistent naming and descriptions
3. **Backup Your Database**: Regularly backup `port_service_commands.db`
4. **Update Regularly**: Add new techniques and tools as you discover them
5. **Category Properly**: Accurate categorization makes filtering more effective

---

## 🔐 Security Notes

- This tool is for **authorized penetration testing only**
- Always obtain proper authorization before testing
- Commands are templates - verify and customize for each engagement
- Some commands may require root/administrator privileges
- Not all commands work on all systems - test in your environment

---

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.6+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check for error messages in terminal

### Copy to clipboard not working
- Install xclip (Linux): `sudo apt-get install xclip`
- Install xsel (Linux alternative): `sudo apt-get install xsel`
- Windows and Mac should work out of the box with pyperclip

### Database errors
- Delete `port_service_commands.db` to reset
- Application will recreate with default data on next run

### Display issues
- Ensure tkinter is installed: `python -m tkinter`
- Update your Python installation if tkinter is missing

---

## 📝 Changelog

### Version 1.0 (Initial Release)
- Complete port/service database with 20+ services
- Command categorization system
- Search and filter functionality
- Copy to clipboard feature
- Full CRUD operations for customization
- Dark professional theme
- SQLite database backend

---

## 🤝 Contributing

Suggestions and improvements are welcome! Common additions:
- New ports and services
- Additional commands for existing services
- Command optimizations
- Feature requests

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

## 👤 Author

**SwiftGunner**

*Streamline Your Enumeration*

---

## 🙏 Acknowledgments

Built to streamline repetitive tasks and improve efficiency during security assessments. Special thanks to the security community for tools like nmap, metasploit, hydra, and countless others that make this work possible.

---

**Stay safe. Stay ethical. Happy hunting! 🎯**
