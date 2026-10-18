# 🎓 Competitive Exam Quiz Telegram Bot

A feature-rich, multilingual Telegram Quiz Bot designed specifically for competitive exam aspirants preparing for **UPSC, SSC, OPSC, OSSSC, OSSC, NEET, JEE Main, JEE Advanced, OJEE, and Class 10th/11th/12th Board Exams**.

---

## 🌟 Key Features

1. **📚 Multi-Subject & NCERT Chapter Selection:**
   - **Biology:** Cell Structure, Genetics & Evolution, Human Physiology, Plant Physiology, Biotechnology, Ecology.
   - **Physics:** Mechanics, Thermodynamics, Optics & Waves, Electromagnetism, Modern Physics, Gravitation.
   - **Chemistry:** Chemical Bonding, Periodic Table, Organic Chemistry, Thermodynamics & Equilibrium, Solutions.
   - **Mathematics:** Number System & Arithmetic, Algebra, Trigonometry, Geometry, Calculus, Probability & Statistics.
   - **History:** Ancient India, Medieval India, Modern India & Freedom Struggle, Odisha History & Paika Bidroha, World History.
   - **Reasoning:** Series & Analogy, Coding-Decoding, Blood Relations, Syllogism, Direction Sense.
   - **English:** Grammar & Error Spotting, Vocabulary, Idioms & Phrases, Reading Comprehension.
   - **Odia (ଓଡ଼ିଆ ଭାଷା ଓ ବ୍ୟାକରଣ):** ସନ୍ଧି, ସମାସ, କୃଦନ୍ତ-ତଦ୍ଧିତ, ରୂଢ଼ି ଓ ଲୋକବାଣୀ, ଓଡ଼ିଆ ସାହିତ୍ୟ.
   - **Current Affairs:** National & International Events, Sports & Awards, Government Schemes, Defence & Science, Odisha Special.

2. **🌐 4 Languages Supported:**
   - 🇬🇧 English
   - 🇮🇳 हिन्दी (Hindi)
   - 🇮🇳 ଓଡ଼ିଆ (Odia)
   - 🇮🇳 Hinglish

3. **🎯 Exam Level Targeting:**
   - UPSC Civil Services
   - SSC CGL / CHSL / MTS / GD
   - OPSC (OAS, ASO)
   - OSSSC (PEO, RI, Amin)
   - OSSC
   - NEET (UG Medical)
   - JEE Main & Advanced (Engineering)
   - OJEE (Odisha JEE)
   - Class 10th (NCERT / BSE)
   - Class 11th & 12th (NCERT / CHSE)

4. **⚡ Interactive Quiz Engine:**
   - **Option Buttons (A, B, C, D)**: Tap to answer directly.
   - **💡 Get Hint Button**: Pops up a native modal with a guiding clue without revealing the answer.
   - **Instant Explanations**: Concise, conceptual breakdown shown after answering for both correct and incorrect choices.
   - **➡️ Next Question**: Seamlessly proceed to the next question.
   - **📊 View Result**: Check scorecard and accuracy percentage anytime!

5. **👑 Admin Panel:**
   - `/admin` - Overall stats and command manual.
   - `/stats` - Total registered candidates and quiz metrics.
   - `/broadcast <message>` - Send mass announcements to all registered users.
   - `/addq <pipe-delimited-data>` - Add new questions dynamically.

---

## 🚀 How to Run Locally (Windows)

1. **Get Bot Token**:
   - Open Telegram and message [@BotFather](https://t.me/BotFather).
   - Use `/newbot`, name your bot, and copy your API Token.

2. **Configure Token**:
   - Open `config.py` and replace `"YOUR_BOT_TOKEN_HERE"` with your token, OR set the environment variable:
     ```cmd
     set BOT_TOKEN=your_token_here
     ```

3. **Double Click to Run**:
   - Double-click `run.bat` in this folder. It will automatically install requirements, initialize the SQLite database with seed questions, and start polling!

---

## ☁️ How to Deploy 24/7 on Railway

1. Create a new repository on **GitHub** (e.g., `telegram-quiz-bot`).
2. Push all files inside this `quiz_bot` folder to GitHub.
3. Go to [Railway.app](https://railway.app/) and sign in with GitHub.
4. Click **New Project** -> **Deploy from GitHub repo** -> Select your repo.
5. In your Railway service settings:
   - Go to **Variables** tab.
   - Add variable: `BOT_TOKEN` = `your_telegram_bot_token`.
   - (Optional) Add variable: `ADMIN_IDS` = `your_numeric_telegram_user_id`.
6. Railway will automatically detect `railway.json` / `Procfile` and deploy your bot 24/7!

