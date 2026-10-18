import os
import sys

# Ensure local module directory has highest priority in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from config import BOT_TOKEN, LANGUAGES, SUBJECTS_DATA, EXAM_LEVELS, UI_STRINGS
from database import (
    init_db,
    get_or_create_user,
    set_user_language,
    get_user_language,
    get_questions_for_quiz,
    get_question_by_id,
    start_quiz_session,
    get_session,
    record_answer,
    next_question_index,
    finish_quiz_session,
    get_user_stats
)
from seed_data import seed_database_if_empty
from admin import (
    admin_panel_handler,
    admin_stats_handler,
    admin_broadcast_handler,
    admin_add_question_handler
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_text(user_id: int, key: str) -> str:
    """Helper to get localized string for user."""
    lang = get_user_language(user_id)
    return UI_STRINGS.get(lang, UI_STRINGS["en"]).get(key, UI_STRINGS["en"].get(key, ""))

# ==========================================
# COMMAND HANDLERS
# ==========================================

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Welcomes user and offers language selection."""
    user = update.effective_user
    if not user:
        return
        
    get_or_create_user(user.id, user.username, user.first_name)
    
    keyboard = []
    # 2 languages per row
    row = []
    for code, label in LANGUAGES.items():
        row.append(InlineKeyboardButton(label, callback_data=f"lang:{code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    welcome_text = (
        "👋 **Welcome to the Competitive Exam Quiz Bot!**\n"
        "**ପ୍ରତିଯୋଗିତାମୂଳକ ପରୀକ୍ଷା କୁଇଜ୍ ବଟ୍‌କୁ ସ୍ୱାଗତ!**\n"
        "**प्रतियोगी परीक्षा क्विज बॉट में आपका स्वागत है!**\n\n"
        "🎯 Prepare for **UPSC, SSC, OPSC, OSSSC, NEET, JEE, OJEE & Board Exams**.\n\n"
        "🌐 **Please choose your language / ଭାଷା ଚୟନ କରନ୍ତୁ / भाषा चुनें:**"
    )
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Display the main dashboard menu with localized options."""
    lang = get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    keyboard = [
        [InlineKeyboardButton(strings["btn_start_quiz"], callback_data="menu:start_quiz")],
        [
            InlineKeyboardButton(strings["btn_my_stats"], callback_data="menu:my_stats"),
            InlineKeyboardButton(strings["btn_change_lang"], callback_data="menu:change_lang")
        ],
        [InlineKeyboardButton(strings["btn_help"], callback_data="menu:help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(strings["menu_title"], reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(strings["menu_title"], reply_markup=reply_markup, parse_mode="Markdown")

# ==========================================
# QUIZ SELECTION FLOW
# ==========================================

async def show_subjects_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Step 1: Display subject selection menu."""
    lang = get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    keyboard = []
    for sub_key, data in SUBJECTS_DATA.items():
        keyboard.append([InlineKeyboardButton(data["name"], callback_data=f"sub:{sub_key}")])
        
    keyboard.append([InlineKeyboardButton(strings["btn_home"], callback_data="menu:home")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(strings["select_subject"], reply_markup=reply_markup, parse_mode="Markdown")

async def show_topics_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, subject_key: str):
    """Step 2: Display NCERT topics menu for chosen subject."""
    lang = get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])
    context.user_data["selected_subject"] = subject_key
    
    sub_data = SUBJECTS_DATA.get(subject_key)
    if not sub_data:
        await show_subjects_menu(update, context, user_id)
        return

    keyboard = []
    for top_key, top_name in sub_data["topics"]:
        keyboard.append([InlineKeyboardButton(top_name, callback_data=f"top:{top_key}")])
        
    keyboard.append([InlineKeyboardButton("🔙 Back to Subjects", callback_data="menu:start_quiz")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    title = strings["select_topic"].format(subject=sub_data["name"])
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(title, reply_markup=reply_markup, parse_mode="Markdown")

async def show_levels_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, topic_key: str):
    """Step 3: Display competitive exam level picker."""
    lang = get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])
    context.user_data["selected_topic"] = topic_key
    subject_key = context.user_data.get("selected_subject", "biology")

    keyboard = []
    row = []
    for lvl_key, lvl_label in EXAM_LEVELS:
        row.append(InlineKeyboardButton(lvl_label, callback_data=f"lvl:{lvl_key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("🔙 Back to Topics", callback_data=f"sub:{subject_key}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(strings["select_level"], reply_markup=reply_markup, parse_mode="Markdown")

# ==========================================
# QUIZ ENGINE & QUESTION DISPLAY
# ==========================================

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, exam_level: str):
    """Fetch questions and launch the active quiz."""
    context.user_data["selected_level"] = exam_level
    subject = context.user_data.get("selected_subject", "biology")
    topic = context.user_data.get("selected_topic", "bio_cell")
    lang = get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    # Fetch question IDs
    q_ids = get_questions_for_quiz(subject, topic, exam_level, lang, limit=10)
    if not q_ids:
        # Retry with English if Odia/Hindi had no specific questions for that exact topic
        q_ids = get_questions_for_quiz(subject, topic, exam_level, "en", limit=10)

    if not q_ids:
        if update.callback_query:
            await update.callback_query.answer("⚠️ No questions found for this combination! Try another topic.", show_alert=True)
            await show_subjects_menu(update, context, user_id)
        return

    # Start session in database
    start_quiz_session(user_id, subject, topic, exam_level, lang, q_ids)
    
    # Display the first question
    await display_current_question(update, context, user_id)

async def display_current_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Render the current question card with interactive answer and navigation buttons."""
    session = get_session(user_id)
    if not session:
        await show_main_menu(update, context, user_id)
        return

    q_ids = session["question_ids"]
    curr_idx = session["current_idx"]
    lang = session.get("language") or get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    if curr_idx >= len(q_ids):
        # All questions finished
        await finish_and_show_results(update, context, user_id)
        return

    q_id = q_ids[curr_idx]
    q_data = get_question_by_id(q_id)
    if not q_data:
        await finish_and_show_results(update, context, user_id)
        return

    # Prepare Question Text
    level_label = dict(EXAM_LEVELS).get(session["exam_level"], session["exam_level"].upper())
    card_text = strings["question_card"].format(
        q_num=curr_idx + 1,
        total=len(q_ids),
        level=level_label,
        topic=q_data["topic"].replace("_", " ").title(),
        question=q_data["question_text"],
        opt_a=q_data["opt_a"],
        opt_b=q_data["opt_b"],
        opt_c=q_data["opt_c"],
        opt_d=q_data["opt_d"]
    )

    # Option buttons
    keyboard = [
        [
            InlineKeyboardButton("A", callback_data="ans:A"),
            InlineKeyboardButton("B", callback_data="ans:B"),
            InlineKeyboardButton("C", callback_data="ans:C"),
            InlineKeyboardButton("D", callback_data="ans:D")
        ],
        [
            InlineKeyboardButton(strings["btn_hint"], callback_data="quiz:hint")
        ],
        [
            InlineKeyboardButton(strings["btn_view_result"], callback_data="quiz:view_result")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(card_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(card_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_answer_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, chosen_opt: str):
    """Evaluate selected option, show instant feedback and explanation, and provide Next/Result buttons."""
    session = get_session(user_id)
    if not session:
        await show_main_menu(update, context, user_id)
        return

    lang = session.get("language") or get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    if session["current_answered"]:
        await update.callback_query.answer(strings["already_answered"], show_alert=True)
        return

    q_ids = session["question_ids"]
    curr_idx = session["current_idx"]
    if curr_idx >= len(q_ids):
        await finish_and_show_results(update, context, user_id)
        return

    q_id = q_ids[curr_idx]
    q_data = get_question_by_id(q_id)
    if not q_data:
        return

    correct_opt = q_data["correct_opt"].upper()
    is_correct = (chosen_opt.upper() == correct_opt)

    # Record answer in database
    session = record_answer(user_id, chosen_opt, is_correct)

    # Format feedback message
    feedback_text = strings["correct_answer"] if is_correct else strings["wrong_answer"].format(correct=correct_opt)
    explanation = q_data.get("explanation", "No detailed explanation provided.")
    exp_block = strings["explanation_header"].format(explanation=explanation)

    level_label = dict(EXAM_LEVELS).get(session["exam_level"], session["exam_level"].upper())
    
    # Mark options with symbols
    def format_opt(letter, text):
        icon = ""
        if letter == correct_opt:
            icon = " ✅"
        elif letter == chosen_opt and not is_correct:
            icon = " ❌"
        return f"{letter}) {text}{icon}"

    updated_card = (
        f"📌 **Question {curr_idx + 1}/{len(q_ids)}** | *{level_label}*\n"
        f"🏷️ **Topic:** {q_data['topic'].replace('_', ' ').title()}\n\n"
        f"{q_data['question_text']}\n\n"
        f"{format_opt('A', q_data['opt_a'])}\n"
        f"{format_opt('B', q_data['opt_b'])}\n"
        f"{format_opt('C', q_data['opt_c'])}\n"
        f"{format_opt('D', q_data['opt_d'])}\n\n"
        f"{feedback_text}"
        f"{exp_block}"
    )

    # New keyboard with Next Question and View Result
    keyboard = [
        [InlineKeyboardButton(strings["btn_next"], callback_data="quiz:next_q")],
        [InlineKeyboardButton(strings["btn_view_result"], callback_data="quiz:view_result")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.answer("Answer recorded!")
    await update.callback_query.edit_message_text(updated_card, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_hint_request(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Display hint modal popup without spoiling the answer."""
    session = get_session(user_id)
    if not session:
        await update.callback_query.answer("No active quiz session found.")
        return

    q_ids = session["question_ids"]
    curr_idx = session["current_idx"]
    if curr_idx >= len(q_ids):
        await update.callback_query.answer("No hint available.")
        return

    q_id = q_ids[curr_idx]
    q_data = get_question_by_id(q_id)
    hint_text = q_data.get("hint") if q_data else None

    if not hint_text:
        hint_text = "Eliminate two options that are obviously incorrect, then consider the remaining choices carefully!"

    # Show as an alert popup directly on user's Telegram screen
    await update.callback_query.answer(f"💡 HINT:\n{hint_text}", show_alert=True)

async def finish_and_show_results(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Finalize quiz, save stats, and display the scorecard."""
    session = finish_quiz_session(user_id)
    user = update.effective_user
    name = user.first_name if user else "Candidate"

    if not session:
        # Fallback if session was already closed
        await show_main_menu(update, context, user_id)
        return

    lang = session.get("language") or get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    total = len(session["question_ids"])
    attempted = session["answered_count"]
    correct = session["score"]
    wrong = attempted - correct
    accuracy = round((correct / attempted * 100), 1) if attempted > 0 else 0

    if accuracy >= 80:
        grade = "⭐⭐⭐⭐⭐ Outstanding / Excellent!"
        feedback = "🔥 Brilliant preparation! You are well-positioned for top ranks!"
    elif accuracy >= 50:
        grade = "⭐⭐⭐ Good Effort!"
        feedback = "👍 Solid performance! Revise the explanations to target full marks."
    else:
        grade = "⭐ Needs More Practice"
        feedback = "📖 Keep going! Review NCERT chapters and retake the quiz daily."

    sub_name = SUBJECTS_DATA.get(session["subject"], {}).get("name", session["subject"].title())
    level_label = dict(EXAM_LEVELS).get(session["exam_level"], session["exam_level"].upper())

    result_text = strings["result_card"].format(
        name=name,
        subject=sub_name,
        level=level_label,
        correct=correct,
        wrong=wrong,
        attempted=attempted,
        total=total,
        accuracy=accuracy,
        grade=grade,
        feedback=feedback
    )

    keyboard = [
        [InlineKeyboardButton(strings["btn_retry"], callback_data="menu:start_quiz")],
        [InlineKeyboardButton(strings["btn_home"], callback_data="menu:home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_user_stats(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Display cumulative performance analytics for user."""
    user = update.effective_user
    name = user.first_name if user else "Candidate"
    lang = get_user_language(user_id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    stats = get_user_stats(user_id)
    text = strings["stats_card"].format(
        name=name,
        total_quizzes=stats["quizzes_completed"],
        total_attempted=stats["total_attempted"],
        total_correct=stats["total_correct"],
        accuracy=stats["accuracy"]
    )

    keyboard = [
        [InlineKeyboardButton(strings["btn_start_quiz"], callback_data="menu:start_quiz")],
        [InlineKeyboardButton(strings["btn_home"], callback_data="menu:home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ==========================================
# MASTER CALLBACK ROUTER
# ==========================================

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Central router for all inline button callbacks."""
    query = update.callback_query
    data = query.data
    user = update.effective_user
    if not user:
        return
    user_id = user.id

    if data.startswith("lang:"):
        code = data.split(":", 1)[1]
        set_user_language(user_id, code)
        await query.answer("Language updated!")
        await show_main_menu(update, context, user_id)

    elif data == "menu:start_quiz":
        await show_subjects_menu(update, context, user_id)

    elif data == "menu:my_stats":
        await show_user_stats(update, context, user_id)

    elif data == "menu:change_lang":
        await start_handler(update, context)

    elif data == "menu:home":
        await show_main_menu(update, context, user_id)

    elif data == "menu:help":
        lang = get_user_language(user_id)
        strings = UI_STRINGS.get(lang, UI_STRINGS["en"])
        keyboard = [[InlineKeyboardButton(strings["btn_home"], callback_data="menu:home")]]
        await query.answer()
        await query.edit_message_text(strings["help_text"], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("sub:"):
        subject_key = data.split(":", 1)[1]
        await show_topics_menu(update, context, user_id, subject_key)

    elif data.startswith("top:"):
        topic_key = data.split(":", 1)[1]
        await show_levels_menu(update, context, user_id, topic_key)

    elif data.startswith("lvl:"):
        exam_level = data.split(":", 1)[1]
        await start_quiz(update, context, user_id, exam_level)

    elif data.startswith("ans:"):
        chosen_opt = data.split(":", 1)[1]
        await handle_answer_selection(update, context, user_id, chosen_opt)

    elif data == "quiz:hint":
        await handle_hint_request(update, context, user_id)

    elif data == "quiz:next_q":
        next_question_index(user_id)
        await display_current_question(update, context, user_id)

    elif data == "quiz:view_result":
        await finish_and_show_results(update, context, user_id)

# ==========================================
# BOT APPLICATION BOOTSTRAP
# ==========================================

def main():
    """Start the bot."""
    # Ensure database tables exist and seed default question bank
    init_db()
    seed_database_if_empty()

    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("=" * 60)
        print("⚠️ [WARNING] BOT_TOKEN is not configured!")
        print("Please set your BOT_TOKEN in config.py or as an environment variable.")
        print("Example: set BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ")
        print("=" * 60)
        return

    logger.info("Initializing Telegram Quiz Bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # User Command Handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("menu", lambda u, c: show_main_menu(u, c, u.effective_user.id)))
    app.add_handler(CommandHandler("stats", lambda u, c: show_user_stats(u, c, u.effective_user.id)))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(get_text(u.effective_user.id, "help_text"), parse_mode="Markdown")))

    # Admin Handlers
    app.add_handler(CommandHandler("admin", admin_panel_handler))
    app.add_handler(CommandHandler("broadcast", admin_broadcast_handler))
    app.add_handler(CommandHandler("addq", admin_add_question_handler))

    # Master Callback Query Handler
    app.add_handler(CallbackQueryHandler(callback_router))

    logger.info("Bot is polling for updates... Press Ctrl+C to terminate.")
    app.run_polling()

if __name__ == "__main__":
    main()
