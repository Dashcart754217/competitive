"""
Configuration module for Competitive Exam Quiz Telegram Bot.
Includes supported languages, subjects, NCERT topics, exam levels, and UI texts.
"""
import os

# Telegram Bot Token - load from environment or specify here
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Admin Telegram User IDs (integer Telegram chat IDs)
# Add your Telegram numeric user ID here (e.g., [123456789])
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

# Database File Path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_bot.db")

# Supported Languages
LANGUAGES = {
    "en": "🇬🇧 English",
    "hi": "🇮🇳 हिन्दी (Hindi)",
    "or": "🇮🇳 ଓଡ଼ିଆ (Odia)",
    "hinglish": "🇮🇳 Hinglish"
}

# Competitive Exam Levels
EXAM_LEVELS = [
    ("upsc", "🏛️ UPSC Civil Services"),
    ("ssc", "🎯 SSC CGL / CHSL / MTS"),
    ("opsc", "🏛️ OPSC (OAS / ASO)"),
    ("ossc", "📋 OSSC (Odisha Staff Selection)"),
    ("osssc", "📑 OSSSC (PEO / RI / Amin)"),
    ("neet", "🩺 NEET (UG Medical)"),
    ("jee_main", "⚡ JEE Main (Engineering)"),
    ("jee_adv", "🚀 JEE Advanced"),
    ("ojee", "🎓 OJEE (Odisha JEE)"),
    ("10th", "📚 Class 10th (NCERT / BSE)"),
    ("11th", "🔬 Class 11th (NCERT / CHSE)"),
    ("12th", "🎓 Class 12th (NCERT / CHSE)")
]

# Subjects and their NCERT / Syllabus Topics
SUBJECTS_DATA = {
    "biology": {
        "name": "🧬 Biology (ଜୀବବିଜ୍ଞାନ / जीवविज्ञान)",
        "topics": [
            ("bio_cell", "Cell: Structure & Function (କୋଷ)"),
            ("bio_genetics", "Genetics & Evolution (ବଂଶଗତି)"),
            ("bio_human_physio", "Human Physiology (ମାନବ ଶରୀର କ୍ରିୟା)"),
            ("bio_plant_physio", "Plant Physiology & Photosynthesis"),
            ("bio_biotech", "Biotechnology & Applications"),
            ("bio_ecology", "Ecology & Biodiversity (ପରିବେଶ)"),
            ("bio_all", "🌟 Complete Biology (Mixed)")
        ]
    },
    "physics": {
        "name": "⚡ Physics (ପଦାର୍ଥ ବିଜ୍ଞାନ / भौतिक विज्ञान)",
        "topics": [
            ("phy_mechanics", "Mechanics & Laws of Motion (ଗତି ଓ ବଳ)"),
            ("phy_thermo", "Thermodynamics & Heat (ତାପଗତିକୀ)"),
            ("phy_optics", "Optics & Wave Motion (ଆଲୋକ ଓ ତରଙ୍ଗ)"),
            ("phy_electromag", "Electricity & Magnetism (ବିଦ୍ୟୁତ)"),
            ("phy_modern", "Modern Physics & Nuclear Physics"),
            ("phy_gravitation", "Gravitation & Planetary Motion (ମାଧ୍ୟାକର୍ଷଣ)"),
            ("phy_all", "🌟 Complete Physics (Mixed)")
        ]
    },
    "chemistry": {
        "name": "🧪 Chemistry (ରସାୟନ ବିଜ୍ଞାନ / रसायन विज्ञान)",
        "topics": [
            ("chem_bonding", "Chemical Bonding & Molecular Structure"),
            ("chem_periodic", "Periodic Table & Classification (ଆବର୍ତ୍ତ ସାରଣୀ)"),
            ("chem_organic", "Organic Chemistry Basics & Hydrocarbons"),
            ("chem_thermo_eq", "Thermodynamics & Equilibrium"),
            ("chem_solutions", "Solutions, Electrochemistry & Kinetics"),
            ("chem_environmental", "Environmental Chemistry"),
            ("chem_all", "🌟 Complete Chemistry (Mixed)")
        ]
    },
    "math": {
        "name": "📐 Mathematics (ଗଣିତ / गणित)",
        "topics": [
            ("math_num_sys", "Number System & Arithmetic (ସଂଖ୍ୟା ପଦ୍ଧତି)"),
            ("math_algebra", "Algebra & Polynomials (ବୀଜଗଣିତ)"),
            ("math_trigo", "Trigonometry & Heights/Distances (ତ୍ରିକୋଣମିତି)"),
            ("math_geometry", "Geometry & Mensuration (କ୍ଷେତ୍ରମିତି)"),
            ("math_calculus", "Calculus & Coordinate Geometry"),
            ("math_stat_prob", "Probability & Statistics (ସମ୍ଭାବ୍ୟତା)"),
            ("math_all", "🌟 Complete Mathematics (Mixed)")
        ]
    },
    "history": {
        "name": "📜 History (ଇତିହାସ / इतिहास)",
        "topics": [
            ("hist_ancient", "Ancient India & Harappan Civilization"),
            ("hist_medieval", "Medieval India, Delhi Sultanate & Mughals"),
            ("hist_modern", "Modern India & Freedom Struggle (1857-1947)"),
            ("hist_odisha", "Odisha History & Paika Rebellion (ଓଡ଼ିଶା ଇତିହାସ)"),
            ("hist_world", "World History & Revolutions"),
            ("hist_all", "🌟 Complete History (Mixed)")
        ]
    },
    "reasoning": {
        "name": "🧩 Reasoning & Mental Ability (ତର୍କଶକ୍ତି / रीजनिंग)",
        "topics": [
            ("reas_analogy", "Number & Alphabet Series / Analogy"),
            ("reas_coding", "Coding - Decoding"),
            ("reas_blood", "Blood Relations (ରକ୍ତ ସମ୍ପର୍କ)"),
            ("reas_syllogism", "Syllogism & Logical Deduction"),
            ("reas_direction", "Direction Sense & Seating Arrangement"),
            ("reas_nonverbal", "Non-Verbal & Pattern Completion"),
            ("reas_all", "🌟 Complete Reasoning (Mixed)")
        ]
    },
    "english": {
        "name": "📖 English Language (ସାଧାରଣ ଇଂରାଜୀ / अंग्रेजी)",
        "topics": [
            ("eng_grammar", "Spotting Errors, Tenses & Prepositions"),
            ("eng_vocab", "Synonyms, Antonyms & One Word Substitution"),
            ("eng_idioms", "Idioms & Phrases"),
            ("eng_comprehension", "Reading Comprehension & Cloze Test"),
            ("eng_voice_narration", "Active/Passive Voice & Direct/Indirect"),
            ("eng_all", "🌟 Complete English (Mixed)")
        ]
    },
    "odia": {
        "name": "🏛️ Odia Language & Grammar (ଓଡ଼ିଆ ଭାଷା ଓ ବ୍ୟାକରଣ)",
        "topics": [
            ("odia_sandhi", "ସନ୍ଧି ଓ ସମାସ (Sandhi & Samasa)"),
            ("odia_krudanta", "କୃଦନ୍ତ, ତଦ୍ଧିତ ଓ କାରକ-ବିଭକ୍ତି"),
            ("odia_shabda", "ଶବ୍ଦ ସମ୍ଭାର, ରୂଢ଼ି ଓ ଲୋକବାଣୀ (Idioms & Proverbs)"),
            ("odia_sahitya", "ଓଡ଼ିଆ ସାହିତ୍ୟ ଓ ପ୍ରସିଦ୍ଧ ଲେଖକ (Literature & Authors)"),
            ("odia_shuddha", "ବାକ୍ୟ ଶୁଦ୍ଧି ଓ ବର୍ଣ୍ଣାଶୁଦ୍ଧି (Sentence Correction)"),
            ("odia_all", "🌟 ସମ୍ପୂର୍ଣ୍ଣ ଓଡ଼ିଆ (Mixed Odia Practice)")
        ]
    },
    "current_affairs": {
        "name": "🌍 Current Affairs & GK (ସାମ୍ପ୍ରତିକ ଘଟଣାବଳୀ / करेंट अफेयर्स)",
        "topics": [
            ("ca_national", "National & International Events"),
            ("ca_sports", "Sports, Awards & Honors (ଖେଳ ଓ ପୁରସ୍କାର)"),
            ("ca_schemes", "Government Schemes & Policies (ଯୋଜନା)"),
            ("ca_science_def", "Science, Tech & Defence (ପ୍ରତିରକ୍ଷା)"),
            ("ca_odisha", "Odisha Special Current Affairs (ଓଡ଼ିଶା ସ୍ପେଶାଲ)"),
            ("ca_all", "🌟 Complete Current Affairs (Mixed)")
        ]
    }
}

# Localized UI Strings
UI_STRINGS = {
    "en": {
        "welcome": (
            "👋 **Welcome to Competitive Exam Quiz Bot!**\n\n"
            "Prepare for **UPSC, SSC, OPSC, OSSSC, NEET, JEE, OJEE & Board Exams** with high-yield questions!\n\n"
            "✨ **Features:**\n"
            "• NCERT Topic & Subject Selection\n"
            "• Multi-lingual (English, Hindi, Odia, Hinglish)\n"
            "• Instant short explanations for every question\n"
            "• 💡 Hints to guide you without revealing answers\n"
            "• Live Scorecard & Performance Analytics\n\n"
            "👇 **Please select your preferred language below:**"
        ),
        "menu_title": "🎯 **Main Dashboard**\nChoose an action below to begin your prep:",
        "btn_start_quiz": "🚀 Start Quiz",
        "btn_my_stats": "📊 My Performance",
        "btn_change_lang": "🌐 Change Language",
        "btn_help": "ℹ️ Help & Guide",
        "select_subject": "📚 **Step 1/3: Choose Subject**\nSelect the subject you want to practice:",
        "select_topic": "📑 **Step 2/3: Choose NCERT / Syllabus Topic**\nSubject: **{subject}**",
        "select_level": "🎯 **Step 3/3: Choose Target Exam Level**\nSelect your target examination:",
        "quiz_starting": (
            "🎯 **Quiz Initialized!**\n\n"
            "• **Subject:** {subject}\n"
            "• **Topic:** {topic}\n"
            "• **Level:** {level}\n"
            "• **Total Questions:** {total}\n\n"
            "Tap any option below to answer. Good luck! 🚀"
        ),
        "question_card": (
            "📌 **Question {q_num}/{total}** | *{level}*\n"
            "🏷️ **Topic:** {topic}\n\n"
            "{question}\n\n"
            "A) {opt_a}\n"
            "B) {opt_b}\n"
            "C) {opt_c}\n"
            "D) {opt_d}"
        ),
        "btn_hint": "💡 Get Hint",
        "btn_next": "➡️ Next Question",
        "btn_view_result": "📊 View Result",
        "btn_retry": "🔄 New Quiz",
        "btn_home": "🏠 Main Menu",
        "correct_answer": "✅ **Correct! Excellent job!** 🎉",
        "wrong_answer": "❌ **Incorrect!** The correct answer is **Option {correct}**.",
        "explanation_header": "\n\n💡 **Explanation:**\n{explanation}",
        "hint_text": "💡 **Hint:**\n{hint}",
        "already_answered": "⚠️ You have already answered this question! Tap 'Next Question' or 'View Result'.",
        "result_card": (
            "🏆 **QUIZ COMPLETED!**\n\n"
            "👤 **Candidate:** {name}\n"
            "📚 **Subject:** {subject}\n"
            "🎯 **Exam Level:** {level}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ **Correct Answers:** {correct}\n"
            "❌ **Wrong Answers:** {wrong}\n"
            "📊 **Total Attempted:** {attempted} / {total}\n"
            "📈 **Accuracy:** {accuracy}%\n"
            "⭐ **Grade:** {grade}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "{feedback}"
        ),
        "stats_card": (
            "📊 **Your Learning Analytics**\n\n"
            "👤 **User:** {name}\n"
            "🎯 **Total Quizzes Taken:** {total_quizzes}\n"
            "📝 **Total Questions Attempted:** {total_attempted}\n"
            "✅ **Total Correct Answers:** {total_correct}\n"
            "📈 **Overall Accuracy:** {accuracy}%\n\n"
            "Keep practicing daily to boost your rank! 🚀"
        ),
        "help_text": (
            "ℹ️ **How to Use This Bot:**\n\n"
            "1. Use /start anytime to reset or return to the main menu.\n"
            "2. Select your Language (English, Hindi, Odia, Hinglish).\n"
            "3. Choose Subject (Biology, Physics, Chemistry, Math, Odia, English, etc.).\n"
            "4. Choose specific NCERT topic or chapter.\n"
            "5. Pick your exam target (UPSC, SSC, OPSC, OSSSC, NEET, JEE, etc.).\n"
            "6. Answer questions using the inline buttons.\n"
            "7. Click **💡 Get Hint** if you're stuck.\n"
            "8. Read the instant short explanation after every answer!\n"
            "9. Click **📊 View Result** anytime to see your detailed scorecard."
        ),
        "admin_access_denied": "🚫 You are not authorized to use admin commands.",
        "admin_panel": (
            "👑 **Admin Control Panel**\n\n"
            "• **Total Registered Users:** {users_count}\n"
            "• **Total Question Bank:** {questions_count}\n"
            "• **Total Quizzes Completed:** {quizzes_count}\n\n"
            "**Admin Commands:**\n"
            "• `/broadcast <message>` - Send announcement to all users\n"
            "• `/stats` - View detailed system stats\n"
            "• `/addq` - Add new question interactively"
        )
    },
    "hi": {
        "welcome": (
            "👋 **प्रतियोगी परीक्षा क्विज बॉट में आपका स्वागत है!**\n\n"
            "**UPSC, SSC, OPSC, OSSSC, NEET, JEE, OJEE और 10वीं/12वीं बोर्ड** की तैयारी बेहतरीन प्रश्नों के साथ करें!\n\n"
            "✨ **विशेषताएं:**\n"
            "• NCERT विषय और टॉपिक अनुसार क्विज\n"
            "• बहुभाषी (हिन्दी, English, ଓଡ଼ିଆ, Hinglish)\n"
            "• प्रत्येक प्रश्न के लिए तुरंत संक्षिप्त व्याख्या (Explanation)\n"
            "• 💡 हिंट (Hint) की सुविधा बिना उत्तर बताए\n"
            "• लाइव रिजल्ट कार्ड और परफॉर्मेंस रिपोर्ट\n\n"
            "👇 **कृपया अपनी पसंदीदा भाषा चुनें:**"
        ),
        "menu_title": "🎯 **मुख्य डैशबोर्ड**\nअभ्यास शुरू करने के लिए नीचे एक विकल्प चुनें:",
        "btn_start_quiz": "🚀 क्विज शुरू करें",
        "btn_my_stats": "📊 मेरी रिपोर्ट",
        "btn_change_lang": "🌐 भाषा बदलें",
        "btn_help": "ℹ️ सहायता एवं निर्देश",
        "select_subject": "📚 **चरण 1/3: विषय चुनें**\nआप किस विषय का अभ्यास करना चाहते हैं?",
        "select_topic": "📑 **चरण 2/3: NCERT टॉपिक चुनें**\nविषय: **{subject}**",
        "select_level": "🎯 **चरण 3/3: परीक्षा स्तर चुनें**\nअपनी लक्षित परीक्षा का चयन करें:",
        "quiz_starting": (
            "🎯 **क्विज प्रारंभ!**\n\n"
            "• **विषय:** {subject}\n"
            "• **टॉपिक:** {topic}\n"
            "• **स्तर:** {level}\n"
            "• **कुल प्रश्न:** {total}\n\n"
            "उत्तर देने के लिए नीचे दिए गए बटन पर टैप करें। शुभकामनाएँ! 🚀"
        ),
        "question_card": (
            "📌 **प्रश्न {q_num}/{total}** | *{level}*\n"
            "🏷️ **टॉपिक:** {topic}\n\n"
            "{question}\n\n"
            "A) {opt_a}\n"
            "B) {opt_b}\n"
            "C) {opt_c}\n"
            "D) {opt_d}"
        ),
        "btn_hint": "💡 हिंट देखें",
        "btn_next": "➡️ अगला प्रश्न",
        "btn_view_result": "📊 परिणाम देखें",
        "btn_retry": "🔄 नया क्विज",
        "btn_home": "🏠 मुख्य मेनू",
        "correct_answer": "✅ **बिल्कुल सही उत्तर! बहुत बढ़िया!** 🎉",
        "wrong_answer": "❌ **गलत उत्तर!** सही विकल्प **{correct}** है।",
        "explanation_header": "\n\n💡 **संक्षिप्त व्याख्या (Explanation):**\n{explanation}",
        "hint_text": "💡 **हिंट (संकेत):**\n{hint}",
        "already_answered": "⚠️ आप इस प्रश्न का उत्तर पहले ही दे चुके हैं! 'अगला प्रश्न' या 'परिणाम देखें' पर क्लिक करें।",
        "result_card": (
            "🏆 **क्विज संपन्न!**\n\n"
            "👤 **परीक्षार्थी:** {name}\n"
            "📚 **विषय:** {subject}\n"
            "🎯 **स्तर:** {level}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ **सही उत्तर:** {correct}\n"
            "❌ **गलत उत्तर:** {wrong}\n"
            "📊 **हल किए गए प्रश्न:** {attempted} / {total}\n"
            "📈 **सटीकता (Accuracy):** {accuracy}%\n"
            "⭐ **ग्रेड:** {grade}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "{feedback}"
        ),
        "stats_card": (
            "📊 **आपकी अध्ययन रिपोर्ट**\n\n"
            "👤 **नाम:** {name}\n"
            "🎯 **कुल क्विज दिए:** {total_quizzes}\n"
            "📝 **कुल हल प्रश्न:** {total_attempted}\n"
            "✅ **कुल सही उत्तर:** {total_correct}\n"
            "📈 **औसत सटीकता:** {accuracy}%\n\n"
            "रोजाना अभ्यास करें और अपनी रैंक बेहतर बनाएं! 🚀"
        ),
        "help_text": (
            "ℹ️ **इस बॉट का उपयोग कैसे करें:**\n\n"
            "1. किसी भी समय /start दबाकर मुख्य मेनू पर आएं।\n"
            "2. अपनी भाषा (हिन्दी, English, ଓଡ଼ିଆ, Hinglish) चुनें।\n"
            "3. विषय (Biology, Physics, Chemistry, Math, History आदि) चुनें।\n"
            "4. NCERT टॉपिक चुनें और अपना परीक्षा स्तर चुनें।\n"
            "5. प्रश्नों के उत्तर बटन दबाकर दें।\n"
            "6. जरूरत पड़ने पर **💡 हिंट देखें** बटन दबाएं।\n"
            "7. प्रत्येक प्रश्न के बाद संक्षिप्त व्याख्या पढ़ें।\n"
            "8. किसी भी समय **📊 परिणाम देखें** पर क्लिक करके अपना स्कोरकार्ड देख सकते हैं।"
        ),
        "admin_access_denied": "🚫 आपको एडमिन कमांड का उपयोग करने की अनुमति नहीं है।",
        "admin_panel": (
            "👑 **एडमिन कंट्रोल पैनल**\n\n"
            "• **कुल पंजीकृत उपयोगकर्ता:** {users_count}\n"
            "• **कुल प्रश्न बैंक:** {questions_count}\n"
            "• **कुल पूर्ण क्विज:** {quizzes_count}\n\n"
            "**एडमिन कमांड्स:**\n"
            "• `/broadcast <संदेश>` - सभी उपयोगकर्ताओं को संदेश भेजें\n"
            "• `/stats` - विस्तृत आंकड़े देखें"
        )
    },
    "or": {
        "welcome": (
            "👋 **ପ୍ରତିଯୋଗିତାମୂଳକ ପରୀକ୍ଷା କୁଇଜ୍ ବଟ୍‌କୁ ସ୍ୱାଗତ!**\n\n"
            "**UPSC, SSC, OPSC (OAS/ASO), OSSSC (PEO/RI), OSSC, NEET, JEE, OJEE ଏବଂ 10ମ/12ଶ ଶ୍ରେଣୀ** ପରୀକ୍ଷା ପାଇଁ ସର୍ବୋତ୍ତମ ପ୍ରଶ୍ନୋତ୍ତର ଅଭ୍ୟାସ କରନ୍ତୁ!\n\n"
            "✨ **ମୁଖ୍ୟ ବୈଶିଷ୍ଟ୍ୟ:**\n"
            "• NCERT ବିଷୟ ଓ ଅଧ୍ୟାୟ ଭିତ୍ତିକ କୁଇଜ୍\n"
            "• ଓଡ଼ିଆ, ଇଂରାଜୀ, ହିନ୍ଦୀ ଓ ହିଙ୍ଗଲିଶ୍ ଭାଷା ସମର୍ଥନ\n"
            "• ପ୍ରତ୍ୟେକ ପ୍ରଶ୍ନର ସଂକ୍ଷିପ୍ତ ସଠିକ୍ ବ୍ୟାଖ୍ୟା (Explanation)\n"
            "• 💡 ସଂକେତ (Hint) ସୁବିଧା\n"
            "• ତତ୍କାଳ ଫଳାଫଳ ଓ ସ୍କୋରକାର୍ଡ\n\n"
            "👇 **ଦୟାକରି ତଳେ ଆପଣଙ୍କ ପସନ୍ଦର ଭାଷା ବାଛନ୍ତୁ:**"
        ),
        "menu_title": "🎯 **ମୁଖ୍ୟ ଡ୍ୟାସବୋର୍ଡ**\nଅଭ୍ୟାସ ଆରମ୍ଭ କରିବା ପାଇଁ ତଳୁ ଗୋଟିଏ ବିକଳ୍ପ ଚୟନ କରନ୍ତୁ:",
        "btn_start_quiz": "🚀 କୁଇଜ୍ ଆରମ୍ଭ କରନ୍ତୁ",
        "btn_my_stats": "📊 ମୋର ପ୍ରଦର୍ଶନ ରିପୋର୍ଟ",
        "btn_change_lang": "🌐 ଭାଷା ପରିବର୍ତ୍ତନ କରନ୍ତୁ",
        "btn_help": "ℹ️ ସହାୟତା ଓ ନିର୍ଦ୍ଦେଶାବଳୀ",
        "select_subject": "📚 **ପଦକ୍ଷେପ ୧/୩: ବିଷୟ ବାଛନ୍ତୁ**\nଆପଣ କେଉଁ ବିଷୟ ଅଭ୍ୟାସ କରିବାକୁ ଚାହାଁନ୍ତି?",
        "select_topic": "📑 **ପଦକ୍ଷେପ ୨/୩: NCERT ଅଧ୍ୟାୟ / ଟପିକ୍ ବାଛନ୍ତୁ**\nବିଷୟ: **{subject}**",
        "select_level": "🎯 **ପଦକ୍ଷେପ ୩/୩: ପରୀକ୍ଷା ସ୍ତର ବାଛନ୍ତୁ**\nଆପଣଙ୍କ ଟାର୍ଗେଟ ପରୀକ୍ଷା ଚୟନ କରନ୍ତୁ:",
        "quiz_starting": (
            "🎯 **କୁଇଜ୍ ଆରମ୍ଭ ହେଲା!**\n\n"
            "• **ବିଷୟ:** {subject}\n"
            "• **ଅଧ୍ୟାୟ:** {topic}\n"
            "• **ପରୀକ୍ଷା ସ୍ତର:** {level}\n"
            "• **ମୋଟ ପ୍ରଶ୍ନ:** {total}\n\n"
            "ଉତ୍ତର ଦେବା ପାଇଁ ତଳେ ଥିବା ବିକଳ୍ପ ବଟନ୍‌କୁ ଦବାନ୍ତୁ। ଶୁଭକାମନା! 🚀"
        ),
        "question_card": (
            "📌 **ପ୍ରଶ୍ନ {q_num}/{total}** | *{level}*\n"
            "🏷️ **ଅଧ୍ୟାୟ:** {topic}\n\n"
            "{question}\n\n"
            "A) {opt_a}\n"
            "B) {opt_b}\n"
            "C) {opt_c}\n"
            "D) {opt_d}"
        ),
        "btn_hint": "💡 ହିଣ୍ଟ (ସଂକେତ) ଦେଖନ୍ତୁ",
        "btn_next": "➡️ ପରବର୍ତ୍ତୀ ପ୍ରଶ୍ନ",
        "btn_view_result": "📊 ଫଳାଫଳ ଦେଖନ୍ତୁ",
        "btn_retry": "🔄 ନୂତନ କୁଇଜ୍",
        "btn_home": "🏠 ମୁଖ୍ୟ ମେନୁ",
        "correct_answer": "✅ **ଅତି ଉତ୍ତମ! ସଠିକ୍ ଉତ୍ତର!** 🎉",
        "wrong_answer": "❌ **ଭୁଲ ଉତ୍ତର!** ସଠିକ୍ ବିକଳ୍ପ ହେଉଛି **{correct}**।",
        "explanation_header": "\n\n💡 **ସଂକ୍ଷିପ୍ତ ବ୍ୟାଖ୍ୟା (Explanation):**\n{explanation}",
        "hint_text": "💡 **ସଂକେତ (Hint):**\n{hint}",
        "already_answered": "⚠️ ଆପଣ ଏହି ପ୍ରଶ୍ନର ଉତ୍ତର ପୂର୍ବରୁ ଦେଇସାରିଛନ୍ତି! 'ପରବର୍ତ୍ତୀ ପ୍ରଶ୍ନ' କିମ୍ବା 'ଫଳାଫଳ ଦେଖନ୍ତୁ' ଦବାନ୍ତୁ।",
        "result_card": (
            "🏆 **କୁଇଜ୍ ସମାପ୍ତ!**\n\n"
            "👤 **ପରୀକ୍ଷାର୍ଥୀ:** {name}\n"
            "📚 **ବିଷୟ:** {subject}\n"
            "🎯 **ସ୍ତର:** {level}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ **ସଠିକ୍ ଉତ୍ତର:** {correct}\n"
            "❌ **ଭୁଲ ଉତ୍ତର:** {wrong}\n"
            "📊 **ଅଭ୍ୟାସ କରିଥିବା ପ୍ରଶ୍ନ:** {attempted} / {total}\n"
            "📈 **ସଠିକତା (Accuracy):** {accuracy}%\n"
            "⭐ **ଗ୍ରେଡ୍:** {grade}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "{feedback}"
        ),
        "stats_card": (
            "📊 **ଆପଣଙ୍କ ପ୍ରଦର୍ଶନ ରିପୋର୍ଟ**\n\n"
            "👤 **ନାମ:** {name}\n"
            "🎯 **ସମୁଦାୟ କୁଇଜ୍:** {total_quizzes}\n"
            "📝 **ସମୁଦାୟ ଚେଷ୍ଟା କରାଯାଇଥିବା ପ୍ରଶ୍ନ:** {total_attempted}\n"
            "✅ **ମୋଟ ସଠିକ୍ ଉତ୍ତର:** {total_correct}\n"
            "📈 **ମୋଟ ସଠିକତା ହାର:** {accuracy}%\n\n"
            "ପ୍ରତିଦିନ ଅଭ୍ୟାସ ଜାରି ରଖନ୍ତୁ ଓ ସଫଳତା ହାସଲ କରନ୍ତୁ! 🚀"
        ),
        "help_text": (
            "ℹ️ **ଏହି ବଟ୍ କିପରି ବ୍ୟବହାର କରିବେ:**\n\n"
            "1. ଯେକୌଣସି ସମୟରେ ମୁଖ୍ୟ ମେନୁକୁ ଫେରିବା ପାଇଁ /start ଟାଇପ୍ କରନ୍ତୁ।\n"
            "2. ନିଜ ଭାଷା (ଓଡ଼ିଆ, English, Hindi, Hinglish) ଚୟନ କରନ୍ତୁ।\n"
            "3. ବିଷୟ (Biology, Physics, Chemistry, Math, History, Odia ଇତ୍ୟାଦି) ବାଛନ୍ତୁ।\n"
            "4. NCERT ଅଧ୍ୟାୟ ଏବଂ ପରୀକ୍ଷା ସ୍ତର (UPSC, OPSC, OSSSC, SSC, NEET, JEE) ବାଛନ୍ତୁ।\n"
            "5. ସ୍କ୍ରିନରେ ଥିବା ବଟନ୍ ଦବାଇ ଉତ୍ତର ଦିଅନ୍ତୁ।\n"
            "6. ପ୍ରଶ୍ନ କଠିନ ଲାଗିଲେ **💡 ହିଣ୍ଟ** ଦେଖନ୍ତୁ।\n"
            "7. ପ୍ରତ୍ୟେକ ଉତ୍ତର ପରେ ତଳେ ସଂକ୍ଷିପ୍ତ ବ୍ୟାଖ୍ୟା ପଢନ୍ତୁ।\n"
            "8. ଯେକୌଣସି ସମୟରେ **📊 ଫଳାଫଳ ଦେଖନ୍ତୁ** ବଟନ୍ ଚୟନ କରି ସ୍କୋରକାର୍ଡ ଦେଖିପାରିବେ।"
        ),
        "admin_access_denied": "🚫 ଆପଣଙ୍କ ପାଖରେ ଆଡମିନ୍ ଅଧିକାର ନାହିଁ।",
        "admin_panel": (
            "👑 **ଆଡମିନ୍ କଣ୍ଟ୍ରୋଲ ପ୍ୟାନେଲ**\n\n"
            "• **ମୋଟ ବ୍ୟବହାରକାରୀ:** {users_count}\n"
            "• **ମୋଟ ପ୍ରଶ୍ନ ସଂଖ୍ୟା:** {questions_count}\n"
            "• **ମୋଟ ସମାପ୍ତ କୁଇଜ୍:** {quizzes_count}\n\n"
            "**ଆଡମିନ୍ କମାଣ୍ଡ:**\n"
            "• `/broadcast <ସନ୍ଦେଶ>` - ସମସ୍ତ ୟୁଜରଙ୍କୁ ମେସେଜ୍ ପଠାନ୍ତୁ\n"
            "• `/stats` - ସମ୍ପୂର୍ଣ୍ଣ ସିଷ୍ଟମ ରିପୋର୍ଟ"
        )
    },
    "hinglish": {
        "welcome": (
            "👋 **Welcome to Competitive Exam Quiz Bot!**\n\n"
            "**UPSC, SSC, OPSC, OSSSC, NEET, JEE, OJEE aur Board Exams** ki top quality preparation karo!\n\n"
            "✨ **Features:**\n"
            "• NCERT Topic & Subject wise Practice\n"
            "• 4 Languages (English, Hindi, Odia, Hinglish)\n"
            "• Har question ka instant short Explanation\n"
            "• 💡 Hint option bina answer reveal kiye\n"
            "• Instant Scorecard & Performance Analytics\n\n"
            "👇 **Neeche apni language select karo:**"
        ),
        "menu_title": "🎯 **Main Dashboard**\nPractice start karne ke liye ek option choose karo:",
        "btn_start_quiz": "🚀 Quiz Start Karo",
        "btn_my_stats": "📊 Meri Performance",
        "btn_change_lang": "🌐 Language Badlo",
        "btn_help": "ℹ️ Help & Guide",
        "select_subject": "📚 **Step 1/3: Subject Choose Karo**\nAap kis subject ka practice karna chahte ho?",
        "select_topic": "📑 **Step 2/3: NCERT / Syllabus Topic Choose Karo**\nSubject: **{subject}**",
        "select_level": "🎯 **Step 3/3: Exam Level Choose Karo**\nApna target exam select karo:",
        "quiz_starting": (
            "🎯 **Quiz Shuru Ho Gaya!**\n\n"
            "• **Subject:** {subject}\n"
            "• **Topic:** {topic}\n"
            "• **Level:** {level}\n"
            "• **Total Questions:** {total}\n\n"
            "Answer dene ke liye options par tap karo. All the best! 🚀"
        ),
        "question_card": (
            "📌 **Question {q_num}/{total}** | *{level}*\n"
            "🏷️ **Topic:** {topic}\n\n"
            "{question}\n\n"
            "A) {opt_a}\n"
            "B) {opt_b}\n"
            "C) {opt_c}\n"
            "D) {opt_d}"
        ),
        "btn_hint": "💡 Hint Dekho",
        "btn_next": "➡️ Agla Question",
        "btn_view_result": "📊 Result Dekho",
        "btn_retry": "🔄 Naya Quiz",
        "btn_home": "🏠 Main Menu",
        "correct_answer": "✅ **Ekdum Sahi Jawab! Bahut badhiya!** 🎉",
        "wrong_answer": "❌ **Galat Jawab!** Sahi option **Option {correct}** hai.",
        "explanation_header": "\n\n💡 **Explanation:**\n{explanation}",
        "hint_text": "💡 **Hint:**\n{hint}",
        "already_answered": "⚠️ Aapne is question ka answer pehle hi de diya hai! 'Agla Question' ya 'Result Dekho' dabayein.",
        "result_card": (
            "🏆 **QUIZ FINISHED!**\n\n"
            "👤 **Student:** {name}\n"
            "📚 **Subject:** {subject}\n"
            "🎯 **Exam Level:** {level}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ **Correct Answers:** {correct}\n"
            "❌ **Wrong Answers:** {wrong}\n"
            "📊 **Total Attempted:** {attempted} / {total}\n"
            "📈 **Accuracy:** {accuracy}%\n"
            "⭐ **Grade:** {grade}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "{feedback}"
        ),
        "stats_card": (
            "📊 **Aapki Performance Report**\n\n"
            "👤 **User:** {name}\n"
            "🎯 **Total Quizzes Diye:** {total_quizzes}\n"
            "📝 **Total Attempted Questions:** {total_attempted}\n"
            "✅ **Total Sahi Jawab:** {total_correct}\n"
            "📈 **Overall Accuracy:** {accuracy}%\n\n"
            "Daily practice karte raho exam clear karne ke liye! 🚀"
        ),
        "help_text": (
            "ℹ️ **Bot kaise use karein:**\n\n"
            "1. Kabhi bhi /start send karke main menu me aa sakte ho.\n"
            "2. Apni language (English, Hindi, Odia, Hinglish) select karo.\n"
            "3. Subject choose karo (Bio, Physics, Chemistry, Math, Odia, etc.).\n"
            "4. NCERT topic & target exam level choose karo.\n"
            "5. Buttons dabakar answer select karo.\n"
            "6. Question tough lage toh **💡 Hint Dekho** click karo.\n"
            "7. Har answer ke baad short explanation zaroor padho.\n"
            "8. Kabhi bhi **📊 Result Dekho** dabakar apna scorecard check kar sakte ho."
        ),
        "admin_access_denied": "🚫 Aapko admin access nahi hai.",
        "admin_panel": (
            "👑 **Admin Control Panel**\n\n"
            "• **Total Users:** {users_count}\n"
            "• **Total Questions:** {questions_count}\n"
            "• **Total Quizzes Finished:** {quizzes_count}\n\n"
            "**Admin Commands:**\n"
            "• `/broadcast <message>` - Sabhi users ko notification bhejo\n"
            "• `/stats` - Total bot analytics check karo"
        )
    }
}

