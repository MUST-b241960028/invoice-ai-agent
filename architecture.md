# System Architecture — AI Invoice Processing Agent

## Full Pipeline Diagram

```mermaid
flowchart TD
    INPUT["📂 Invoice Input\nJPG · PNG · PDF"]

    INPUT --> SPLIT{File Type?}

    SPLIT -->|PDF| PDF["🔧 PyMuPDF\nRender page → PNG\n200 DPI"]
    SPLIT -->|JPG / PNG| IMG["🖼️ Load Image\nBase64 encode"]

    PDF --> VISION
    IMG --> VISION

    VISION["🤖 Claude Sonnet 4\nVision API\nMultimodal extraction"]

    VISION --> JSON["📋 Structured JSON\ninvoice_number · vendor_name\nbank_name · account_number\ninvoice_date · due_date\nline_items · grand_total"]

    JSON --> VAL

    subgraph VAL ["⚙️ VALIDATION ENGINE"]
        direction TB
        V1["💰 Amount Check\nqty × unit_price = line total?\nΣ lines = grand total?"]
        V2["🏢 Vendor Check\nNormalized match vs\nmaster DB vendors"]
        V3["🏦 Bank Check\nBank name + account\nvs registered records"]
        V4["📅 Date Check\nParseable? Due ≥ invoice?\nNo Feb-30?"]
        V5["🔁 Duplicate Check\nvendor + date + total\nvs 596 historical invoices"]
    end

    DB[("🗄️ Master SQLite DB\n━━━━━━━━━━━━━━\n10 Vendors\n10 Categories\n50 Items\n596 Historical Invoices")]

    DB -->|vendor list| V2
    DB -->|bank / account| V3
    DB -->|history records| V5

    V1 --> REASON
    V2 --> REASON
    V3 --> REASON
    V4 --> REASON
    V5 --> REASON

    REASON["📊 Reasoning Trace\nPer-check structured JSON:\ncompared values · pass/fail · detail"]

    REASON --> CONF["📈 Confidence Score\n0.0 → 1.0\nbased on field completeness"]

    CONF --> CLASS

    subgraph CLASS ["🏷️ CLASSIFIER"]
        direction LR
        C1["① Vendor history\n(most common category)"]
        C2["② Keyword match\n(item descriptions)"]
        C3["③ Item DB match\n(master items table)"]
        C1 --> C2 --> C3
    end

    CLASS --> DECIDE{"⚖️ DECISION ENGINE"}

    DECIDE -->|"Critical issues\nAMOUNT_MISMATCH\nBANK_MISMATCH\nINVALID_DATE\nDUPLICATE\nUNREGISTERED_VENDOR"| DENY["❌ DENY\nWith issue type\n+ reasoning trace"]

    DECIDE -->|"confidence < 0.6\nor new vendor\nor extraction failed"| HUMAN["⚠️ HUMAN APPROVAL\nManual review queue\nWith explanation"]

    DECIDE -->|"Registered vendor\nAll checks passed\nconfidence ≥ 0.6\nHas history"| AUTO["✅ AUTO POST\nAuto-approved\nWith confidence score"]

    DENY --> OUT
    HUMAN --> OUT
    AUTO --> OUT

    OUT["📁 Results\nresults.json · CSV\nPer-invoice reasoning"]

    OUT --> QA["💬 Q&A Agent\nClaude API\nAggregate analytics\nover all results"]

    QA --> ANSWERS["📣 Answers\n'How many denied?' → 28\n'Which vendor?' → Демо Компани-12\n'Why invoice_007?' → AMOUNT_MISMATCH"]
```

## Decision Logic Summary

```mermaid
flowchart LR
    I[Invoice] --> E{Any\ncritical\nissues?}
    E -->|Yes| D[❌ DENY]
    E -->|No| C{confidence\n≥ 0.6?}
    C -->|No| H[⚠️ HUMAN APPROVAL]
    C -->|Yes| V{Registered\nvendor with\nhistory?}
    V -->|No| H
    V -->|Yes| A[✅ AUTO POST]
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Vision & Q&A | Claude Sonnet 4 (Anthropic API) |
| PDF Rendering | PyMuPDF (fitz) |
| Master Database | SQLite |
| Demo UI | Streamlit |
| Chatbot Interface | React / JSX |
| Language | Python 3.10+ |
