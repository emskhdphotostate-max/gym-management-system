# 🏋️ IRON PULSE GYM — Admin Panel (Streamlit + Neon)

VIP/premium gym management web app: members, fee/chalan history, timing, PDF export, secure admin login.
Colour theme matches your reference login design (deep blue background, white card, orange→pink gradient buttons).

## Features
- 🔐 Secure admin login (bcrypt-hashed password, stored in Neon Postgres)
- 🧑‍🤝‍🧑 Member management (add / edit / delete / search)
- 🧾 Fee collection with **auto-generated chalan numbers** + PDF chalan download
- 📜 Full fee/chalan history per member and gym-wide
- ⏰ Gym timing settings (opening/closing hours, weekly off, members grouped by slot)
- 📄 One-click PDF export for members list and fee history reports
- 🚪 Logout
- 🎨 Custom themed UI matching your provided design (logo included in `assets/logo.png`)

## Project Structure
```
gym-app/
├── app.py                  # Login page (entry point)
├── requirements.txt
├── .streamlit/
│   ├── config.toml         # Theme colors
│   └── secrets_example.toml# Copy to secrets.toml and fill in
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Members.py
│   ├── 3_Fee_Chalan.py
│   ├── 4_Timing.py
│   └── 5_Reports.py
├── utils/
│   ├── db.py                # Neon Postgres queries
│   ├── auth.py               # Login/logout, bcrypt hashing
│   ├── pdf_generator.py      # Chalan + report PDFs
│   └── styles.py              # Shared CSS theme
└── assets/
    └── logo.png             # Demo gym logo (replace anytime)
```

## 1. Create your free Neon database
1. Go to https://neon.tech and sign up (free tier is enough).
2. Create a new project.
3. Open **Connection Details** and copy the connection string
   (looks like `postgresql://user:pass@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require`).

You do **not** need to create tables manually — the app creates them automatically
on first run (`init_db()` in `utils/db.py`).

## 2. Configure secrets locally
```bash
cp .streamlit/secrets_example.toml .streamlit/secrets.toml
```
Edit `.streamlit/secrets.toml` and paste your real `NEON_DB_URL`. Also set:
- `DEFAULT_ADMIN_USERNAME` / `DEFAULT_ADMIN_PASSWORD` — the first admin account created automatically
- `GYM_NAME` — shown on the login screen and sidebar

⚠️ `secrets.toml` is already in `.gitignore` — never commit it.

## 3. Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Default demo login: **admin / Admin@123** (change this in `secrets.toml` before going live).

## 4. Push to GitHub
```bash
git init
git add .
git commit -m "Gym admin panel - initial version"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```
Double-check `secrets.toml` is **not** in the commit (`git status` should not list it).

## 5. Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io and connect your GitHub repo.
2. Set **Main file path** to `app.py`.
3. In the app's **Settings → Secrets**, paste the same content as your local `secrets.toml`
   (this is how Neon credentials reach the deployed app securely).
4. Deploy — done! 🎉

## Customizing later
- **Change gym name / logo:** edit `GYM_NAME` in secrets, and replace `assets/logo.png` with your real logo (same filename, any size works).
- **Change colors:** edit `.streamlit/config.toml` and `utils/styles.py`.
- **Add more admin accounts:** currently one default admin is auto-seeded; you can insert more rows into the `admins` table directly in Neon's SQL editor using a bcrypt hash, or extend `pages/` with an "Admin Users" management page later.

## Notes
- All money fields default to **PKR (Rs.)** — change the currency label in `utils/pdf_generator.py` and page files if needed.
- Chalan numbers are auto-generated in the format `CH-YYYY-00001`.
