# Wedding E-Card: Aqil & Asyura

A pastel, nature-themed wedding invitation with three sections (welcome, event details, RSVP)
and a little bird that flies between them. Guests' RSVPs are saved to a database.

| Part | Tech | Folder | Hosted on |
| --- | --- | --- | --- |
| Frontend | Vue 3 + TypeScript + Vite | `frontend/` | Vercel |
| Backend API | FastAPI + SQLAlchemy | `backend/` | Vercel (Python) |
| Database | PostgreSQL | – | Supabase |

```
.
├── backend/
│   ├── app/
│   │   ├── domain/          # Business rules (RSVP, event). No frameworks.
│   │   ├── application/     # Use cases + interfaces (ports)
│   │   ├── infrastructure/  # Database, config, tokens, event file
│   │   ├── presentation/    # FastAPI routes and request/response schemas
│   │   ├── container.py     # Wires the layers together
│   │   └── main.py          # FastAPI app (Vercel entrypoint)
│   ├── data/event.json      # Names, date, venue, programme  ← edit this
│   └── migrations/          # SQL to run on Supabase
└── frontend/
    └── src/
        ├── domain/          # Types and form validation rules
        ├── application/     # Use cases + interfaces (ports)
        ├── infrastructure/  # HTTP calls to the API, localStorage
        ├── presentation/    # Vue components, styles, the bird
        └── main.ts          # Wires the layers together
```

---

## 1. Run it on your computer

You need **Node.js 20.19+** and **Python 3.12+**.

**Backend** (terminal 1):

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/uvicorn app.main:app --reload
```

The API runs at http://localhost:8000. Interactive docs are at http://localhost:8000/docs.
Locally it uses a SQLite file (`backend/data/wedding.db`), so you don't need Supabase yet.

**Frontend** (terminal 2):

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The dev server forwards `/api` calls to the backend.

---

## 2. Deploy

You'll create **one Supabase project** and **two Vercel projects** (one for `backend/`, one for
`frontend/`), both from the same GitHub repository.

Keep a note open as you go. You'll collect these values:

| Value | Example |
| --- | --- |
| Supabase connection URL | `postgresql://postgres.abcd...:PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres` |
| Admin key | a random string you generate |
| Backend URL | `https://wedding-backend.vercel.app` |
| Frontend URL | `https://wedding-frontend.vercel.app` |

### Step 1: Put the code on GitHub

1. Create an empty repository on https://github.com/new (private is fine). Don't add a README.
2. In this folder, run:

   ```bash
   git init
   git add .
   git commit -m "Wedding e-card"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

`.env` files, `node_modules/` and `.venv/` are ignored, so no secrets get uploaded.

### Step 2: Create the database on Supabase

1. Sign in at https://supabase.com/dashboard and click **New project**.
2. Choose a name, set a **database password** (save it in your note), and pick a region close to
   your guests, e.g. **Southeast Asia (Singapore)**. Click **Create new project** and wait for it to
   finish.
3. Create the table:
   1. Open **SQL Editor** in the left menu and click **New query**.
   2. Paste everything from [`backend/migrations/001_create_rsvps.sql`](backend/migrations/001_create_rsvps.sql).
   3. Click **Run**. You should see "Success. No rows returned".
   4. Open **Table Editor**. A table called `rsvps` should be listed.

   The script also turns on Row Level Security. That stops anyone from reading the guest list
   through Supabase's public API. Only your backend can read it.
4. Get the connection URL:
   1. Click **Connect** at the top of the project page.
   2. Find **Transaction pooler** (port **6543**) and copy the URI.
   3. Replace `[YOUR-PASSWORD]` with your database password and save the full URL in your note.

   > If your password has special characters such as `@`, `#`, `/` or `%`, they must be URL-encoded
   > (for example `@` becomes `%40`). The easiest fix is to reset the password to letters and numbers
   > only under **Project Settings → Database**.

   Use the **Transaction pooler** URL, not "Direct connection". Vercel can't reach the direct
   connection (it needs IPv6), and the pooler is built for serverless apps.

### Step 3: Deploy the backend to Vercel

1. Generate an admin key and save it in your note:

   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. Go to https://vercel.com/new and **import** your GitHub repository.
3. Configure the project:
   - **Project Name:** e.g. `wedding-backend`
   - **Root Directory:** click **Edit** and choose `backend`
   - **Framework Preset:** FastAPI (Vercel should detect it)
4. Open **Environment Variables** and add:

   | Name | Value |
   | --- | --- |
   | `WEDDING_DATABASE_URL` | the Supabase connection URL from Step 2 |
   | `WEDDING_AUTO_CREATE_SCHEMA` | `false` |
   | `WEDDING_ADMIN_API_KEY` | the admin key you generated |
   | `WEDDING_CORS_ORIGINS` | `http://localhost:5173` (you'll change this in Step 5) |

5. Click **Deploy**. When it's done, copy the domain (e.g. `https://wedding-backend.vercel.app`)
   into your note.
6. Check it works by opening these in your browser:
   - `https://<backend-url>/health` should show `{"status":"ok"}`
   - `https://<backend-url>/api/v1/event` should show the wedding details
7. Recommended: put the API in the same region as the database. Go to **Settings → Functions →
   Function Region**, choose **Singapore (sin1)** (or whichever matches your Supabase region),
   save, then redeploy (**Deployments → ⋯ → Redeploy**).

### Step 4: Deploy the frontend to Vercel

1. Go to https://vercel.com/new again and import the **same** repository.
2. Configure the project:
   - **Project Name:** e.g. `wedding-frontend`
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (detected automatically)
3. Add this environment variable:

   | Name | Value |
   | --- | --- |
   | `VITE_API_BASE_URL` | `https://<backend-url>/api/v1` |

   No trailing slash. Example: `https://wedding-backend.vercel.app/api/v1`
4. Click **Deploy** and copy the frontend domain into your note.

### Step 5: Let the frontend talk to the backend

The backend only accepts requests from websites you allow (CORS).

1. Open the **backend** project in Vercel and go to **Settings → Environment Variables**.
2. Edit `WEDDING_CORS_ORIGINS` and set it to your frontend URL, without a trailing slash:

   ```
   https://wedding-frontend.vercel.app
   ```

   To allow more than one, separate them with commas, e.g.
   `https://wedding-frontend.vercel.app,https://aqilasyura.com`.
3. Optional, for preview deployments: add `WEDDING_CORS_ORIGIN_REGEX` with
   `https://wedding-frontend-[a-z0-9-]+\.vercel\.app` (use your own project name).
4. **Redeploy the backend** (**Deployments → ⋯ → Redeploy**). Changes to environment variables only
   apply to new deployments.

### Step 6: Test it

1. Open the frontend URL. The bird should fly in and land on the branch.
2. Go to **RSVP**, fill in the form and send it. You should see the thank-you message.
3. In Supabase, open **Table Editor → rsvps**. Your test RSVP should be there.
4. See every RSVP and the total headcount:

   ```bash
   curl -H "X-Admin-Key: <your-admin-key>" https://<backend-url>/api/v1/admin/rsvps
   ```

5. Delete your test row in the Supabase Table Editor before you send the link to guests.

### Step 7 (optional): Use your own domain

In the **frontend** project, go to **Settings → Domains**, add your domain and follow the DNS
instructions. Then add that domain to `WEDDING_CORS_ORIGINS` on the backend and redeploy it
(Step 5).

---

## 3. Making changes

| What | Where | Then |
| --- | --- | --- |
| Names, date, venue, programme, RSVP deadline, max guests | `backend/data/event.json` | Push to GitHub. The backend redeploys on its own. |
| Look, text, animations | `frontend/src/presentation/` | Push to GitHub. The frontend redeploys on its own. |
| Environment variables | Vercel → Project → Settings | Redeploy that project. |

Dates in `event.json` must include the time zone offset, e.g. `2026-12-12T11:00:00+08:00`.

Every push to `main` deploys both projects. Pushes to other branches create preview deployments.

---

## 4. Troubleshooting

| Problem | What to check |
| --- | --- |
| Card says "We couldn't open the invitation" | Open `https://<backend-url>/api/v1/event`. If that works, check `VITE_API_BASE_URL` on the frontend, then redeploy the frontend. |
| Browser console shows a **CORS** error | `WEDDING_CORS_ORIGINS` must exactly match the frontend URL (`https://`, no trailing slash). Redeploy the backend after changing it. |
| Backend logs show `password authentication failed` | Wrong password in `WEDDING_DATABASE_URL`, or special characters that aren't URL-encoded. |
| Backend logs show `relation "rsvps" does not exist` | Run the SQL from Step 2.3 in the Supabase SQL Editor. |
| Backend logs show connection timeouts | Make sure you used the **Transaction pooler** URL (port `6543`), not the direct connection. |
| Admin endpoint returns 404 | `WEDDING_ADMIN_API_KEY` isn't set. Set it and redeploy. |
| Preview deployment shows a Vercel login page | Vercel protects previews by default. Production URLs are public. You can change this under **Settings → Deployment Protection**. |

Backend errors are listed in Vercel under the backend project → **Logs**.

> **Supabase free plan:** projects pause after about a week with no activity. Open the invitation
> or the Supabase dashboard now and then, or upgrade, so the database is awake when guests reply.

---

## 5. API reference

| Method | Path | Who | Purpose |
| --- | --- | --- | --- |
| GET | `/health` | anyone | Health check |
| GET | `/api/v1/event` | anyone | Wedding details shown on the card |
| POST | `/api/v1/rsvps` | anyone | Send an RSVP. Returns an `edit_token`. |
| GET | `/api/v1/rsvps/{id}` | guest (`X-Rsvp-Token` header) | Read your own RSVP |
| PUT | `/api/v1/rsvps/{id}` | guest (`X-Rsvp-Token` header) | Change your own RSVP |
| GET | `/api/v1/admin/rsvps` | couple (`X-Admin-Key` header) | All RSVPs and totals |

The RSVP endpoints are public on purpose so guests can reply without logging in. They have no rate
limit or CAPTCHA, so share the link with your guests rather than posting it publicly.
