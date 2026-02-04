"""Push all rows from the provided CSV into a Supabase Postgres table.

Environment:
- SUPABASE_PG_DSN: full Postgres DSN (use the transaction pooler DSN provided).
- SUPABASE_PG_TABLE (optional): target table name; defaults to students_import.

Behavior:
- No rows are skipped; data is inserted as-is (trimmed strings).
- Creates the table if it does not exist (id primary key, no uniqueness on email/reg_number
  so duplicates are preserved).
"""

import os
import pandas as pd
import psycopg


CSV_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Untitled spreadsheet - Sheet1.csv"))
TABLE_NAME = os.getenv("SUPABASE_PG_TABLE", "students_import")
DSN = os.getenv("SUPABASE_PG_DSN")


def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id BIGSERIAL PRIMARY KEY,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                reg_number TEXT,
                branch TEXT,
                batch TEXT,
                graduation_year TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
    conn.commit()


def load_rows():
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"CSV not found: {CSV_FILE}")

    df = pd.read_csv(CSV_FILE, dtype=str, keep_default_na=False)
    records = []
    for _, row in df.iterrows():
        records.append(
            (
                str(row.get("FullName", "")).strip(),
                str(row.get("College Domain Mail ID", "")).strip(),
                str(row.get("Phone", "")).strip(),
                str(row.get("Reg Number", "")).strip(),
                str(row.get("Branch", "")).strip(),
                str(row.get("Batch", "")).strip(),
                str(row.get("Graduation Year", "")).strip(),
            )
        )
    return records


def insert_rows(conn, rows):
    if not rows:
        print("No rows to insert.")
        return

    with conn.cursor() as cur:
        cur.executemany(
            f"""
            INSERT INTO {TABLE_NAME}
            (full_name, email, phone, reg_number, branch, batch, graduation_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            rows,
        )
    conn.commit()
    print(f"Inserted {len(rows)} rows into {TABLE_NAME}.")


def main():
    if not DSN:
        raise RuntimeError("SUPABASE_PG_DSN not set")

    rows = load_rows()
    print(f"Loaded {len(rows)} rows from {CSV_FILE}")

    with psycopg.connect(DSN) as conn:
        ensure_table(conn)
        insert_rows(conn, rows)


if __name__ == "__main__":
    main()