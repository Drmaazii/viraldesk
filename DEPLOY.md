# ViralDesk — put it on the web (3 steps)

Your own ViralDesk website: opens on your phone and your computer, no Muse
needed, locked with a password only you know. Everything is free.

**One honest note:** the free hosting "sleeps" when nobody opens the site.
The first open of the day takes about a minute to wake up. After that it is
fast. (This is what you chose — totally fine.)

## Step 1 — GitHub (where the code lives)

1. On your phone or computer, go to **github.com** and create a free account.
2. Tap **+** (top right) → **New repository**. Name it `viraldesk`, leave it
   Public, tap **Create repository**.
3. On the new repo page tap **uploading an existing file**, and upload all
   the files Muse prepared for you (the whole `viraldesk` folder contents).
   Then tap **Commit changes**.

## Step 2 — Turso (where your data lives)

1. Go to **turso.tech** and create a free account.
2. Create a database — call it `viraldesk`.
3. It will show you two things. **Copy both somewhere safe:**
   - the database URL (starts with `libsql://`)
   - an auth token (a long secret key)

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

## Then tell Muse

Send Muse the Turso URL + token **through the secure link** (never in chat).
Muse then copies your saved links, prompts and trend reports into the cloud
database — everything you built so far appears on the site.

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
