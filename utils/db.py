"""
Database layer — all Neon (Postgres) connection + query logic lives here.
Uses SQLAlchemy so it works cleanly with pandas + Streamlit caching.
"""

import ssl
import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from sqlalchemy import create_engine, text
from datetime import date


@st.cache_resource(show_spinner=False)
def get_engine():
    raw_url = st.secrets["NEON_DB_URL"]
    parsed = urlparse(raw_url)
    # Rebuild the URL for the pg8000 driver (pure-Python, no compilation needed,
    # works on any Python version — avoids the psycopg2 "pg_config not found" build error).
    # Query params like sslmode/channel_binding aren't used by pg8000, so we drop them
    # and pass SSL explicitly via connect_args instead.
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
                monthly_fee NUMERIC(10,2) DEFAULT 0,
                time_slot VARCHAR(30) DEFAULT 'Morning',
                join_date DATE DEFAULT CURRENT_DATE,
                status VARCHAR(20) DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT NOW()
            );
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
        # default gym timing settings
        conn.execute(text("""
            INSERT INTO gym_settings (key, value)
            VALUES ('opening_time', '06:00 AM'), ('closing_time', '11:00 PM'),
                   ('weekly_off', 'Sunday')
            ON CONFLICT (key) DO NOTHING;
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
                membership_type, monthly_fee, time_slot, join_date, status)
            VALUES (:full_name, :phone, :email, :address, :gender,
                :membership_type, :monthly_fee, :time_slot, :join_date, :status)
        """), data)


def update_member(member_id: int, data: dict):
    engine = get_engine()
    data["id"] = member_id
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE members SET full_name=:full_name, phone=:phone, email=:email,
                address=:address, gender=:gender, membership_type=:membership_type,
                monthly_fee=:monthly_fee, time_slot=:time_slot, status=:status
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
        this_month_income = conn.execute(text("""
            SELECT COALESCE(SUM(amount),0) FROM fees
            WHERE month = to_char(CURRENT_DATE, 'Month') AND year = EXTRACT(YEAR FROM CURRENT_DATE)
        """)).scalar()
        total_income = conn.execute(text("SELECT COALESCE(SUM(amount),0) FROM fees")).scalar()
    return {
        "total_members": total_members,
        "active_members": active_members,
        "this_month_income": float(this_month_income or 0),
        "total_income": float(total_income or 0),
    }
