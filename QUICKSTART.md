# Quick Start Guide - Port & Service Command Reference Tool

## Instant Setup (3 Steps)

### 1. Install Dependencies
```bash
pip install pyperclip
```

### 2. Run the Application
```bash
python port_service_tool.py
```

### 3. Start Using
- **Set your target IP** in the target configuration panel at top
- Browse ports in the left panel
- View commands in the right panel
- Click "📋 Copy" to copy command with auto-replaced IP
- Filter by category using radio buttons
- Search with the search bar

---

## First Time Use

The application will automatically:
- Create `port_service_commands.db` (SQLite database)
- Populate with 20+ common ports and 100+ commands
- Ready to use immediately!

---

## Adding Custom Content

### Quick Add Port
1. Click "Add Port/Service"
2. Fill: Port Number, Service Name, Description
3. Save

### Quick Add Command
1. Select port from list
2. Click "Add Command"
3. Select category, enter command and description
4. Save

---

## Common Use Cases

**Quick Start Example:**
```
1. Set Target IP: 10.10.10.50
2. Search for "445" (SMB)
3. Filter by "Enumeration"
4. Click Copy on: smbclient -L //<target> -N
5. Pasted command: smbclient -L //10.10.10.50 -N
6. Run directly - no manual editing needed!
```

**During Recon:**
1. Enter target IP at the top
2. Search for port (e.g., "80")
3. Filter by "Reconnaissance" or "Enumeration"
4. Copy desired commands (auto-filled with your IP)
5. Paste into terminal - ready to run!

**Custom Workflow:**
1. Add your custom ports/services
2. Add your preferred command variations
3. Build your personalized pentesting command library

---

## Keyboard Shortcuts
- **Tab** - Navigate between fields in dialogs
- **Enter** - Confirm/Save in dialogs
- **Esc** - Close dialogs (in most cases)

---

## Pro Tips

✓ **Backup regularly**: Copy `port_service_commands.db`
✓ **Customize freely**: Add your own tools and variations
✓ **Use placeholders**: Replace `<target>`, `<user>`, etc.
✓ **Stay organized**: Use clear descriptions for easy searching
✓ **Export commands**: Copy to a text file for documentation

---

## Troubleshooting

**Issue**: ModuleNotFoundError: No module named 'tkinter'

**Linux Fix**:
```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**Mac**: Usually pre-installed with Python

**Windows**: Usually pre-installed with Python

---

**Issue**: Copy to clipboard not working (Linux)

**Fix**:
```bash
# Install xclip
sudo apt-get install xclip

# Or xsel
sudo apt-get install xsel
```

---

## Need Help?

Check the full README.md for:
- Complete feature list
- Detailed usage guide
- Database structure
- Security notes
- And more!

---

**SwiftGunner - Streamline Your Enumeration** 🎯
