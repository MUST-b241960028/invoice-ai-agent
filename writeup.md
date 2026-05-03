# AI Invoice Processing Agent — AI Legends 2026

## Шийдлийн товч танилцуулга

Энэхүү систем нь 100 invoice-ийг (15 JPG гар бичмэл + 4 PNG + 81 PDF) автоматаар боловсруулж, мэдээлэл олборлох, баталгаажуулах, ангилах, шийдвэр гаргах бүрэн pipeline хэрэгжүүлсэн AI agent юм. Claude Vision API болон Python дээр суурилсан.

## Загварын архитектур болон Agent Workflow

Pipeline нь 5 үндсэн алхамтай:

**Алхам 1: Extract** — Invoice файлаас structured data олборлох. PDF файлуудад PyMuPDF ашиглан эхний хуудсыг 200 DPI-тай PNG зураг болгон хөрвүүлж, Claude Vision API-д дамжуулсан. JPG/PNG зурагуудыг шууд Claude Vision API-д base64-ээр илгээсэн. Ингэснээр гар бичмэл болон дижитал бүх төрлийн invoice-ийг нэг unified multimodal extraction pipeline-аар боловсруулсан.

**Алхам 2: Validate** — Master DB-тай тулган 5 төрлийн зөрчил шалгах. AMOUNT_MISMATCH (qty×unit_price≠total), UNREGISTERED_VENDOR (DB-д бүртгэлгүй), BANK_ACCOUNT_MISMATCH (данс/банк зөрүү), INVALID_DATE (parse алдаа, due<invoice, 2026-02-30), DUPLICATE (vendor+date+total давхцал).

**Алхам 3: Classify** — 10 санхүүгийн ангилалд хуваарилах. 3 стратеги: (1) Vendor-ийн түүхэн ангилал, (2) Keyword matching, (3) Item DB matching.

**Алхам 4: Decide** — AUTO_POST (бүртгэлтэй, алдаагүй, confidence≥0.6, түүхтэй), HUMAN_APPROVAL (шинэ vendor, confidence<0.6, extraction алдаатай), DENY (зөрчилтэй: AMOUNT_MISMATCH, BANK_MISMATCH, INVALID_DATE, DUPLICATE, UNREGISTERED_VENDOR).

**Алхам 5: Q&A** — Нийт үр дүн дээр aggregate асуултад хариулах.

## Өгөгдөл боловсруулах, шалгах стратеги

**Multimodal боловсруулалт:** 3 төрлийн файл: JPG (гар бичмэл, утасны камераар авсан зураг), PNG (дижитал template), PDF (дижитал). PDF файлуудыг PyMuPDF-ээр 200 DPI PNG болгон хөрвүүлж, JPG/PNG зурагтай хамт Claude Vision API-д base64 encode хийн дамжуулсан. Ингэснээр гар бичмэл болон дижитал бүх invoice-ийг нэг unified pipeline-аар боловсруулсан.

**Vendor тулгалт:** Regex normalize хийж (зай, тире зэргийг стандартчилсан) Master DB-ийн 10 vendor-тай харьцуулсан. Бүртгэлгүй vendor (Демо Компани-11, Демо Компани-12) илэрсэн.

**Банкны мэдээлэл шалгалт:** Банкны нэр (Демо Банк 1/2) болон 10 оронтой данс дугаарыг DB-тай тулгасан. Гар бичмэлийн OCR алдаа (жишээ: 1002033445 vs 1002233445) болон санаатай зөрүү аль алийг нь илрүүлсэн.

**Огнооны шалгалт:** 2026-02-30 (Февраль 30 гэж байхгүй), due_date < invoice_date зэрэг алдааг илрүүлсэн.

**Давхардлын шалгалт:** 596 түүхэн invoice-тай vendor+date+grand_total-аар тулгасан.

## Үнэлгээний үр дүн

| Шалгуур | Тоо |
|---------|-----|
| Нийт invoice | 100 |
| AUTO_POST (зөв) | 72 |
| HUMAN_APPROVAL | 0 |
| DENY (алдаатай/сэжигтэй) | 28 |

| Зөрчлийн төрөл | Тоо | Жишээ |
|----------------|-----|-------|
| BANK_ACCOUNT_MISMATCH | 8 | invoice_002, 003, 013, 015, 039, 053, 056, 075 |
| AMOUNT_MISMATCH | 5 | invoice_007, 028, 064, 080, 094 |
| INVALID_DATE | 5 | invoice_005, 022, 034, 066, 087 |
| UNREGISTERED_VENDOR | 5 | invoice_010, 026, 041, 088, 092 |
| DUPLICATE | 5 | invoice_025, 035, 038, 047, 057 |

| Файлын төрөл | Тоо |
|-------------|-----|
| JPG (гар бичмэл) | 15 |
| PNG (дижитал) | 4 |
| PDF (дижитал) | 81 |

## Гол дүгнэлт, хязгаарлалт, цаашдын сайжруулалт

**Гол дүгнэлт:** 100 invoice-ийн 72% нь зөв, 28% нь ямар нэг зөрчилтэй. Хамгийн түгээмэл зөрчил нь банкны дансны зөрүү (8), дараа нь математик алдаа, буруу огноо, бүртгэлгүй vendor, давхардал (тус бүр 5).

**Хязгаарлалт:** (1) Гар бичмэл OCR нарийвчлал — утасны зургаас тоо уншихад алдаа гарах магадлалтай. (2) Duplicate шалгалт нь зөвхөн яг ижил vendor+date+total дээр суурилсан. (3) Ангилал нь vendor-ийн түүхэн pattern-д хэт хамааралтай.

**Сайжруулалт:** (1) Fuzzy matching ашиглан partial duplicate илрүүлэх (одоо яг ижил vendor+date+total-аар хязгаарлагдсан). (2) Unit price-ийг Items DB-тай тулгаж нэгж үнийн зөрүү шалгах. (3) Ensemble approach: Claude Vision + regex fallback хослуулах.
