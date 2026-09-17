# Raj Kumar Das | Personal Developer Portfolio

A complete, premium, modern, highly interactive personal developer portfolio website for **Raj Kumar Das**, B.Tech Computer Science & Engineering student at Amity University Jharkhand (Batch 2025–2029).

Built with a **Developer/Coder Aesthetic + Dark Glassmorphism + Futuristic Cyber UI + Smooth Motion + Fully Functional Backend Message Management System**.

---

## 🌟 Key Features

1. **Verified Student Information**
   - Degree: B.Tech Computer Science & Engineering
   - Institute: Amity University Jharkhand (Batch 2025–2029, 3rd Semester)
   - Location: Jharkhand, India
   - Honest representational labels (Learning, Familiar, Working Knowledge) without fabricated statistics.

2. **Futuristic Dark Glassmorphism Aesthetic**
   - Translucent glass panels with `backdrop-filter: blur()`, neon cyan/purple/emerald gradients, soft glowing elements, animated background particles, and responsive layout.

3. **Interactive Coder Identity**
   - **Hero Terminal**: Live simulated typing execution of `$ whoami`, `$ role`, `$ currently_learning`, and `$ status`.
   - **Interactive CLI Prompt**: Visitors can type real commands (`help`, `whoami`, `skills`, `projects`, `sih2026`, `contact`, `clear`, `matrix`).
   - **Developer Status Card**: Glass terminal widget displaying live student status indicator.

4. **Featured Projects**
   - **Smart Canteen**: College food pre-ordering app (Flask/JS/Bootstrap) designed for campus hostels.
   - **SentinelAI**: AI-based network security & threat forecasting system (Smart India Hackathon 2026, Team: UNCODED.SIH, PS: SIH26153, Role: Frontend Dashboard UI Design).
   - **MNIST ML Project**: Deep learning research comparing CNN, Autoencoders, SAE, and VAE models.

5. **Message Management System & Admin Dashboard**
   - Contact form sends real-time AJAX requests to `/api/contact`.
   - Messages are stored securely in a local SQLite database (`portfolio.db`).
   - Dedicated **Admin Portal** (`/admin/messages`) with secure authentication to view, mark read/unread, and delete incoming user messages!

6. **Accessibility (WCAG 2.2 AA) & Performance**
   - Keyboard accessible, focus trap on modal dialogs, skip-to-content link, `aria-live` form feedback, native `:user-invalid` form states, and support for `prefers-reduced-motion`.

---

## 🚀 How to Run the Website Locally

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Flask Server

```bash
python app.py
```

### Step 3: Open in Browser

- **Public Portfolio**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Admin Message Dashboard**: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
  - **Default Admin Username**: `admin`
  - **Default Admin Password**: `RajDevAdmin2026!`

---

## 📁 Directory Structure

```
raj-kumar-das-portfolio/
├── app.py                      # Flask Server, Routes, SQLite DB & Admin APIs
├── requirements.txt            # Python Dependencies
├── static/
│   ├── css/
│   │   ├── style.css           # Main Glassmorphism & Responsive Layout CSS
│   │   ├── terminal.css        # Interactive CLI Terminal Styling
│   │   └── admin.css           # Admin Dashboard Styling
│   ├── js/
│   │   ├── main.js             # Navigation, Canvas Particles, Modal Dialogs
│   │   ├── terminal.js         # Typewriter & CLI Execution Engine
│   │   ├── contact.js          # Contact Form AJAX & Validation
│   │   ├── github.js           # GitHub Activity Matrix Simulator
│   │   └── admin.js            # Admin Dashboard Message Handler
│   ├── images/                 # Custom SVG Visual Graphics
│   │   ├── smart-canteen.svg
│   │   ├── sentinel-ai.svg
│   │   ├── mnist-ml.svg
│   │   ├── certificate-placeholder.svg
│   │   └── avatar.svg
│   └── docs/
│       └── Raj_Kumar_Das_Resume.pdf # Sample Resume File
└── templates/
    ├── index.html              # Main Single-Page Developer Portfolio
    ├── admin.html              # Admin Message Dashboard
    └── admin_login.html        # Secure Admin Authentication Page
```
