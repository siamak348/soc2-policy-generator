[README.md](https://github.com/user-attachments/files/21928010/README.md)
# SOC 2 Security Policy Template Generator

A lightweight Flask app that generates SOC 2-ready security policies from Jinja templates.  
You choose your company profile (SaaS, startup, remote-first), fill a short form, and export policies as `.docx` documents.

https://user-images.githubusercontent.com/0000000/placeholder/demo.gif

---

## ✨ Features
- Prebuilt **SOC 2 policy templates** (Access Control, Incident Response, Change Management, etc.)
- Simple **web UI** to set company name, industry, hosting model, remote policy, and timezone
- Exports **DOCX** with your company details automatically rendered
- **Extensible**: add or edit templates in `src/policies/`
- MIT licensed

---

## 🧱 Project Structure
```
soc2-policy-generator/
├── src/
│   ├── app.py
│   ├── generator.py
│   ├── config_schema.yaml
│   ├── policies/                # Jinja2 text templates
│   └── web/
│       ├── templates/           # HTML templates
│       └── static/
├── tests/
├── .github/workflows/ci.yml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start (Local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=src/app.py  # Windows: set FLASK_APP=src/app.py
flask run
```
Open: http://127.0.0.1:5000

**Docker**
```bash
docker build -t soc2-policy-generator .
docker run -p 5000:5000 soc2-policy-generator
```

---

## 🧩 Add or Edit Policy Templates
1. Create a new file in `src/policies/` like `logging_monitoring.j2`.
2. Use Jinja variables such as `{{ company.name }}`, `{{ company.timezone }}`, `{{ controls.access_review_frequency }}`.
3. The generator will automatically include it in the UI list.

---

## ✅ Templates Included
- Access Control
- Incident Response
- Change Management
- Vendor Management
- Data Retention & Disposal
- Encryption
- Backup & Recovery
- Business Continuity & Disaster Recovery
- Logging & Monitoring
- Acceptable Use

---

## 🧪 Tests (basic smoke)
```bash
pytest
```

---

## 📄 Export
Click **Generate DOCX** to download a zipped set of `.docx` files (one per policy) in `/exports/YYYYmmdd-HHMMSS/`

---

## 🤝 Contributing
PRs welcome! Update or add templates, improve controls and defaults, or add export to PDF.

---
