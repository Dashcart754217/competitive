import os
import sys

# Ensure local module directory has highest priority in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import sqlite3
import json
import logging
from typing import Optional, List, Dict, Any, Tuple
from config import DB_PATH

logger = logging.getLogger(__name__)

def get_connection():
    """Get a SQLite database connection with row factory configured."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'en',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Questions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                exam_level TEXT NOT NULL,
                language TEXT NOT NULL,
                question_text TEXT NOT NULL,
                opt_a TEXT NOT NULL,
                opt_b TEXT NOT NULL,
                opt_c TEXT NOT NULL,
                opt_d TEXT NOT NULL,
                correct_opt TEXT NOT NULL,
                explanation TEXT,
                hint TEXT
            )
        """)
        
        # User Quiz Sessions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                user_id INTEGER PRIMARY KEY,
                subject TEXT,
                topic TEXT,
                exam_level TEXT,
                language TEXT,
                question_ids TEXT,
                current_idx INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                answered_count INTEGER DEFAULT 0,
                current_answered INTEGER DEFAULT 0,
                answers_history TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User Analytics Stats Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER PRIMARY KEY,
                quizzes_completed INTEGER DEFAULT 0,
                total_attempted INTEGER DEFAULT 0,
                total_correct INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
    logger.info("Database initialized successfully.")

def get_or_create_user(user_id: int, username: Optional[str], first_name: Optional[str]) -> Dict[str, Any]:
    """Retrieve existing user or register a new user in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            cursor.execute(
                "UPDATE users SET last_active = CURRENT_TIMESTAMP, username = ?, first_name = ? WHERE user_id = ?",
                (username or "", first_name or "", user_id)
            )
            conn.commit()
            return dict(row)
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name, language) VALUES (?, ?, ?, 'en')",
            (user_id, username or "", first_name or "")
        )
        cursor.execute(
            "INSERT OR IGNORE INTO user_stats (user_id, quizzes_completed, total_attempted, total_correct) VALUES (?, 0, 0, 0)",
            (user_id,)
        )
        conn.commit()
        return {"user_id": user_id, "username": username, "first_name": first_name, "language": "en"}

def set_user_language(user_id: int, language: str) -> None:
    """Update language preference for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
        conn.commit()

def get_user_language(user_id: int) -> str:
    """Get the current language preference of the user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return row["language"] if row and row["language"] else "en"

def get_questions_for_quiz(subject: str, topic: str, exam_level: str, language: str, limit: int = 10) -> List[int]:
    """
    Fetch a randomized batch of question IDs matching subject, topic, exam_level, and language.
    Includes smart fallbacks if topic or exam level has fewer questions.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # If user picked mixed topic (ending in _all)
        topic_clause = "" if topic.endswith("_all") else "AND topic = ?"
        
        # Try finding questions matching exact language
        query = f"""
            SELECT id FROM questions 
            WHERE subject = ? {topic_clause}
            AND language = ?
            ORDER BY RANDOM() LIMIT ?
        """
        params = [subject]
        if not topic.endswith("_all"):
            params.append(topic)
        params.extend([language, limit])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        q_ids = [r["id"] for r in rows]
        
        # If we got fewer than 5 questions, relax the topic restriction to subject level
        if len(q_ids) < 3 and not topic.endswith("_all"):
            cursor.execute("""
                SELECT id FROM questions 
                WHERE subject = ? AND language = ? AND id NOT IN ({})
                ORDER BY RANDOM() LIMIT ?
            """.format(",".join("?" for _ in q_ids) if q_ids else "0"),
            [subject, language] + q_ids + [limit - len(q_ids)])
            q_ids.extend([r["id"] for r in cursor.fetchall()])
            
        # If still empty (e.g., questions in English fallback), fetch in 'en' or any language
        if len(q_ids) < 2:
            cursor.execute("""
                SELECT id FROM questions 
                WHERE subject = ?
                ORDER BY RANDOM() LIMIT ?
            """, (subject, limit))
            q_ids = [r["id"] for r in cursor.fetchall()]
            
        return q_ids

def get_question_by_id(question_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve full details of a question by its primary key ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def start_quiz_session(user_id: int, subject: str, topic: str, exam_level: str, language: str, question_ids: List[int]) -> bool:
    """Create or reset an active quiz session for the user."""
    if not question_ids:
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO user_sessions 
            (user_id, subject, topic, exam_level, language, question_ids, current_idx, score, answered_count, current_answered, answers_history)
            VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 0, '[]')
        """, (user_id, subject, topic, exam_level, language, json.dumps(question_ids)))
        conn.commit()
    return True

def get_session(user_id: int) -> Optional[Dict[str, Any]]:
    """Get active session details for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_sessions WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        data = dict(row)
        data["question_ids"] = json.loads(data["question_ids"]) if data["question_ids"] else []
        data["answers_history"] = json.loads(data["answers_history"]) if data["answers_history"] else []
        return data

def record_answer(user_id: int, chosen_opt: str, is_correct: bool) -> Optional[Dict[str, Any]]:
    """Record user's answer for the current question."""
    session = get_session(user_id)
    if not session:
        return None
        
    current_answered = session["current_answered"]
    if current_answered:
        return session  # already answered this question
        
    idx = session["current_idx"]
    q_ids = session["question_ids"]
    if idx >= len(q_ids):
        return session
        
    q_id = q_ids[idx]
    new_score = session["score"] + (1 if is_correct else 0)
    new_answered = session["answered_count"] + 1
    
    history = session["answers_history"]
    history.append({
        "q_id": q_id,
        "chosen": chosen_opt,
        "is_correct": is_correct
    })
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_sessions 
            SET score = ?, answered_count = ?, current_answered = 1, answers_history = ?
            WHERE user_id = ?
        """, (new_score, new_answered, json.dumps(history), user_id))
        conn.commit()
        
    session["score"] = new_score
    session["answered_count"] = new_answered
    session["current_answered"] = 1
    session["answers_history"] = history
    return session

def next_question_index(user_id: int) -> Optional[Dict[str, Any]]:
    """Advance the user's session to the next question."""
    session = get_session(user_id)
    if not session:
        return None
        
    new_idx = session["current_idx"] + 1
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_sessions 
            SET current_idx = ?, current_answered = 0
            WHERE user_id = ?
        """, (new_idx, user_id))
        conn.commit()
        
    session["current_idx"] = new_idx
    session["current_answered"] = 0
    return session

def finish_quiz_session(user_id: int) -> Optional[Dict[str, Any]]:
    """Finalize the quiz session and update cumulative user stats."""
    session = get_session(user_id)
    if not session:
        return None
        
    attempted = session["answered_count"]
    correct = session["score"]
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_stats 
            SET quizzes_completed = quizzes_completed + 1,
                total_attempted = total_attempted + ?,
                total_correct = total_correct + ?
            WHERE user_id = ?
        """, (attempted, correct, user_id))
        
        # Clear active session
        cursor.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,))
        conn.commit()
        
    return session

def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Retrieve cumulative statistics for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_stats WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return {"quizzes_completed": 0, "total_attempted": 0, "total_correct": 0, "accuracy": 0}
        
        data = dict(row)
        attempted = data.get("total_attempted", 0)
        correct = data.get("total_correct", 0)
        accuracy = round((correct / attempted * 100), 1) if attempted > 0 else 0
        data["accuracy"] = accuracy
        return data

def get_admin_stats() -> Dict[str, int]:
    """Retrieve global system statistics for the admin dashboard."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS count FROM users")
        users_count = cursor.fetchone()["count"]
        
        cursor.execute("SELECT COUNT(*) AS count FROM questions")
        questions_count = cursor.fetchone()["count"]
        
        cursor.execute("SELECT COALESCE(SUM(quizzes_completed), 0) AS count FROM user_stats")
        quizzes_count = cursor.fetchone()["count"]
        
        return {
            "users_count": users_count,
            "questions_count": questions_count,
            "quizzes_count": quizzes_count
        }

def get_all_user_ids() -> List[int]:
    """Return all registered Telegram user IDs for broadcasts."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        return [r["user_id"] for r in cursor.fetchall()]

def insert_question(subject: str, topic: str, exam_level: str, language: str, 
                    q_text: str, opt_a: str, opt_b: str, opt_c: str, opt_d: str, 
                    correct_opt: str, explanation: str, hint: str) -> int:
    """Insert a single question into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions 
            (subject, topic, exam_level, language, question_text, opt_a, opt_b, opt_c, opt_d, correct_opt, explanation, hint)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (subject, topic, exam_level, language, q_text, opt_a, opt_b, opt_c, opt_d, correct_opt.upper(), explanation, hint))
        conn.commit()
        return cursor.lastrowid
