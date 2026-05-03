# AI Invoice Processing Agent — AI Legends 2026

## Шийдлийн товч танилцуулга

Байгууллагуудад invoice боловсруулалт нь цаг хугацаа их шаардах, алдаа гаргах магадлал өндөр гар ажиллагааны процесс байдаг. Энэхүү систем нь тэр процессыг бүрэн автоматжуулах **AI agent** юм — хэрэглэгч invoice файл upload хийхэд агент дангаараа уншиж, баталгаажуулж, ангилаад, шийдвэр гаргаж өгнө.

Claude Vision API болон Python дээр суурилсан бөгөөд JPG гар бичмэл, PNG, PDF гэсэн бүх форматтай invoice-ийг нэгдсэн pipeline-аар боловсруулдаг.

## Агент яаж ажилладаг вэ?

Pipeline нь 5 үндсэн алхамтай:

**Алхам 1: Extract** — Invoice файлаас structured data автоматаар олборлох. PDF-ийг PyMuPDF-ээр 200 DPI PNG болгон хөрвүүлж, JPG/PNG зурагтай хамт Claude Vision API-д base64-ээр дамжуулна. Нэг unified multimodal pipeline нь гар бичмэл болон дижитал бүх invoice-ийг боловсруулдаг — тусдаа OCR эсвэл template хэрэггүй.

**Алхам 2: Validate** — Олборлосон мэдээллийг Master DB-тай тулган 5 төрлийн зөрчил автоматаар шалгана:
- **AMOUNT_MISMATCH** — qty × unit_price ≠ total
- **UNREGISTERED_VENDOR** — DB-д бүртгэлгүй нийлүүлэгч
- **BANK_ACCOUNT_MISMATCH** — данс/банк DB-тай таарахгүй
- **INVALID_DATE** — parse алдаа, due < invoice, 2026-02-30 гэх мэт боломжгүй огноо
- **DUPLICATE** — 596 түүхэн invoice-тай vendor+date+total-аар тулгасан давхардал

Шалгалт бүр дэлгэрэнгүй reasoning trace буцаана тул яагаад тэр шийдвэр гарсан нь тайлбарлагдана.

**Алхам 3: Classify** — Invoice-ийг 10 санхүүгийн ангилалд хуваарилна. 3 давхар стратеги: (1) Vendor-ийн түүхэн ангиллын pattern, (2) Keyword matching, (3) Item DB тулгалт — нэг нь амжилтгүй болсон ч нөгөө нь ажиллана.

**Алхам 4: Decide** — Шалгалтын үр дүн болон confidence score-д үндэслэн эцсийн шийдвэр гаргана:
- **AUTO_POST** — бүртгэлтэй vendor, бүх шалгалт давсан, confidence ≥ 0.6, түүхтэй
- **HUMAN_APPROVAL** — шинэ vendor, confidence < 0.6, extraction алдаатай
- **DENY** — зөрчил илэрсэн (AMOUNT_MISMATCH, BANK_MISMATCH, INVALID_DATE, DUPLICATE, UNREGISTERED_VENDOR)

**Алхам 5: Q&A** — Боловсруулсан бүх invoice дээр aggregate асуултад хариулна. "Хэдэн invoice DENY болсон?", "Банкны зөрүүтэй invoice хэд?" гэх мэт асуултад тоо, дэлгэрэнгүй жишээгээр хариулна.

## Хэрэглэгч яаж ашиглах вэ?

Систем нь **хоёр интерфэйстэй**:

### 1. Streamlit web app (`app.py`)
Гурван tab-тай:
- **Upload & Analyze** — Invoice file upload хийхэд Claude Vision API уншиж, шалгалт хийж, шийдвэрийг дэлгэцэнд харуулна. PDF бол эхний хуудасны preview-г зэрэг харуулна.
- **100 Invoice Results** — Нийт үнэлгээний дүн: AUTO_POST/DENY/HUMAN_APPROVAL тоо, зөрчлийн тархалт, deny болсон invoice-ийн жагсаалт.
- **Q&A Chat** — Claude AI-тай invoice дата дээр чөлөөт асуулт хариулт. Mongolian болон English хэл аль алинд хариулна.

### 2. Batch pipeline (`pipeline.py`)
Олон invoice-ийг нэг дор боловсруулах командын мөрийн хэрэгсэл. Eval dataset дээр `DATA_DIR` зааж өгөхөд бүх файлыг scan хийж, `full_results.json` болон CSV export хийнэ.

## Техникийн архитектур

```
Invoice (JPG/PNG/PDF)
        │
        ▼
[PyMuPDF: PDF→PNG 200DPI]   [JPG/PNG шууд]
        │                          │
        └──────────┬───────────────┘
                   ▼
        [Claude Sonnet 4 Vision API]
        [Base64 → Structured JSON]
                   │
                   ▼
        [Validate — 5 шалгалт]
        [Master DB: 10 vendors, 596 history]
        [Reasoning trace буцаана]
                   │
                   ▼
        [Classify — 10 category]
        [Vendor history + Keyword + Items DB]
                   │
                   ▼
        [Confidence Score 0.0–1.0]
        [Key field completeness]
                   │
                   ▼
        [Decision Engine]
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    AUTO_POST  HUMAN_APPROVAL  DENY
                   │
                   ▼
        [Q&A Agent — Claude API]
        [Aggregate analytics]
```

## Яагаад Claude Vision вэ?

- Гар бичмэл invoice (JPG, утасны камераар авсан) болон дижитал PDF-ийг ижил pipeline-аар боловсруулна — тусдаа OCR систем хэрэггүй
- Монгол хэлний invoice-ийг нэмэлт тохиргоогүй уншина
- Нэг API call-д vendor нэр, данс, огноо, бараа жагсаалт, дүн зэрэг бүх талбарыг нэгэн зэрэг олборлоно
- Extraction алдаатай эсвэл confidence бага бол HUMAN_APPROVAL руу чиглүүлж, нуугдмал алдаа гарахаас сэргийлнэ

## Үнэлгээний үр дүн (100 нийтийн dataset)

| Шалгуур | Тоо |
|---------|-----|
| Нийт invoice | 100 |
| AUTO_POST | 72 |
| HUMAN_APPROVAL | 0* |
| DENY | 28 |

*Нийтийн 100 invoice бүгд бүртгэлтэй vendor-тай, confidence өндөртэй байсан тул HUMAN_APPROVAL гараагүй. Eval dataset дээр extraction алдаатай эсвэл шинэ vendor байвал HUMAN_APPROVAL ажиллана.

| Зөрчлийн төрөл | Тоо |
|----------------|-----|
| BANK_ACCOUNT_MISMATCH | 8 |
| AMOUNT_MISMATCH | 5 |
| INVALID_DATE | 5 |
| UNREGISTERED_VENDOR | 5 |
| DUPLICATE | 5 |

## Хязгаарлалт ба цаашдын сайжруулалт

**Хязгаарлалт:**
1. Гар бичмэл OCR нарийвчлал — утасны зургаас тоо уншихад алдаа гарах магадлалтай (жишээ: 1002033445 vs 1002233445)
2. Duplicate шалгалт нь яг ижил vendor+date+total-д тулгуурладаг — fuzzy partial duplicate илрүүлдэггүй
3. Ангилал нь vendor-ийн түүхэн pattern-д тулгуурладаг тул шинэ vendor-д keyword fallback хэрэглэнэ

**Цаашдын сайжруулалт:**
1. Fuzzy matching ашиглан partial duplicate илрүүлэх
2. Unit price-ийг Items DB-тай тулгаж нэгж үнийн зөрүү шалгах
3. Multi-page PDF дэмжих (одоо зөвхөн эхний хуудас)
