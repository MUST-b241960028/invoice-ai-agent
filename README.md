# Smart Invoice Agent — AI Legends 2026

AI-powered invoice processing agent that extracts, validates, classifies, and makes decisions on Mongolian financial invoices using Claude Vision API.

## Pipeline Architecture

```
Invoice (JPG/PNG/PDF)
        │
        ▼
  1. EXTRACT    ← Claude Vision API → structured JSON
        │
        ▼
  2. VALIDATE   ← 5 checks against SQLite master DB
        │
        ▼
  3. CLASSIFY   ← 10 financial categories
        │
        ▼
  4. DECIDE     ← AUTO_POST / HUMAN_APPROVAL / DENY
        │
        ▼
  5. Q&A        ← Aggregate analytics via Claude API
```

## Validation Checks

| Check | Description |
|-------|-------------|
| `AMOUNT_MISMATCH` | qty × unit_price ≠ line total, or sum ≠ grand_total |
| `UNREGISTERED_VENDOR` | Vendor not in master database |
| `BANK_ACCOUNT_MISMATCH` | Bank/account doesn't match vendor record |
| `INVALID_DATE` | Unparseable date, Feb-30, or due < invoice date |
| `DUPLICATE` | Same vendor + date + total in historical data |

## Results (100 Invoices Processed)

| Decision | Count |
|----------|-------|
| AUTO_POST | 72 |
| DENY | 28 |
| HUMAN_APPROVAL | 0 |

| Issue Type | Count | Invoice Numbers |
|------------|-------|-----------------|
| BANK_ACCOUNT_MISMATCH | 8 | 002, 003, 013, 015, 039, 053, 056, 075 |
| AMOUNT_MISMATCH | 5 | 007, 028, 064, 080, 094 |
| INVALID_DATE | 5 | 005, 022, 034, 066, 087 |
| UNREGISTERED_VENDOR | 5 | 010, 026, 041, 088, 092 |
| DUPLICATE | 5 | 025, 035, 038, 047, 057 |

- Total amount: **66,110,000₮**
- Denied amount: **28,210,000₮**
- File types: JPG handwritten (15), PNG digital (4), PDF digital (81)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Run Pipeline

```bash
python pipeline.py
```

## Run Streamlit Demo

```bash
streamlit run app.py
```

## Tech Stack

- **Claude Sonnet 4** — Vision extraction + Q&A reasoning
- **PyMuPDF** — PDF page rendering
- **SQLite** — Master vendor/items/history database
- **Streamlit** — Interactive demo UI
- **React/JSX** — Chatbot interface (`invoice_agent_chatbot.jsx`)

## Files

| File | Description |
|------|-------------|
| `pipeline.py` | Core 5-step processing pipeline |
| `app.py` | Streamlit demo application |
| `invoice_agent_chatbot.jsx` | React chatbot component |
| `requirements.txt` | Python dependencies |

## Competition

AI Legends 2026 — AI Agent Automation Track
Organized by Prof. D.Zolzaya, MUST
