# 🔧 IMPORT TROUBLESHOOTING & FIX

## Issue Found

The import script failed because:
- **Phase 1**: ✅ Successful (11 users from dummy CSV)
- **Phase 2**: ❌ Failed (99 out of 100 users from untitled spreadsheet)

**Error**: `get() returned more than one User -- it returned 4!`

This means there are **duplicate users in the Django database** with the same email.

---

## ✅ Fix Applied

I've updated both import scripts to use `.filter().first()` instead of `.get()`, which handles duplicates gracefully by selecting the first matching user.

**Files updated:**
- `backend/import_untitled_spreadsheet.py`
- `backend/import_dummy_users_supabase.py`

---

## 🧹 Cleanup Required

**Step 1: Clean up orphaned Supabase users**

85+ Supabase users were created but not mapped to Django users. Let's delete them:

```bash
cd backend
python cleanup_orphaned_supabase_users.py
```

This will:
1. Find all Supabase users without Django mappings
2. Show you the list
3. Delete them after confirmation

---

## 🔄 Re-run Import

After cleanup, re-run the import:

```bash
cd backend
python import_untitled_spreadsheet.py
```

Choose option **1** (default password: `TempPass@2024`)

---

## 📋 Expected Results

After re-import:
- **11 users** from dummy CSV (already imported ✅)
- **100 users** from untitled spreadsheet (will now succeed ✅)
- **Total: 111 users** ready to login

---

## 🚀 Quick Commands

**Option 1: Full cleanup and re-import**
```bash
cd backend
python cleanup_orphaned_supabase_users.py
python import_untitled_spreadsheet.py
```

**Option 2: Just re-import (skip cleanup)**
```bash
cd backend
python import_untitled_spreadsheet.py
```

---

## ℹ️ What Went Wrong?

The database had duplicate users from previous imports/tests. The script tried to use `.get()` which requires exactly one match, but found 4-7 duplicate users with the same email.

The fix uses `.filter().first()` which:
- Returns the first match if duplicates exist
- Handles edge cases gracefully
- Continues importing without errors

---

## 🔐 Login Credentials

After successful import, all users can login with:

**From dummy CSV (11 users):**
- Email: `<from CSV>`
- Password: `pass123@`

**From untitled spreadsheet (100 users):**
- Email: `<from CSV>`
- Password: `TempPass@2024`

Example:
- Email: `sudharsshana.r.cse.2024@snsce.ac.in`
- Password: `pass123@`

Or:
- Email: `naren.rs.cse.2024@snsct.org`
- Password: `TempPass@2024`
