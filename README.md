# 🎤 Custom Speech Plus

![Python](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Bot](https://img.shields.io/badge/discord-bot-5865F2)
![Made by](https://img.shields.io/badge/made%20by-Mikougo-orange)

A customizable Discord bot that lets server staff create, edit, delete, and view custom text commands with persistent storage and admin protection.

---

## ✨ Features

* ➕ Add custom commands
* ✏️ Edit command triggers and responses
* ❌ Delete commands
* 📜 View all commands with `!cmds`
* 🔒 Only server owner and admins can manage commands
* 💾 Persistent storage using `commands.json`
* ⚡ In-memory caching for better performance
* 🧠 Supports multi-word triggers
* ⏱️ Cooldown protection for command listing and custom trigger spam

---

## 🧪 Example Usage

```text
!addcmd hello = yobru
!hello
→ yobru

!editcmd hello = hi -
!hi
→ yobru

!editcmd - yobru = hey bro
!hi
→ hey bro

!delcmd hi

!cmds
```

---

## 🔐 Permissions

Only users with **Administrator** permission or the **server owner** can:

* Add commands
* Edit commands
* Delete commands

Everyone can use the custom commands that already exist.

---

## 📁 Project Structure

```text
.
├── base.py
├── commands.json
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/Custom-Speech-Plus.git
cd Custom-Speech-Plus
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file for local testing:

```env
DISCORD_TOKEN=your_bot_token_here
```

4. Run the bot:

```bash
python base.py
```

---

## 🚀 Deployment

This bot can be deployed on platforms such as:

* Railway
* Render
* VPS

Set the environment variable:

```text
DISCORD_TOKEN=your_bot_token_here
```

---

## ⚠️ Important Notes

* Do **NOT** share your bot token
* Do **NOT** upload your `.env` file
* Enable **Message Content Intent** in the Discord Developer Portal
* Use `requirements.txt` when deploying

---

## 🧠 Future Ideas

* Per-server command storage
* Command categories
* Better logging for who edited what
* Embed-style responses
* Dashboard or web panel

---

## 👨‍💻 Author

Made by **Mikougo**

---

## ⭐ Final Note

Custom Speech Plus started as a simple idea and became a real deployed Discord bot with live users, admin protection, persistence, and performance improvements.
