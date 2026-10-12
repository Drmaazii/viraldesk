# ViralDesk — put it on the web (3 steps)

Your own ViralDesk website: opens on your phone and your computer, no Muse
needed, locked with a password only you know. Everything is free.

**One honest note:** the free hosting "sleeps" when nobody opens the site.
The first open of the day takes about a minute to wake up. After that it is
fast. (This is what you chose — totally fine.)

## Step 1 — GitHub (where the code lives)

Done already — the code is pushed to **Drmaazii/viraldesk** (branch `master`).
If Muse asks you for the GitHub token again, it's only to push one small
final fix; the website itself never uses it.

## Step 2 — Turso (where your data lives)

1. Go to **turso.tech** and create a free account (sign in with Google is fine).
2. **Download the `viraldesk.db` file** Muse sent you in chat (tap it on your phone).
3. In the Turso dashboard: **Databases** → **Create Database** → tap the
   **Upload SQLite File** tab at the top → upload the file → name it
   `viraldesk-data` → region **AWS AP South (Mumbai)** → Create.
4. Open the new database → copy the **URL** (starts with `libsql://`) →
   **Tokens** tab → **Create token** → copy the **token** (it shows once).
5. Paste the URL + token in chat. (You can delete the empty `viraldesk`
   database later — ignore it.)

## Step 3 — Streamlit (the website itself)

1. Go to **share.streamlit.io** and sign in **with your GitHub account**.
2. Tap **New app** → choose the `viraldesk` repository → the main file is
   `app.py` → tap **Deploy**.
3. Before it finishes, open the app's **Settings → Secrets** and paste this
   (replace with your own values):

```
TURSO_URL = "libsql://your-database-url-here"
TURSO_TOKEN = "your-token-here"
APP_PASSWORD = "pick-a-password-only-you-know"
```

4. Save. The site rebuilds — you get a link like
   `yourname-viraldesk.streamlit.app`. Open it on your phone and your PC.

**Important:** do not skip `APP_PASSWORD` — without it the site has no login
and anyone with the link can open your data. Pick a password only you know.

## Then tell Muse

Paste the Turso URL + token in chat. Your uploaded database already contains
everything (links, prompts, trend reports) — nothing further to migrate.
Muse then finishes the Streamlit deploy with you and sets the Trend Radar to
keep writing fresh trends into the same cloud database on schedule.

## How it keeps working

- **You** open the site, browse, decode, read trends. Password keeps it private.
- **Muse's machine** keeps running the Trend Radar on schedule and writes new
  trends straight into the same cloud database — they appear on your site
  automatically.
- **Video making** (previews + production) still runs on Muse's machine and
  comes to you in chat, as before.
- **Adding links on the site:** the automatic link-fetcher needs a tool that
  isn't available on free hosting, so pasted links save but fetch best on
  Muse's side for now. Everything else works fully.
