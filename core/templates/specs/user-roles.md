# USER ROLES & PERMISSION MATRIX

---

## 👥 1. Actor Directory

| Role Code | Role Name | Description & Authority |
| :--- | :--- | :--- |
| `ROLE_ADMIN` | System Administrator | Full access to configurations, user management, audit reports, and traces |
| `ROLE_USER` | Standard User | Access to core business features and personal workspace profile |
| `ROLE_GUEST` | Unauthenticated Guest | Read-only access to public pages with rate-limited trial queries |

---

## 🔐 2. Permission Matrix

| Business Operation / Resource | Guest | Standard User | System Admin |
| :--- | :---: | :---: | :---: |
| View landing page & public documentation | ✅ | ✅ | ✅ |
| Sign in and manage active session | ❌ | ✅ | ✅ |
| Execute core AI agent operations | Limited | ✅ | ✅ |
| Manage other user accounts | ❌ | ❌ | ✅ |
| View system configuration & API keys | ❌ | ❌ | ✅ |
