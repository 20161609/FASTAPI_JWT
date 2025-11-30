# FastAPI Cookie JWT Auth

A tiny FastAPI project that demonstrates **JWT authentication stored in HttpOnly cookies**,  
with everything prefilled so you can just run it and test it with a simple `test.html` page.

- Python: **3.11**
- Auth: JWT (access + refresh)
- Storage: SQLite (`app.db`)
- Password hashing: Argon2 via `passlib`
- Cookies: `access_token`, `refresh_token` (HttpOnly)

---

## 1. Project structure

```text
FASTAPI_JWT/
├─ app/
│  ├─ main.py
│  ├─ db/
│  │  ├─ init.py
│  │  └─ model.py
│  ├─ lib/
│  │  └─ security.py
│  └─ route/
│     ├─ auth.py
│     └─ test.py
├─ static/ (mounted inside app/)
├─ test.html
├─ .gitignore
├─ .env.example
├─ requirements.txt
├─ what_is_jmt.md
└─ README.md
```

Everything is already filled in (`.env`, routes, DB models, HTML tester).

---

## 2. Environment variables (already filled)

The `.env` file is prepared with `.env.example`.
You need to create the `.env` file like this.
```
cp .env.example .env
```

```env
DATABASE_URL=sqlite:///./app.db
JWT_KEY=dev_secret_key_change_me_123456!

MAIN_EMAIL=YOUR_EMAIL
MAIN_EMAIL_PASSWORD=YOUR_EMAIL_PASSWORD

BACK_URL=http://127.0.0.1:8000
FRONTEND_ORIGIN=http://127.0.0.1:5500
```

- `YOUR_EMAIL`, `YOUR_EMAIL_PASSWORD`: fill out your individual address and password.
- `FRONTEND_ORIGIN` is exactly the origin of the static HTML server we’ll use: `http://127.0.0.1:5500`.

You can customize these later if you want; this tutorial assumes you leave them as-is.

---

## 3. Setup

From the project root (`FASTAPI_JWT`):

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

That’s it. No manual editing required.

---

## 4. Run the FastAPI backend

Still in the project root:

```bash
uvicorn app.main:app --reload
```

If everything is OK you’ll see:

```text
Connecting to database and creating models...
Application startup complete.
```

The API is now available at:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/auth/...`
- `http://127.0.0.1:8000/test/...`

---

## 5. Run the static HTML test client

We will serve `test.html` using a tiny HTTP server, so the origin becomes  
**`http://127.0.0.1:5500`**, which matches `FRONTEND_ORIGIN` in `.env`.

In another terminal (same folder):

```bash
# make sure you're in FASTAPI_JWT
python -m http.server 5500
```

Now open this in your browser:

> `http://127.0.0.1:5500/test.html`

You’ll see a super simple page with buttons for:

- **Sign Up**
- **Sign In**
- **Get Me**
- **Sign Out**

---

## 6. Auth flow — step by step using test.html

### 6.1. Sign Up

1. Open `http://127.0.0.1:5500/test.html`
2. Click **Sign Up**
3. Check the browser dev console:
   - You should see `{ status: "ok", ... }` as JSON

This creates a user with:

- email: YOUR_EMAIL
- username: `jack`
- password: `password123`

If you click it twice, the second time you’ll get “Email already registered.” — that’s expected.

---

### 6.2. Sign In (issue cookies)

1. Click **Sign In**
2. The backend will:
   - Validate email/password
   - Create an access token + refresh token
   - Store them in the DB
   - **Set them as HttpOnly cookies** on the response

You won’t see the cookies in JS (HttpOnly), but you can inspect them:

- Browser DevTools → **Application → Cookies → http://127.0.0.1:8000**

You should see `access_token` and `refresh_token`.

---

### 6.3. Get Me (use cookie authentication)

1. Click **Get Me**
2. The browser automatically sends cookies to `http://127.0.0.1:8000`
3. The backend reads the `access_token` from cookies and decodes it
4. If valid, it returns current user info:

Example JSON:

```json
{
  "uid": 1,
  "email": YOUR_EMAIL,
  "username": "jack",
  "is_active": true
}
```

No Authorization header, no manual token handling — only cookies.

---

### 6.4. Sign Out

1. Click **Sign Out**
2. The backend:
   - Deletes the token row from the DB
   - Clears both cookies
3. After that, click **Get Me** again:
   - You should get `401 Unauthorized` — you’re logged out.

---

## 7. API endpoints summary

### `POST /auth/signup`

Body:

```json
{
  "email": YOUR_EMAIL,
  "username": "jack",
  "password": "password123"
}
```

Creates a new user.

---

### `POST /auth/signin`

Body:

```json
{
  "email": YOUR_EMAIL,
  "password": "password123"
}
```

On success:

- Issues new access + refresh JWTs
- Stores them in DB
- Sends them as `HttpOnly` cookies to the browser.

---

### `GET /auth/me`

- Uses the cookie `access_token`
- Returns current user info

---

### `POST /auth/signout`

- Deletes token row from DB
- Clears cookies.

---

## 8. Notes

- This project is intentionally minimal so you can rip it apart or plug it into your own stuff.
- No Swagger/docs are required to test auth — everything is done via `test.html`.

Enjoy.  
If you break it, that’s also part of learning 🙂
