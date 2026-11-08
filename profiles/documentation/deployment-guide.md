---
id: T-004
type: reference
when: "Production deployment guide"
---
# SYSTEM DEPLOYMENT GUIDE

---

## 🚀 1. LOCAL DEVELOPMENT ENVIRONMENT
1. Clone the repository to your machine:
   ```bash
   git clone https://github.com/<your-org>/<your-repo>.git
   cd Project-Builder-4-Agents
   ```
2. Create the `.env` file from the sample file:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies and start according to the corresponding stack.

---

## 🌐 2. CLOUD FREE TIER DEPLOYMENT
* **Frontend**: Connect the repository to **Vercel**, configure environment variables and deploy automatically.
* **Backend**: Deploy on **Render.com** (using a Dockerfile or a Web Service).
* **Database**: Create a free project on **Supabase**, take the PostgreSQL Connection String and put it in `.env`.
