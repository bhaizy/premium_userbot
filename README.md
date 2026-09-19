 # 亗 Premium Telegram Userbot v2.0 亗

A high-performance, modular Telegram Userbot powered by **Pyrofork**, **PyTgCalls**, **Yuki API** (for YouTube audio extraction without IP blocks), and **MongoDB Atlas** with in-memory zero-latency caching.

<p align="center"><a href="https://dashboard.heroku.com/new?template=https://github.com/bhaizy/userbot"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-black?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>


---

## ⚡ Features

| Module | Commands | Description |
| :--- | :--- | :--- |
| **System** | .ping, .pong, .alive | Latency benchmarking in ms, uptime, CPU/RAM stats, and operational status. |
| **Voice Chat** | .vc join, .vc leave | Directly join or leave group voice calls. |
| **Music Streaming** | .play <song>, .stop | Stream audio into VC via PyTgCalls powered by Yuki API (zero YouTube IP bans). |
| **MP3 Downloader** | .song <name>, .music <name> | Search, download 320kbps MP3 with thumbnail, and send as Telegram audio. |
| **Raid & Spam** | .raid <count> <text> | Fire repeated messages with configurable delay. |
| **Reply Raid** | .rd / .replyraid, .rrd | Target a user; bot automatically counters their messages with roasts. |
| **Delay Config** | .delay <seconds> | Adjust global delay interval between operations (saved to MongoDB). |
| **Global Mute** | .gmute, .ungmute, .gmutelist | Silences user across all chats by instantly auto-deleting their messages. |
| **Media Saver** | .photo save, .save | Intercepts disappearing/self-destructing timer photos & saves them permanently to Saved Messages. |
| **History Tracker** | .history, .sg | Queries SangMata to view former display names and usernames. |
| **Help Menu** | .help | Interactive categorized command viewer. |

---

## 🚀 Quick Setup & Deployment

### Step 1: Clone or Copy Project
`ash
cd premium_userbot
`

### Step 2: Install Dependencies
`ash
pip install -r requirements.txt
`

### Step 3: Generate String Session
Run the interactive generator:
`ash
python generate_session.py
`
This will prompt for your API_ID, API_HASH, and Phone number, send a Telegram login code, and save your STRING_SESSION directly to .env.

### Step 4: Configure .env
Create a .env file (refer to .env.example):
`env
API_ID=12345678
API_HASH=your_api_hash
STRING_SESSION=your_generated_session_string
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MEOW_API_URL=https://music.yukiapi.site
MEOW_API_KEY=yuki_28d18045448fe0df857d31dfe08fcdef
PREFIXES=. !
DEFAULT_DELAY=0.5
`

### Step 5: Start the Bot
`ash
python main.py
`

---

## 🌐 Deploy Everywhere

### 1. Heroku
1. Create a new App on Heroku.
2. Connect your GitHub repository.
3. Add Config Vars in Settings (API_ID, API_HASH, STRING_SESSION, MONGO_URL, MEOW_API_KEY, etc.).
4. Deploy the main branch. The included Procfile (worker: python3 main.py) will automatically run the bot.

### 2. Koyeb / Render / Railway (Docker)
1. Select Dockerfile deployment.
2. The root Dockerfile will install fmpeg, libopus, Python dependencies, and run python3 main.py.
3. Add your environment variables in the dashboard.

### 3. VPS (Ubuntu / Debian)
`ash
bash deployments/start.sh
`
Or run with screen / 	mux:
`ash
tmux new -s userbot
python3 main.py
`

### 4. Android (Termux)
`ash
pkg install -y git
git clone <your-repo> userbot
cd userbot
bash deployments/termux_install.sh
`

---

## 🛡️ Important Safety Note
- Never share your STRING_SESSION or .env file with anyone.
- Avoid excessive raiding or spamming in public groups to keep your Telegram account safe from user reports.
