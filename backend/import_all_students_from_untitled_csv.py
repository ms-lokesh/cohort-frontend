"""Import every row from the attached CSV as student users with password pass123#.

This script is intentionally permissive: it does not skip rows even when data is
duplicated or partially missing. Usernames are based on the full name (trimmed; a
numeric suffix is added only if the exact name is already taken). Names and emails
are kept as provided (trimmed for safety). Campus is forced to TECH; all students
are placed on floor 2.
"""

import os
from typing import Tuple

import django
import pandas as pd


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from apps.profiles.models import UserProfile  # noqa: E402


CSV_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Untitled spreadsheet - Sheet1.csv"))
DEFAULT_PASSWORD = "pass123#"
DEFAULT_FLOOR = 2
FORCED_CAMPUS = "TECH"


def infer_campus(email: str) -> str:
    email_lower = (email or "").lower()
    if "snsct.org" in email_lower:
        return "ARTS"
    if "snsce.ac.in" in email_lower:
        return "TECH"
    return None


def make_username(full_name: str, row_index: int) -> str:
    # Collapse internal whitespace to keep the username close to the provided name
    cleaned = " ".join((full_name or "").strip().split())
    if not cleaned:
        cleaned = f"student_{row_index + 1:03d}"

    candidate = cleaned
    suffix = 1
    while User.objects.filter(username=candidate).exists():
        candidate = f"{cleaned}_{suffix}"
        suffix += 1
    return candidate


def upsert_user(row: pd.Series, row_index: int) -> Tuple[bool, str, str, str, str]:
    full_name = str(row.get("FullName") or "").strip()
    email = str(row.get("College Domain Mail ID") or "").strip()
    reg_no = str(row.get("Reg Number") or "").strip()

    username = make_username(full_name, row_index)
    campus = FORCED_CAMPUS

    user = User.objects.filter(username=username).first()
    created = False

    if not user:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=DEFAULT_PASSWORD,
            first_name=full_name,
            last_name="",
            is_staff=False,
            is_superuser=False,
        )
        created = True
    else:
        user.first_name = full_name
        user.last_name = ""
        user.email = email
        user.is_staff = False
        user.is_superuser = False
        user.set_password(DEFAULT_PASSWORD)
        user.save()

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "role": "STUDENT",
            "campus": campus,
            "floor": DEFAULT_FLOOR,
        },
    )
    profile.role = "STUDENT"
    profile.campus = campus
    profile.floor = DEFAULT_FLOOR
    profile.save()

    return created, campus, username, full_name, email


def main() -> None:
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    df = pd.read_csv(CSV_FILE, dtype=str, keep_default_na=False)

    created_count = 0
    updated_count = 0
    fallback_campus_count = 0

    print(f"Processing {len(df)} rows from {CSV_FILE}\n")

    for idx, row in df.iterrows():
        created, campus, username, full_name, email = upsert_user(row, idx)

        if campus == FORCED_CAMPUS and infer_campus(email) is None:
            fallback_campus_count += 1

        action = "CREATED" if created else "UPDATED"
        print(
            f"{action} #{idx + 1}: username={username} | name={full_name} | "
            f"email={email} | campus={campus} | floor={DEFAULT_FLOOR}"
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    print("\nImport complete")
    print(f"Created: {created_count}")
    print(f"Updated: {updated_count}")
    print(f"Campus fallback used (emails without known domain): {fallback_campus_count}")
    print(f"Password set to: {DEFAULT_PASSWORD}")


if __name__ == "__main__":
    main()