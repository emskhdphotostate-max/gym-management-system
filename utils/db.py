"""
Database layer — all Neon (Postgres) connection + query logic lives here.
Uses SQLAlchemy so it works cleanly with pandas + Streamlit caching.
"""

import ssl
import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from sqlalchemy import create_engine, text
from datetime import date, datetime


@st.cache_resource(show_spinner=False)
def get_engine():
    raw_url = st.secrets["NEON_DB_URL"]
    parsed = urlparse(raw_url)
    clean_url = f"postgresql+pg8000://{parsed.netloc}{parsed.path}"
    ssl_context = ssl.create_default_context()
    return create_engine(clean_url, pool_pre_ping=True, connect_args={"ssl_context": ssl_context})


def init_db():
    """Creates all required tables if they don't exist yet. Safe to run every startup."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS admins (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS members (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(150) NOT NULL,
                phone VARCHAR(30),
                email VARCHAR(150),
                address TEXT,
                gender VARCHAR(20),
                membership_type VARCHAR(50) DEFAULT 'Standard',
                monthly_fee NUMERIC(10,2) DEFAULT 2000,
                time_slot VARCHAR(30) DEFAULT 'Morning',
                join_date DATE DEFAULT CURRENT_DATE,
                status VARCHAR(20) DEFAULT 'Active',
                photo TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))
        # Ensure photo column exists if table was created previously
        conn.execute(text("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='members' AND column_name='photo') THEN
                    ALTER TABLE members ADD COLUMN photo TEXT;
                END IF;
            END $$;
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fees (
                id SERIAL PRIMARY KEY,
                member_id INTEGER REFERENCES members(id) ON DELETE CASCADE,
                chalan_no VARCHAR(30) UNIQUE NOT NULL,
                amount NUMERIC(10,2) NOT NULL,
                month VARCHAR(20) NOT NULL,
                year INTEGER NOT NULL,
                payment_method VARCHAR(30) DEFAULT 'Cash',
                status VARCHAR(20) DEFAULT 'Paid',
                paid_date DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS gym_settings (
                id SERIAL PRIMARY KEY,
                key VARCHAR(50) UNIQUE NOT NULL,
                value TEXT
            );
        """))
        conn.execute(text("""
            INSERT INTO gym_settings (key, value)
            VALUES ('opening_time', '06:00 AM'), ('closing_time', '11:00 PM'),
                   ('weekly_off', 'Sunday')
            ON CONFLICT (key) DO NOTHING;
        """))

        # Attendance Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS attendance (
                id SERIAL PRIMARY KEY,
                member_id INTEGER REFERENCES members(id) ON DELETE CASCADE,
                date DATE DEFAULT CURRENT_DATE,
                time_in TIME DEFAULT CURRENT_TIME,
                notes TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))

        # Expenses Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                title VARCHAR(150) NOT NULL,
                category VARCHAR(50) DEFAULT 'Utilities',
                amount NUMERIC(10,2) NOT NULL,
                expense_date DATE DEFAULT CURRENT_DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))

        # Trainers Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS trainers (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(150) NOT NULL,
                phone VARCHAR(30),
                specialization VARCHAR(100),
                salary NUMERIC(10,2) DEFAULT 0,
                shift VARCHAR(30) DEFAULT 'Morning',
                status VARCHAR(20) DEFAULT 'Active',
                photo TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))


def seed_default_admin(username: str, password_hash: str):
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM admins")).scalar()
        if result == 0:
            conn.execute(
                text("INSERT INTO admins (username, password_hash) VALUES (:u, :p)"),
                {"u": username, "p": password_hash},
            )


def get_admin_by_username(username: str):
    engine = get_engine()
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT id, username, password_hash FROM admins WHERE username = :u"),
            {"u": username},
        ).fetchone()
        return row


# ---------------- Members ----------------

def add_member(data: dict):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO members (full_name, phone, email, address, gender,
                membership_type, monthly_fee, time_slot, join_date, status, photo)
            VALUES (:full_name, :phone, :email, :address, :gender,
                :membership_type, :monthly_fee, :time_slot, :join_date, :status, :photo)
        """), data)


def update_member(member_id: int, data: dict):
    engine = get_engine()
    data["id"] = member_id
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE members SET full_name=:full_name, phone=:phone, email=:email,
                address=:address, gender=:gender, membership_type=:membership_type,
                monthly_fee=:monthly_fee, time_slot=:time_slot, status=:status, photo=:photo
            WHERE id=:id
        """), data)


def delete_member(member_id: int):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM members WHERE id=:id"), {"id": member_id})


def get_all_members() -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(text("SELECT * FROM members ORDER BY id DESC"), engine)


def get_member(member_id: int):
    engine = get_engine()
    with engine.begin() as conn:
        return conn.execute(text("SELECT * FROM members WHERE id=:id"), {"id": member_id}).fetchone()


# ---------------- Fees / Chalans ----------------

def generate_chalan_no():
    engine = get_engine()
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM fees")).scalar()
    return f"CH-{date.today().year}-{count + 1:05d}"


def add_fee(data: dict):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO fees (member_id, chalan_no, amount, month, year,
                payment_method, status, paid_date)
            VALUES (:member_id, :chalan_no, :amount, :month, :year,
                :payment_method, :status, :paid_date)
        """), data)


def get_fees_for_member(member_id: int) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(
        text("SELECT * FROM fees WHERE member_id=:id ORDER BY id DESC"),
        engine, params={"id": member_id}
    )


def get_all_fees() -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(text("""
        SELECT f.*, m.full_name, m.phone
        FROM fees f JOIN members m ON f.member_id = m.id
        ORDER BY f.id DESC
    """), engine)


def get_fee_by_chalan(chalan_no: str):
    engine = get_engine()
    with engine.begin() as conn:
        return conn.execute(text("""
            SELECT f.*, m.full_name, m.phone, m.email, m.membership_type
            FROM fees f JOIN members m ON f.member_id = m.id
            WHERE f.chalan_no = :c
        """), {"c": chalan_no}).fetchone()


# ---------------- Attendance ----------------

def mark_attendance(member_id: int, notes: str = ""):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO attendance (member_id, date, time_in, notes)
            VALUES (:member_id, CURRENT_DATE, CURRENT_TIME, :notes)
        """), {"member_id": member_id, "notes": notes})


def get_today_attendance() -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(text("""
        SELECT a.id, a.date, to_char(a.time_in, 'HH12:MI AM') as time_in,
               m.full_name, m.phone, m.membership_type, m.time_slot, a.notes
        FROM attendance a
        JOIN members m ON a.member_id = m.id
        WHERE a.date = CURRENT_DATE
        ORDER BY a.id DESC
    """), engine)


def get_attendance_history(limit: int = 100) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(text(f"""
        SELECT a.id, a.date, to_char(a.time_in, 'HH12:MI AM') as time_in,
               m.full_name, m.phone, m.membership_type, a.notes
        FROM attendance a
        JOIN members m ON a.member_id = m.id
        ORDER BY a.id DESC
        LIMIT {limit}
    """), engine)


# ---------------- Expenses ----------------

def add_expense(data: dict):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO expenses (title, category, amount, expense_date, notes)
            VALUES (:title, :category, :amount, :expense_date, :notes)
        """), data)


def get_all_expenses() -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(text("SELECT * FROM expenses ORDER BY id DESC"), engine)


def delete_expense(expense_id: int):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM expenses WHERE id=:id"), {"id": expense_id})


# ---------------- Trainers ----------------

def add_trainer(data: dict):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO trainers (full_name, phone, specialization, salary, shift, status, photo)
            VALUES (:full_name, :phone, :specialization, :salary, :shift, :status, :photo)
        """), data)


def update_trainer(trainer_id: int, data: dict):
    engine = get_engine()
    data["id"] = trainer_id
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE trainers SET full_name=:full_name, phone=:phone,
                specialization=:specialization, salary=:salary, shift=:shift,
                status=:status, photo=:photo
            WHERE id=:id
        """), data)


def delete_trainer(trainer_id: int):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM trainers WHERE id=:id"), {"id": trainer_id})


def get_all_trainers() -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(text("SELECT * FROM trainers ORDER BY id DESC"), engine)


def get_trainer(trainer_id: int):
    engine = get_engine()
    with engine.begin() as conn:
        return conn.execute(text("SELECT * FROM trainers WHERE id=:id"), {"id": trainer_id}).fetchone()


# ---------------- Settings ----------------

def get_setting(key: str, default=""):
    engine = get_engine()
    with engine.begin() as conn:
        row = conn.execute(text("SELECT value FROM gym_settings WHERE key=:k"), {"k": key}).fetchone()
        return row[0] if row else default


def set_setting(key: str, value: str):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO gym_settings (key, value) VALUES (:k, :v)
            ON CONFLICT (key) DO UPDATE SET value = :v
        """), {"k": key, "v": value})


# ---------------- Dashboard stats ----------------

def get_dashboard_stats():
    engine = get_engine()
    with engine.begin() as conn:
        total_members = conn.execute(text("SELECT COUNT(*) FROM members")).scalar()
        active_members = conn.execute(text("SELECT COUNT(*) FROM members WHERE status='Active'")).scalar()

        # Month formatted without trailing spaces
        this_month_income = conn.execute(text("""
            SELECT COALESCE(SUM(amount), 0) FROM fees
            WHERE TRIM(month) = TRIM(to_char(CURRENT_DATE, 'Month'))
              AND year = EXTRACT(YEAR FROM CURRENT_DATE)
        """)).scalar()

        total_income = conn.execute(text("SELECT COALESCE(SUM(amount), 0) FROM fees")).scalar()

        this_month_expenses = conn.execute(text("""
            SELECT COALESCE(SUM(amount), 0) FROM expenses
            WHERE EXTRACT(MONTH FROM expense_date) = EXTRACT(MONTH FROM CURRENT_DATE)
              AND EXTRACT(YEAR FROM expense_date) = EXTRACT(YEAR FROM CURRENT_DATE)
        """)).scalar()

        total_expenses = conn.execute(text("SELECT COALESCE(SUM(amount), 0) FROM expenses")).scalar()

        today_attendance_count = conn.execute(text("""
            SELECT COUNT(*) FROM attendance WHERE date = CURRENT_DATE
        """)).scalar()

        total_trainers = conn.execute(text("SELECT COUNT(*) FROM trainers WHERE status='Active'")).scalar()

    return {
        "total_members": total_members or 0,
        "active_members": active_members or 0,
        "this_month_income": float(this_month_income or 0),
        "total_income": float(total_income or 0),
        "this_month_expenses": float(this_month_expenses or 0),
        "total_expenses": float(total_expenses or 0),
        "net_profit": float((total_income or 0) - (total_expenses or 0)),
        "today_attendance": today_attendance_count or 0,
        "active_trainers": total_trainers or 0,
    }
