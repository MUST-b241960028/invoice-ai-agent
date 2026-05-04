# Invoice Processing Q&A

## Aggregate асуултууд

**Нийт хэдэн invoice байна вэ?**
Нийт 100 invoice байна.

**Хэдэн invoice зөв invoice вэ?**
72 invoice нь зөв (AUTO_POST). Эдгээр нь бүртгэлтэй vendor-тай, математик тооцоолол зөв, огноо хүчинтэй, банкны мэдээлэл тохирсон, давхардалгүй invoice-ууд.

**Хэдэн invoice сэжигтэй вэ?**
28 invoice сэжигтэй (DENY) болсон. Шалтгаан: BANK_ACCOUNT_MISMATCH (8), AMOUNT_MISMATCH (5), INVALID_DATE (5), UNREGISTERED_VENDOR (5), DUPLICATE (5).

**Хэдэн invoice duplicate вэ?**
5 invoice duplicate байна: invoice_025.pdf, invoice_035.pdf, invoice_038.pdf, invoice_047.pdf, invoice_057.pdf.

**Хэдэн invoice математик тооцооллын алдаатай вэ?**
5 invoice математик тооцооллын алдаатай: invoice_007.jpg, invoice_028.pdf, invoice_064.pdf, invoice_080.pdf, invoice_094.pdf.

**Хэдэн invoice бүртгэлгүй vendor-той вэ?**
5 invoice бүртгэлгүй vendor-той: invoice_010.jpg (Демо Компани-12), invoice_026.pdf (Демо Компани-11), invoice_041.pdf (Демо Компани-11), invoice_088.pdf (Демо Компани-12), invoice_092.pdf (Демо Компани-11).

**Хэдэн invoice буруу огноотой вэ?**
5 invoice буруу огноотой: invoice_005.jpg, invoice_022.pdf, invoice_034.pdf, invoice_066.pdf, invoice_087.pdf.

**Хэдэн invoice банкны мэдээллийн зөрүүтэй вэ?**
8 invoice банкны мэдээллийн зөрүүтэй: invoice_002.jpg, invoice_003.jpg, invoice_013.jpg, invoice_015.jpg, invoice_039.pdf, invoice_053.pdf, invoice_056.pdf, invoice_075.pdf.

**Хэдэн invoice зураг хэлбэртэй вэ?**
19 invoice зураг хэлбэртэй (15 JPG + 4 PNG).

**Хэдэн invoice гар бичмэлтэй зураг вэ?**
15 invoice гар бичмэлтэй зураг (JPG формат, гар утсаар зурагдсан).

**Хэдэн invoice HUMAN_APPROVAL авах ёстой вэ?**
0 invoice HUMAN_APPROVAL авах ёстой.

**Хэдэн invoice DENY болох ёстой вэ?**
28 invoice DENY болсон.

## Invoice тус бүрийн fact-check

### invoice_001.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 150,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_002.jpg
- **Final decision:** DENY
- **Vendor:** Демо Компани-10
- **Category:** Тээвэр, логистик
- **Grand total:** 2,920,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='1002033445', DB='1002233445'

### invoice_003.jpg
- **Final decision:** DENY
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 2,920,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='5003321110', DB='5003322110'

### invoice_004.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 200,000₮
- **Invoice date:** 2026-01-30
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_005.jpg
- **Final decision:** DENY
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 150,000₮
- **Invoice date:** 2026-03-01
- **Due date:** 2026-01-15
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** INVALID_DATE
- **Deny шалтгаан:** Due date (2026-01-15) is before invoice date (2026-03-01)

### invoice_006.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 150,000₮
- **Invoice date:** 2026-03-15
- **Due date:** 2026-06-01
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_007.jpg
- **Final decision:** DENY
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 2,510,000₮
- **Invoice date:** 2026-03-01
- **Due date:** 2026-04-01
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Үгүй
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** AMOUNT_MISMATCH
- **Deny шалтгаан:** Sum of lines (2500000) ≠ grand total (2510000)

### invoice_008.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 390,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_009.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 280,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_010.jpg
- **Final decision:** DENY
- **Vendor:** Демо Компани-12
- **Category:** Засвар үйлчилгээ
- **Grand total:** 300,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** UNREGISTERED_VENDOR
- **Deny шалтгаан:** Vendor 'Демо Компани-12' not found in master database

### invoice_011.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 200,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_012.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 150,000₮
- **Invoice date:** 2026-04-15
- **Due date:** 2026-05-05
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_013.jpg
- **Final decision:** DENY
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 550,000₮
- **Invoice date:** 2026-04-30
- **Due date:** 2026-06-02
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='4025544332', DB='4005544332'

### invoice_014.jpg
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 350,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_015.jpg
- **Final decision:** DENY
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 285,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='4005544584', DB='4005544332'

### invoice_016.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 350,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_017.png
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 380,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_018.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 2,500,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_019.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 200,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_020.png
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 550,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_021.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-10
- **Category:** Тээвэр, логистик
- **Grand total:** 85,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_022.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-1
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 1,200,000₮
- **Invoice date:** 2026-02-30
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** INVALID_DATE
- **Deny шалтгаан:** Cannot parse invoice date: '2026-02-30'

### invoice_023.png
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 300,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_024.png
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-4
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 75,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_025.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 450,000₮
- **Invoice date:** 2025-12-09
- **Due date:** 2025-12-24
- **Duplicate:** Тийм
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** DUPLICATE
- **Deny шалтгаан:** Matches historical invoice ID=432: same vendor, date, total

### invoice_026.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-11
- **Category:** Тээвэр, логистик
- **Grand total:** 350,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** UNREGISTERED_VENDOR
- **Deny шалтгаан:** Vendor 'Демо Компани-11' not found in master database

### invoice_027.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 200,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_028.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 190,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Үгүй
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** AMOUNT_MISMATCH
- **Deny шалтгаан:** Sum of lines (150000) ≠ grand total (190000)

### invoice_029.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 685,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_030.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 1,760,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_031.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 550,000₮
- **Invoice date:** 2026-03-20
- **Due date:** 2026-04-04
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_032.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 380,000₮
- **Invoice date:** 2026-03-23
- **Due date:** 2026-04-07
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_033.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 200,000₮
- **Invoice date:** 2026-03-23
- **Due date:** 2026-04-07
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_034.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 600,000₮
- **Invoice date:** 2026-04-10
- **Due date:** 2026-04-01
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** INVALID_DATE
- **Deny шалтгаан:** Due date (2026-04-01) is before invoice date (2026-04-10)

### invoice_035.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 855,000₮
- **Invoice date:** 2025-04-07
- **Due date:** 2025-04-22
- **Duplicate:** Тийм
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** DUPLICATE
- **Deny шалтгаан:** Matches historical invoice ID=163: same vendor, date, total

### invoice_036.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 280,000₮
- **Invoice date:** 2026-03-01
- **Due date:** 2026-03-16
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_037.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-1
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 75,000₮
- **Invoice date:** 2026-03-03
- **Due date:** 2026-03-18
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_038.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 170,000₮
- **Invoice date:** 2025-07-27
- **Due date:** 2025-08-11
- **Duplicate:** Тийм
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** DUPLICATE
- **Deny шалтгаан:** Matches historical invoice ID=157: same vendor, date, total

### invoice_039.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-10
- **Category:** Тээвэр, логистик
- **Grand total:** 2,920,000₮
- **Invoice date:** 2026-03-03
- **Due date:** 2026-03-18
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='1002233951', DB='1002233445'

### invoice_040.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 450,000₮
- **Invoice date:** 2026-04-04
- **Due date:** 2026-04-19
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_041.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-11
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 200,000₮
- **Invoice date:** 2026-04-03
- **Due date:** 2026-04-18
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** UNREGISTERED_VENDOR
- **Deny шалтгаан:** Vendor 'Демо Компани-11' not found in master database

### invoice_042.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-4
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 1,480,000₮
- **Invoice date:** 2026-03-06
- **Due date:** 2026-03-21
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_043.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 350,000₮
- **Invoice date:** 2026-03-03
- **Due date:** 2026-03-18
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_044.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 150,000₮
- **Invoice date:** 2026-03-01
- **Due date:** 2026-03-16
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_045.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-1
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 150,000₮
- **Invoice date:** 2026-03-25
- **Due date:** 2026-04-09
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_046.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 380,000₮
- **Invoice date:** 2026-04-07
- **Due date:** 2026-04-22
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_047.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-1
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 190,000₮
- **Invoice date:** 2025-04-29
- **Due date:** 2025-05-14
- **Duplicate:** Тийм
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** DUPLICATE
- **Deny шалтгаан:** Matches historical invoice ID=339: same vendor, date, total

### invoice_048.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 150,000₮
- **Invoice date:** 2026-04-01
- **Due date:** 2026-04-16
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_049.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 200,000₮
- **Invoice date:** 2026-03-06
- **Due date:** 2026-03-21
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_050.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 75,000₮
- **Invoice date:** 2026-03-03
- **Due date:** 2026-03-18
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_051.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 320,000₮
- **Invoice date:** 2026-03-15
- **Due date:** 2026-03-30
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_052.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 170,000₮
- **Invoice date:** 2026-03-27
- **Due date:** 2026-04-11
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_053.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 190,000₮
- **Invoice date:** 2026-04-02
- **Due date:** 2026-04-17
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='5003322521', DB='5003322110'

### invoice_054.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 450,000₮
- **Invoice date:** 2026-03-17
- **Due date:** 2026-04-01
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_055.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-10
- **Category:** Тээвэр, логистик
- **Grand total:** 150,000₮
- **Invoice date:** 2026-03-21
- **Due date:** 2026-04-05
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_056.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 300,000₮
- **Invoice date:** 2026-04-04
- **Due date:** 2026-04-19
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='5003322896', DB='5003322110'

### invoice_057.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 390,000₮
- **Invoice date:** 2025-05-11
- **Due date:** 2025-05-26
- **Duplicate:** Тийм
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** DUPLICATE
- **Deny шалтгаан:** Matches historical invoice ID=396: same vendor, date, total

### invoice_058.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 280,000₮
- **Invoice date:** 2026-03-23
- **Due date:** 2026-04-07
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_059.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 380,000₮
- **Invoice date:** 2026-03-18
- **Due date:** 2026-04-02
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_060.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-10
- **Category:** Тээвэр, логистик
- **Grand total:** 95,000₮
- **Invoice date:** 2026-03-27
- **Due date:** 2026-04-11
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_061.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 2,920,000₮
- **Invoice date:** 2026-04-09
- **Due date:** 2026-04-24
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_062.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-4
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 490,000₮
- **Invoice date:** 2026-03-11
- **Due date:** 2026-03-26
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_063.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 770,000₮
- **Invoice date:** 2026-03-26
- **Due date:** 2026-04-10
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_064.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 220,000₮
- **Invoice date:** 2026-03-19
- **Due date:** 2026-04-03
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Үгүй
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** AMOUNT_MISMATCH
- **Deny шалтгаан:** Sum of lines (200000) ≠ grand total (220000)

### invoice_065.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 855,000₮
- **Invoice date:** 2026-04-06
- **Due date:** 2026-04-21
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_066.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-1
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 2,920,000₮
- **Invoice date:** 2026-02-30
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** INVALID_DATE
- **Deny шалтгаан:** Cannot parse invoice date: '2026-02-30'

### invoice_067.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 280,000₮
- **Invoice date:** 2026-03-18
- **Due date:** 2026-04-02
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_068.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 75,000₮
- **Invoice date:** 2026-04-02
- **Due date:** 2026-04-17
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_069.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 380,000₮
- **Invoice date:** 2026-04-07
- **Due date:** 2026-04-22
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_070.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 545,000₮
- **Invoice date:** 2026-03-05
- **Due date:** 2026-03-20
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_071.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 790,000₮
- **Invoice date:** 2026-03-30
- **Due date:** 2026-04-14
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_072.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 350,000₮
- **Invoice date:** 2026-03-13
- **Due date:** 2026-03-28
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_073.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 350,000₮
- **Invoice date:** 2026-03-29
- **Due date:** 2026-04-13
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_074.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 2,920,000₮
- **Invoice date:** 2026-03-20
- **Due date:** 2026-04-04
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_075.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 760,000₮
- **Invoice date:** 2026-03-07
- **Due date:** 2026-03-22
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** BANK_ACCOUNT_MISMATCH
- **Deny шалтгаан:** Account mismatch: invoice='1102003272', DB='1102003004'

### invoice_076.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 400,000₮
- **Invoice date:** 2026-03-17
- **Due date:** 2026-04-01
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_077.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 200,000₮
- **Invoice date:** 2026-03-22
- **Due date:** 2026-04-06
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_078.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-4
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 535,000₮
- **Invoice date:** 2026-03-17
- **Due date:** 2026-04-01
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_079.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 190,000₮
- **Invoice date:** 2026-03-01
- **Due date:** 2026-03-16
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_080.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 2,930,000₮
- **Invoice date:** 2026-04-01
- **Due date:** 2026-04-16
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Үгүй
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** AMOUNT_MISMATCH
- **Deny шалтгаан:** Sum of lines (2920000) ≠ grand total (2930000)

### invoice_081.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 840,000₮
- **Invoice date:** 2026-03-09
- **Due date:** 2026-03-24
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_082.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-10
- **Category:** Тээвэр, логистик
- **Grand total:** 130,000₮
- **Invoice date:** 2026-03-03
- **Due date:** 2026-03-18
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_083.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 200,000₮
- **Invoice date:** 2026-03-16
- **Due date:** 2026-03-31
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_084.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-1
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 300,000₮
- **Invoice date:** 2026-04-07
- **Due date:** 2026-04-22
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_085.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-2
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 400,000₮
- **Invoice date:** 2026-03-17
- **Due date:** 2026-04-01
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_086.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 150,000₮
- **Invoice date:** 2026-03-05
- **Due date:** 2026-03-20
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_087.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 350,000₮
- **Invoice date:** 2026-02-30
- **Due date:** 2026-04-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** INVALID_DATE
- **Deny шалтгаан:** Cannot parse invoice date: '2026-02-30'

### invoice_088.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-12
- **Category:** Тээвэр, логистик
- **Grand total:** 2,920,000₮
- **Invoice date:** 2026-03-08
- **Due date:** 2026-03-23
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** UNREGISTERED_VENDOR
- **Deny шалтгаан:** Vendor 'Демо Компани-12' not found in master database

### invoice_089.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-10
- **Category:** Тээвэр, логистик
- **Grand total:** 150,000₮
- **Invoice date:** 2026-03-05
- **Due date:** 2026-03-20
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_090.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-4
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 760,000₮
- **Invoice date:** 2026-03-05
- **Due date:** 2026-03-20
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_091.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 220,000₮
- **Invoice date:** 2026-03-31
- **Due date:** 2026-04-15
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_092.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-11
- **Category:** Засвар үйлчилгээ
- **Grand total:** 130,000₮
- **Invoice date:** 2026-03-21
- **Due date:** 2026-04-05
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Үгүй
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** UNREGISTERED_VENDOR
- **Deny шалтгаан:** Vendor 'Демо Компани-11' not found in master database

### invoice_093.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 130,000₮
- **Invoice date:** 2026-03-31
- **Due date:** 2026-04-15
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_094.pdf
- **Final decision:** DENY
- **Vendor:** Демо Компани-9
- **Category:** Тээвэр, логистик
- **Grand total:** 340,000₮
- **Invoice date:** 2026-03-10
- **Due date:** 2026-03-25
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Үгүй
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** AMOUNT_MISMATCH
- **Deny шалтгаан:** Sum of lines (320000) ≠ grand total (340000)

### invoice_095.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 545,000₮
- **Invoice date:** 2026-03-28
- **Due date:** 2026-04-12
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_096.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-8
- **Category:** Тээвэр, логистик
- **Grand total:** 2,500,000₮
- **Invoice date:** 2026-03-03
- **Due date:** 2026-03-18
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_097.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-5
- **Category:** Засвар үйлчилгээ
- **Grand total:** 2,500,000₮
- **Invoice date:** 2026-03-22
- **Due date:** 2026-04-06
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_098.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-3
- **Category:** Мэдээллийн технологийн зардал
- **Grand total:** 920,000₮
- **Invoice date:** 2026-03-01
- **Due date:** 2026-03-16
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_099.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-6
- **Category:** Засвар үйлчилгээ
- **Grand total:** 235,000₮
- **Invoice date:** 2026-03-01
- **Due date:** 2026-03-16
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

### invoice_100.pdf
- **Final decision:** AUTO_POST
- **Vendor:** Демо Компани-7
- **Category:** Засвар үйлчилгээ
- **Grand total:** 200,000₮
- **Invoice date:** 2026-03-18
- **Due date:** 2026-04-02
- **Duplicate:** Үгүй
- **Bank account бүртгэлтэй:** Тийм
- **Математик тооцоолол зөв:** Тийм
- **Human approval шаардлагатай:** Үгүй
- **Илэрсэн алдаа:** Алдаа илрээгүй

