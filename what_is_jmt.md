# What is JWT? (Explain Like I’m 10)

> **JWT = JSON Web Token**  
> Fancy name, simple idea: it’s just a **login ticket**.

---

## 1. Theme park example 🎢

Imagine a theme park.

1. You go to the entrance and **buy a ticket**.
2. The staff writes on the ticket:
   - who you are
   - until what time you can stay
   - maybe some other info  
   and then puts a **stamp** on it.
3. After that:
   - to ride the roller coaster
   - to enter other areas  
   you just **show the ticket**.

That stamped ticket = **JWT**.

- **Server = staff**
- **JWT = ticket with a stamp**

---

## 2. What’s inside a JWT?

A JWT is just a long string, but inside there is info like:

- whose token it is (user id, email, etc.)
- when it expires
- a **signature** that proves “the real server created this”

It looks like this:

```text
aaaaaa.bbbbbb.cccccc
```

Three parts, separated by dots (`.`):

1. **Header**  
   Says: “This is a JWT and this is how it’s signed.”
2. **Payload**  
   The actual data: user id, email, roles, etc.
3. **Signature**  
   The stamp. Created using a secret key that only the server knows.

---

## 3. Why use JWT at all?

### Old way: sessions (server remembers everything)

- When you log in, the server stores something like  
  “user 1 is logged in” in its memory or database.
- With many servers, keeping that in sync becomes painful.

### JWT way: server doesn’t remember you (stateless)

1. You log in once.
2. Server checks your password.
3. If it’s correct, the server creates a **JWT** and gives it to you.
4. Now **you** keep the JWT and send it with every request.

Server logic becomes:

> “I don’t keep a big list of who is logged in.  
> Just show me the ticket (JWT) every time.”

This is called **stateless authentication**.

---

## 4. Where do we store the JWT?

There are two common places:

### 1) Local storage / session storage

```js
localStorage.setItem("token", "eyJhbGciOi...");
```

- Easy to use
- But JavaScript can read it → more vulnerable to XSS attacks

### 2) Cookies (especially HttpOnly cookies)

- Server sends: `Set-Cookie: access_token=...`
- Browser automatically attaches the cookie on each request
- With `HttpOnly`, JavaScript **cannot** read the cookie
  → harder for attackers to steal

Because of this, many apps use:

> **JWT + HttpOnly cookie**

---

## 5. One request flow example

1. Client:  
   “I want to log in!” → sends `/auth/signin` with email + password
2. Server:
   - checks password
   - creates JWT
   - sends it back (often as a cookie)
3. Browser:
   - saves the cookie
4. Next request to `/auth/me`:
   - browser automatically sends the cookie
5. Server:
   - reads JWT from cookie
   - checks the stamp (signature) and the expiry time
   - if okay → “Yes, you are user 1”

---

## 6. One-line summary ✂️

- **JWT = a signed login ticket.**
- The server signs it and gives it to you.
- You send it back with your requests.
- If the ticket is valid and not expired, you’re treated as logged in.

---

## 7. Ultra-short kid version 🤏

- JWT = “I already logged in” paper.
- Server: “If this paper has my stamp and isn’t expired, you can come in.”
- Lose the paper → log in again.
- Time over → log in again.
- Fake paper → server checks the stamp and says “nope”.

If you understand this, you already get most of what JWT is about 😄
