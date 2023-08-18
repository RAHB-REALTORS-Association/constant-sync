---
title: "🛠️ Setup"
layout: page
nav_order: 1
---

# 🛠️ Setup

**1. Clone the Repository 📁**

```bash
git clone https://github.com/RAHB-REALTORS-Association/constant-sync.git
```

**2. Install Dependencies 📦**

Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

**3. Configuration 🔧**

Ensure you have your `config.py` file set up with the necessary credentials for your JSON API endpoint and Constant Contact.

**4. Running the Application 🚀**

Execute:

```bash
python app.py
```

This will start the Flask server, and you can navigate to the displayed URL to initiate the OAuth2 flow with Constant Contact.
