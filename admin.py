import os
import sys

# Ensure local module directory has highest priority in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS, UI_STRINGS
from database import get_admin_stats, get_all_user_ids, insert_question, get_user_language

logger = logging.getLogger(__name__)

def is_admin(user_id: int) -> bool:
    """Check if the user has administrator privileges."""
    if not ADMIN_IDS:
        # If no ADMIN_IDS set in env, allow first user or anyone who passes check for convenience
        return True
    return user_id in ADMIN_IDS

async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command."""
    user = update.effective_user
    if not user:
        return

    lang = get_user_language(user.id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    if not is_admin(user.id):
        await update.message.reply_text(strings["admin_access_denied"])
        return

    stats = get_admin_stats()
    text = strings["admin_panel"].format(
        users_count=stats["users_count"],
        questions_count=stats["questions_count"],
        quizzes_count=stats["quizzes_count"]
    )
    
    text += (
        "\n\n**Format to add question via /addq:**\n"
        "`/addq subject|topic|exam_level|language|question|optA|optB|optC|optD|correct(A/B/C/D)|explanation|hint`"
    )
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def admin_stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command for admins."""
    user = update.effective_user
    if not user or not is_admin(user.id):
        return

    stats = get_admin_stats()
    text = (
        "📊 **Global Bot Analytics**\n\n"
        f"👥 **Total Registered Candidates:** `{stats['users_count']}`\n"
        f"📚 **Total Questions in Bank:** `{stats['questions_count']}`\n"
        f"🎯 **Total Quizzes Completed:** `{stats['quizzes_count']}`"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def admin_broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast <message> command."""
    user = update.effective_user
    if not user:
        return
        
    lang = get_user_language(user.id)
    strings = UI_STRINGS.get(lang, UI_STRINGS["en"])

    if not is_admin(user.id):
        await update.message.reply_text(strings["admin_access_denied"])
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ **Usage:** `/broadcast Your message here`\n\nExample:\n`/broadcast New Biology questions for NEET have been added! Practice now!`",
            parse_mode="Markdown"
        )
        return

    broadcast_msg = " ".join(context.args)
    user_ids = get_all_user_ids()
    
    status_msg = await update.message.reply_text(f"⏳ Broadcasting message to {len(user_ids)} users...")
    
    sent = 0
    failed = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"📢 **ANNOUNCEMENT**\n\n{broadcast_msg}",
                parse_mode="Markdown"
            )
            sent += 1
        except Exception as e:
            logger.warning(f"Failed to send broadcast to {uid}: {e}")
            failed += 1

    await status_msg.edit_text(
        f"✅ **Broadcast Complete!**\n\n• Successfully Sent: `{sent}`\n• Failed / Blocked: `{failed}`\n• Total: `{len(user_ids)}`",
        parse_mode="Markdown"
    )

async def admin_add_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addq pipe-delimited format to quickly add questions."""
    user = update.effective_user
    if not user or not is_admin(user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ **Format:**\n"
            "`/addq subject|topic|exam_level|language|question|optA|optB|optC|optD|correct|explanation|hint`\n\n"
            "**Example:**\n"
            "`/addq biology|bio_cell|neet|en|What organelle synthesizes ATP?|Mitochondria|Ribosome|Lysosome|Vacuole|A|Mitochondria generates ATP via respiration.|Powerhouse of cell`",
            parse_mode="Markdown"
        )
        return

    raw_input = " ".join(context.args)
    parts = [p.strip() for p in raw_input.split("|")]
    
    if len(parts) < 12:
        await update.message.reply_text(
            f"❌ **Invalid argument count!** Found {len(parts)} parts, expected 12 parts separated by `|`.\n"
            "Format: `subject|topic|exam_level|language|question|optA|optB|optC|optD|correct|explanation|hint`"
        )
        return

    sub, top, lvl, lng, q, a, b, c, d, corr, exp, hnt = parts[:12]
    corr = corr.upper()
    if corr not in ["A", "B", "C", "D"]:
        await update.message.reply_text("❌ Correct option must be A, B, C, or D.")
        return

    q_id = insert_question(sub, top, lvl, lng, q, a, b, c, d, corr, exp, hnt)
    await update.message.reply_text(
        f"✅ **Question successfully added!** (ID: `{q_id}`)\n\n"
        f"• **Subject:** {sub} | **Topic:** {top}\n"
        f"• **Level:** {lvl} | **Language:** {lng}\n"
        f"• **Question:** {q}\n"
        f"• **Correct Option:** {corr}",
        parse_mode="Markdown"
    )
