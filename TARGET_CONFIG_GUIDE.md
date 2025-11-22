# Target Configuration Feature Guide

## 🎯 Auto-Replace Your Target IP

### The Problem (Before)
```
Your target: 10.10.10.50

You copy:    nmap -sV -p 22 <target>
Terminal:    nmap -sV -p 22 <target>    ← Still has placeholder
You edit:    nmap -sV -p 22 10.10.10.50 ← Manual typing
You run:     Finally ready...

Every. Single. Command. 😫
```

### The Solution (Now)
```
Your target: 10.10.10.50

Set once:    [Target IP: 10.10.10.50] ✓ Auto-replace
You copy:    nmap -sV -p 22 <target>
Clipboard:   nmap -sV -p 22 10.10.10.50 ← Automatically filled!
You paste:   Ready to run immediately! ✅

Set once, use everywhere! 🚀
```

---

## 📋 Setup Instructions

### Step 1: Enter Your Target Info
```
┌─────────────────────────────────────────────────┐
│ TARGET CONFIGURATION                            │
│ ─────────────────────────────────────────────── │
│ Target IP:  [10.10.10.50________]               │
│ Domain:     [example.com________]               │
│ Username:   [admin______________]               │
│ ☑ Auto-replace placeholders when copying        │
└─────────────────────────────────────────────────┘
```

### Step 2: Use Commands Normally
Just copy as usual - replacements happen automatically!

---

## 🔄 What Gets Replaced

| Placeholder | Replace With     | Example            |
|-------------|------------------|--------------------|
| `<target>`  | Target IP field  | `10.10.10.50`      |
| `<domain>`  | Domain field     | `example.com`      |
| `<user>`    | Username field   | `admin`            |

**Note:** Only placeholders with filled fields get replaced!

---

## 💡 Real-World Examples

### Example 1: Nmap Scan
```
SET: Target IP = 192.168.1.100

ORIGINAL:  nmap -sV -p 80,443 <target>
COPIED:    nmap -sV -p 80,443 192.168.1.100
```

### Example 2: SSH Connection
```
SET: Target IP = 10.10.10.50
     Username  = root

ORIGINAL:  ssh <user>@<target>
COPIED:    ssh root@10.10.10.50
```

### Example 3: SMB Enumeration
```
SET: Target IP = 192.168.50.100

ORIGINAL:  smbclient -L //<target> -N
COPIED:    smbclient -L //192.168.50.100 -N
```

### Example 4: Multiple Placeholders
```
SET: Target IP = 10.10.10.50
     Domain    = COMPANY.local
     Username  = administrator

ORIGINAL:  GetUserSPNs.py <domain>/<user> -dc-ip <target> -request
COPIED:    GetUserSPNs.py COMPANY.local/administrator -dc-ip 10.10.10.50 -request
```

---

## 🎛️ Toggle On/Off

### When to Enable (Default)
✓ Active engagement with a single target
✓ Running multiple commands against same host
✓ Want copy-paste-run workflow
✓ Most common use case

### When to Disable
✓ Need template commands for documentation
✓ Multiple different targets
✓ Creating command cheat sheet
✓ Teaching/training scenarios

**Toggle:** Just uncheck "Auto-replace placeholders when copying"

---

## 🔍 Confirmation Dialog

When you copy a command with auto-replace enabled, you'll see:

```
╔═══════════════════════════════════════════════╗
║  Copied with Replacements                     ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Original:                                    ║
║  nmap -sV -p 22 <target>                      ║
║                                               ║
║  Copied to clipboard:                         ║
║  nmap -sV -p 22 10.10.10.50                   ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

**Why?** So you can verify the replacement before running!

---

## ⚡ Pro Tips

### Tip 1: Set Target First
```
1. Launch tool
2. Enter target IP immediately
3. Browse/copy commands freely
4. Everything auto-fills!
```

### Tip 2: Change Targets Easily
```
Working on new box?
→ Just update the Target IP field
→ All future copies use new IP
→ No need to restart!
```

### Tip 3: Partial Replacement
```
If you only fill Target IP:
→ <target> gets replaced
→ <domain> stays as <domain>
→ <user> stays as <user>

Mix auto & manual as needed!
```

### Tip 4: Quick Verification
```
Dialog shows you BOTH:
→ Original command (template)
→ Final command (what's copied)

Catch mistakes before running!
```

---

## 🎯 Efficiency Gains

### Manual Workflow
```
Time per command:
- Copy: 1 second
- Paste: 1 second  
- Edit <target>: 3-5 seconds
- Verify: 2 seconds
───────────────────
Total: 7-9 seconds

For 50 commands: 6-8 minutes wasted typing IPs!
```

### Auto-Replace Workflow
```
Time per command:
- Copy: 1 second
- Paste: 1 second
- Review dialog: 1 second
- Run: Immediate!
───────────────────
Total: 3 seconds

For 50 commands: 2.5 minutes total
Saved: 4-5.5 minutes! ⚡
```

**Plus:** No typos, no copy-paste errors, no frustration!

---

## 🚫 What Doesn't Get Replaced

These placeholders require manual replacement:
- `<password>` (security - never store passwords)
- `<email>` (too variable)
- `<share>` (SMB share names)
- `<database>` (database names)
- Custom placeholders in your added commands

**Why?** These vary too much per command to auto-replace safely.

---

## 🛠️ Advanced Usage

### Multi-Target Scenario
```
Target 1: 10.10.10.50
→ Set IP, run scans
→ Copy results

Target 2: 10.10.10.51  
→ Change IP field
→ Run same scans
→ Compare results

Quick pivoting between targets!
```

### Documentation Mode
```
Writing report:
→ Uncheck auto-replace
→ Copy commands with placeholders
→ Paste into report
→ Generic templates for documentation
```

### Training Mode
```
Teaching someone:
→ Show command with <target>
→ Explain what it does
→ Enable auto-replace
→ Show filled version
→ Perfect for demonstrations!
```

---

## 📊 Feature Comparison

| Feature                    | Without Config | With Config |
|----------------------------|----------------|-------------|
| Copy command               | ✓              | ✓           |
| Manual IP replacement      | Required       | Optional    |
| Typo risk                  | High           | Zero        |
| Time per command           | 7-9 sec        | 3 sec       |
| Workflow interruption      | Every command  | Never       |
| Multi-command efficiency   | Low            | High        |
| Verification dialog        | ✗              | ✓           |

---

## 🎓 Learning Curve

**Time to Master:** 30 seconds

1. See the target fields at top ← 5 seconds
2. Type your IP ← 5 seconds  
3. Copy a command ← 5 seconds
4. See it auto-filled ← 5 seconds
5. "Oh, that's brilliant!" ← 10 seconds

**ROI:** Immediate

---

## 🏆 Why This Matters

In penetration testing:
- Speed matters
- Accuracy matters  
- Focus matters

**This feature gives you all three.**

Instead of:
- Thinking about IP addresses
- Editing every command
- Double-checking typos
- Breaking your flow

You can:
- Focus on methodology
- Move through ports rapidly
- Maintain concentration
- Work professionally

**That's the SwiftGunner difference.** 🎯

---

**Set once. Use everywhere. Enumerate faster.** ⚡
