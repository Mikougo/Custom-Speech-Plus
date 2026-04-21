# 🎤 Custom Speech Plus

A powerful and flexible Discord bot that lets users create, edit, and manage custom commands with ease.
https://img.shields.io/badge/python-3.10-blue https://img.shields.io/badge/bot-discord-5865F2 https://img.shields.io/badge/made%20by-Mikougo-orange

---

## ✨ Features

* ➕ Add custom commands
* ✏️ Edit command triggers and responses
* ❌ Delete commands
* 📜 View all commands with `!cmds`
* 🔒 Admin-only command management
* 💾 Persistent storage using `commands.json`
* ⚡ Fast performance with in-memory caching
* 🧠 Smart editing system (change trigger, response, or both)

---

## 🧪 Example Usage

```text
!addcmd hello = yobru
!hello
→ yobru

!editcmd hello = hi - yobru = hey bro
!hi
→ hey bro

!delcmd hi

!cmds
```

---

## 🔐 Permissions

Only users with **Administrator** permission (or the server owner) can:

* Add commands
* Edit commands
* Delete commands

---

## 📁 Project Structure

```text
.
├── base.py
├── commands.json
├── requirements.txt
├── .gitignore
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

3. Set your bot token:

* Create a `.env` file (for local use only)

```env
DISCORD_TOKEN=your_bot_token_here
```

4. Run the bot:

```bash
python base.py
```

---

## 🚀 Deployment

This bot is ready to be deployed on platforms like:

* Railway
* Render
* VPS

Make sure to set your environment variable:

```text
DISCORD_TOKEN=your_bot_token_here
```

---

## ⚠️ Important Notes

* Do **NOT** share your bot token
* Do **NOT** upload your `.env` file
* Use environment variables in production

---

## 🧠 Future Ideas

* Per-server command storage
* Command cooldown system
* Embed responses
* Command permissions per role
* Web dashboard 👀

---

## 👨‍💻 Author

Made by **Mikougo**

---

## ⭐ Final Note

This started as a simple bot and evolved into a fully dynamic custom command system.
More features coming soon 🚀
