"""
AI Invoice Processing Agent - AI Legends 2026 Competition
=========================================================
Pipeline: Extract → Validate → Classify → Decide → Q&A
"""

import anthropic
import base64
import json
import sqlite3
import os
import re
import fitz  # PyMuPDF
from datetime import datetime
from pathlib import Path

# ============================================================
# 1. DATABASE LOADER
# ============================================================

def load_master_db(db_path):
    """Load all reference data from master database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Vendors
    cursor.execute("SELECT * FROM Vendors")
    vendors = [dict(row) for row in cursor.fetchall()]
    
    # Items
    cursor.execute("SELECT * FROM Items")
    items = [dict(row) for row in cursor.fetchall()]
    
    # Categories
    cursor.execute("SELECT * FROM InvoiceCategories")
    categories = [dict(row) for row in cursor.fetchall()]
    
    # Historical invoices with line items
    cursor.execute("""
        SELECT i.*, ic.Name as CategoryName,
               GROUP_CONCAT(il.ItemID || ':' || il.Qty || ':' || il.UnitPrice || ':' || il.Total, '|') as LineItems
        FROM Invoices i
        LEFT JOIN InvoiceCategories ic ON i.InvoiceCategoryID = ic.ID
        LEFT JOIN InvoiceLines il ON i.ID = il.InvoiceID
        GROUP BY i.ID
    """)
    historical_invoices = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "vendors": vendors,
        "items": items,
        "categories": categories,
        "historical_invoices": historical_invoices
    }


# ============================================================
# 2. FILE LOADER (JPG, PNG, PDF → base64)
# ============================================================

def load_invoice_file(filepath):
    """Load invoice file and return base64 + media type."""
    ext = Path(filepath).suffix.lower()
    
    if ext in ['.jpg', '.jpeg']:
        with open(filepath, 'rb') as f:
            data = base64.standard_b64encode(f.read()).decode('utf-8')
        return data, "image/jpeg"
    
    elif ext == '.png':
        with open(filepath, 'rb') as f:
            data = base64.standard_b64encode(f.read()).decode('utf-8')
        return data, "image/png"
    
    elif ext == '.pdf':
        # Convert PDF first page to PNG image
        doc = fitz.open(filepath)
        page = doc[0]
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        doc.close()
        data = base64.standard_b64encode(img_bytes).decode('utf-8')
        return data, "image/png"
    
    else:
        raise ValueError(f"Unsupported file type: {ext}")


# ============================================================
# 3. EXTRACTION PROMPT
# ============================================================

EXTRACTION_PROMPT = """You are an expert invoice data extraction system. Extract ALL information from this Mongolian invoice image.

Return ONLY valid JSON with this exact structure (no markdown, no explanation):
{
    "invoice_number": "string or null",
    "vendor_name": "string or null",
    "bank_name": "string or null",
    "account_number": "string or null",
    "email": "string or null",
    "invoice_date": "YYYY/MM/DD or YYYY-MM-DD or null",
    "due_date": "YYYY/MM/DD or YYYY-MM-DD or null",
    "line_items": [
        {
            "description": "string",
            "quantity": number,
            "unit_price": number,
            "total": number
        }
    ],
    "grand_total": number or null
}

Important:
- Read ALL text carefully, including handwritten text
- Numbers should be integers (no commas, no decimals unless present)
- Dates should be in YYYY/MM/DD or YYYY-MM-DD format
- Vendor names often follow pattern "Демо Компани-N"
- Bank names are like "Демо Банк 1" or "Демо Банк 2" (sometimes handwritten as "Demo bank 1/2")
- Account numbers are 10-digit numbers
- For handwritten invoices, read carefully and do your best
- Return ONLY the JSON object, nothing else
"""


# ============================================================
# 4. EXTRACTION FUNCTION
# ============================================================

def extract_invoice_data(client, filepath):
    """Use Claude Vision to extract data from invoice image."""
    img_data, media_type = load_invoice_file(filepath)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": img_data
                    }
                },
                {
                    "type": "text",
                    "text": EXTRACTION_PROMPT
                }
            ]
        }]
    )
    
    text = response.content[0].text.strip()
    # Clean potential markdown fences
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    return json.loads(text)


# ============================================================
# 5. VALIDATION FUNCTIONS
# ============================================================

def validate_invoice(extracted, master_db):
    """Run all validation checks on extracted invoice data."""
    issues = []
    
    # --- 5a. AMOUNT MISMATCH ---
    if extracted.get("line_items"):
        for i, item in enumerate(extracted["line_items"]):
            qty = item.get("quantity", 0) or 0
            unit_price = item.get("unit_price", 0) or 0
            total = item.get("total", 0) or 0
            expected = qty * unit_price
            if expected != 0 and total != 0 and expected != total:
                issues.append({
                    "type": "AMOUNT_MISMATCH",
                    "detail": f"Line {i+1}: {qty} × {unit_price} = {expected}, but invoice shows {total}"
                })
        
        # Check grand total
        line_sum = sum(item.get("total", 0) or 0 for item in extracted["line_items"])
        grand_total = extracted.get("grand_total", 0) or 0
        if line_sum != 0 and grand_total != 0 and line_sum != grand_total:
            issues.append({
                "type": "AMOUNT_MISMATCH",
                "detail": f"Sum of lines ({line_sum}) ≠ grand total ({grand_total})"
            })
    
    # --- 5b. UNREGISTERED VENDOR ---
    vendor_name = (extracted.get("vendor_name") or "").strip()
    vendor_match = None
    for v in master_db["vendors"]:
        # Flexible matching: normalize spaces, case-insensitive
        db_name = v["Name"].strip()
        if vendor_name.lower() == db_name.lower():
            vendor_match = v
            break
        # Handle OCR variations like "Демо Компани - 7" vs "Демо Компани-7"
        norm_vendor = re.sub(r'\s*[-–—]\s*', '-', vendor_name.lower())
        norm_db = re.sub(r'\s*[-–—]\s*', '-', db_name.lower())
        if norm_vendor == norm_db:
            vendor_match = v
            break
    
    if not vendor_match:
        issues.append({
            "type": "UNREGISTERED_VENDOR",
            "detail": f"Vendor '{vendor_name}' not found in master database"
        })
    
    # --- 5c. BANK ACCOUNT MISMATCH ---
    if vendor_match:
        inv_bank = (extracted.get("bank_name") or "").strip()
        inv_account = (extracted.get("account_number") or "").strip()
        db_bank = vendor_match["Bank"].strip()
        db_account = vendor_match["Account"].strip()
        
        # Normalize bank names for comparison
        def normalize_bank(name):
            name = name.lower().strip()
            name = re.sub(r'\s+', ' ', name)
            # Handle "Demo bank 2" vs "Демо Банк 2"
            name = name.replace('demo', 'демо').replace('bank', 'банк')
            return name
        
        if inv_bank and normalize_bank(inv_bank) != normalize_bank(db_bank):
            issues.append({
                "type": "BANK_ACCOUNT_MISMATCH",
                "detail": f"Bank mismatch: invoice='{inv_bank}', DB='{db_bank}'"
            })
        
        if inv_account and inv_account != db_account:
            issues.append({
                "type": "BANK_ACCOUNT_MISMATCH",
                "detail": f"Account mismatch: invoice='{inv_account}', DB='{db_account}'"
            })
    
    # --- 5d. INVALID DATE ---
    def parse_date(date_str):
        if not date_str:
            return None
        date_str = date_str.strip().replace('/', '-')
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return None
    
    inv_date = parse_date(extracted.get("invoice_date"))
    due_date = parse_date(extracted.get("due_date"))
    
    if extracted.get("invoice_date") and not inv_date:
        issues.append({
            "type": "INVALID_DATE",
            "detail": f"Cannot parse invoice date: '{extracted.get('invoice_date')}'"
        })
    
    if extracted.get("due_date") and not due_date:
        issues.append({
            "type": "INVALID_DATE",
            "detail": f"Cannot parse due date: '{extracted.get('due_date')}'"
        })
    
    if inv_date and due_date and due_date < inv_date:
        issues.append({
            "type": "INVALID_DATE",
            "detail": f"Due date ({due_date.date()}) is before invoice date ({inv_date.date()})"
        })
    
    # Check for unreasonably far future or past dates
    now = datetime(2026, 4, 29)
    if inv_date:
        if inv_date.year < 2020 or inv_date > now + __import__('datetime').timedelta(days=365):
            issues.append({
                "type": "INVALID_DATE",
                "detail": f"Invoice date {inv_date.date()} seems unreasonable"
            })
    
    # --- 5e. DUPLICATE CHECK ---
    inv_number = extracted.get("invoice_number")
    grand_total = extracted.get("grand_total", 0) or 0
    
    for hist in master_db["historical_invoices"]:
        # Check by vendor + date + total combination
        hist_vendor = (hist.get("VendorName") or "").strip().lower()
        hist_date = (hist.get("InvoiceDate") or "").strip()
        hist_total = hist.get("GrandTotal", 0) or 0
        
        if (vendor_name.lower() == hist_vendor and 
            grand_total != 0 and grand_total == hist_total):
            # Check date similarity
            inv_date_str = (extracted.get("invoice_date") or "").replace("/", "-")
            if inv_date_str == hist_date:
                issues.append({
                    "type": "DUPLICATE",
                    "detail": f"Matches historical invoice ID={hist['ID']}: same vendor, date, total"
                })
                break
    
    return issues, vendor_match


# ============================================================
# 6. CLASSIFICATION FUNCTION
# ============================================================

def classify_invoice(extracted, master_db, vendor_match):
    """Classify invoice into a financial category."""
    categories = master_db["categories"]
    items = master_db["items"]
    
    # Get line item descriptions
    descriptions = []
    if extracted.get("line_items"):
        descriptions = [item.get("description", "") for item in extracted["line_items"]]
    
    combined_desc = " ".join(descriptions).lower()
    
    # Try to match items from master item list
    matched_items = []
    for desc in descriptions:
        desc_lower = desc.lower().strip()
        for master_item in items:
            item_name_lower = master_item["ItemName"].lower()
            # Fuzzy match: check if key words overlap
            if (desc_lower in item_name_lower or 
                item_name_lower in desc_lower or
                _fuzzy_match(desc_lower, item_name_lower)):
                matched_items.append(master_item)
                break
    
    # If vendor matched, check historical category distribution
    if vendor_match:
        vendor_name = vendor_match["Name"]
        category_counts = {}
        for hist in master_db["historical_invoices"]:
            if hist.get("VendorName", "").strip() == vendor_name:
                cat_id = hist.get("InvoiceCategoryID")
                if cat_id:
                    category_counts[cat_id] = category_counts.get(cat_id, 0) + 1
        
        if category_counts:
            # Use most common category for this vendor
            best_cat_id = max(category_counts, key=category_counts.get)
            for cat in categories:
                if cat["ID"] == best_cat_id:
                    return cat["Name"], cat["ID"]
    
    # Keyword-based classification
    keyword_map = {
        1: ["түрээс", "оффис түрээс", "серверийн өрөө", "агуулах түрээс", "зогсоол", "форклифт"],
        2: ["цахилгаан", "дулаан", "ус", "хог", "цэвэрлэгээ", "харуул", "хамгаалалт", "агааржуулалт"],
        3: ["сервер", "интернэт", "лиценз", "програм", "кибер", "домэйн", "ssl", "нөөцлөлт", "вэб", "бараа бүртгэл"],
        4: ["монитор", "принтер", "камер", "кабель", "тоног"],
        5: ["тээвэр", "шатахуун", "хүргэлт", "ачаа", "гааль", "gps", "логистик"],
        6: ["агуулах", "хадгалалт", "боодол"],
        7: ["засвар", "лифт", "тагт", "цонх", "сантехник", "дээвэр", "хаалга", "зам талбай", "компьютер засвар", "техник үйлчилгээ", "барилга"],
        8: ["сургалт", "хөгжүүлэлт", "мэргэжил"],
        9: ["даатгал"],
        10: ["зөвшөөрөл", "тусгай зөвшөөрөл", "лиценз сунгалт"]
    }
    
    best_cat_id = None
    best_score = 0
    
    for cat_id, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in combined_desc)
        if score > best_score:
            best_score = score
            best_cat_id = cat_id
    
    if best_cat_id:
        for cat in categories:
            if cat["ID"] == best_cat_id:
                return cat["Name"], cat["ID"]
    
    # Default: use item DB matching
    if matched_items:
        item_id = matched_items[0]["ID"]
        # Map item to category based on item ranges
        item_cat_map = {
            range(1, 10): 3,    # IT items → МТ зардал
            range(10, 14): 4,   # Equipment
            range(14, 16): 7,   # Repairs
            range(16, 17): 8,   # Training
            range(17, 18): 10,  # License
            range(18, 19): 1,   # Office rent
            range(19, 26): 2,   # Utilities
            range(26, 35): 7,   # Repairs
            range(35, 42): 5,   # Transport
            range(42, 46): 6,   # Warehouse
            range(46, 47): 7,   # Vehicle repair
            range(47, 48): 9,   # Insurance
            range(48, 49): 1,   # Forklift rent
            range(49, 50): 3,   # Inventory system
            range(50, 51): 10,  # Special permit
        }
        for r, cat_id in item_cat_map.items():
            if item_id in r:
                for cat in categories:
                    if cat["ID"] == cat_id:
                        return cat["Name"], cat["ID"]
    
    return "Бусад", None


def _fuzzy_match(s1, s2):
    """Simple fuzzy match based on common words."""
    words1 = set(s1.split())
    words2 = set(s2.split())
    if not words1 or not words2:
        return False
    overlap = words1 & words2
    return len(overlap) >= min(2, min(len(words1), len(words2)))


# ============================================================
# 7. DECISION FUNCTION
# ============================================================

def make_decision(extracted, issues, vendor_match, master_db):
    """
    Make final business decision:
    - AUTO_POST: Known vendor, no issues, matches historical pattern
    - HUMAN_APPROVAL: New but valid invoice, minor concerns
    - DENY: Has errors, suspicious data, rule violations
    """
    
    # DENY conditions
    deny_types = {"AMOUNT_MISMATCH", "INVALID_DATE", "BANK_ACCOUNT_MISMATCH", "DUPLICATE"}
    critical_issues = [i for i in issues if i["type"] in deny_types]
    
    if critical_issues:
        reasons = [f"{i['type']}: {i['detail']}" for i in critical_issues]
        return "DENY", reasons
    
    # UNREGISTERED_VENDOR → DENY
    if any(i["type"] == "UNREGISTERED_VENDOR" for i in issues):
        return "DENY", ["UNREGISTERED_VENDOR: Vendor not in master database"]
    
    # AUTO_POST conditions: registered vendor, no issues, has historical match
    if vendor_match and len(issues) == 0:
        vendor_name = vendor_match["Name"]
        grand_total = extracted.get("grand_total", 0) or 0
        
        # Check if similar invoice pattern exists in history
        has_history = False
        for hist in master_db["historical_invoices"]:
            if hist.get("VendorName", "").strip() == vendor_name:
                has_history = True
                break
        
        if has_history:
            return "AUTO_POST", ["Registered vendor with clean history, no issues detected"]
        else:
            return "HUMAN_APPROVAL", ["Registered vendor but no historical invoices found"]
    
    # Default: HUMAN_APPROVAL
    return "HUMAN_APPROVAL", ["Requires manual review"]


# ============================================================
# 8. MAIN PIPELINE
# ============================================================

def process_single_invoice(client, filepath, master_db):
    """Process a single invoice through the full pipeline."""
    filename = os.path.basename(filepath)
    print(f"  Processing {filename}...")
    
    # Step 1: Extract
    try:
        extracted = extract_invoice_data(client, filepath)
    except Exception as e:
        print(f"    ERROR extracting {filename}: {e}")
        return {
            "filename": filename,
            "extracted": {},
            "issues": [{"type": "EXTRACTION_ERROR", "detail": str(e)}],
            "category": "Unknown",
            "decision": "DENY",
            "decision_reasons": [f"Failed to extract: {e}"]
        }
    
    # Step 2: Validate
    issues, vendor_match = validate_invoice(extracted, master_db)
    
    # Step 3: Classify
    category_name, category_id = classify_invoice(extracted, master_db, vendor_match)
    
    # Step 4: Decide
    decision, reasons = make_decision(extracted, issues, vendor_match, master_db)
    
    result = {
        "filename": filename,
        "invoice_number": extracted.get("invoice_number"),
        "vendor_name": extracted.get("vendor_name"),
        "bank_name": extracted.get("bank_name"),
        "account_number": extracted.get("account_number"),
        "email": extracted.get("email"),
        "invoice_date": extracted.get("invoice_date"),
        "due_date": extracted.get("due_date"),
        "line_items": extracted.get("line_items", []),
        "grand_total": extracted.get("grand_total"),
        "category": category_name,
        "category_id": category_id,
        "issues": issues,
        "decision": decision,
        "decision_reasons": reasons
    }
    
    print(f"    → {decision} | {category_name} | Issues: {len(issues)}")
    return result


def process_all_invoices(data_dir, db_path):
    """Process all invoices in the directory."""
    client = anthropic.Anthropic()
    master_db = load_master_db(db_path)
    
    # Get all invoice files
    invoice_files = sorted([
        os.path.join(data_dir, f) 
        for f in os.listdir(data_dir) 
        if f.startswith('invoice_') and f.split('.')[-1] in ('jpg', 'jpeg', 'png', 'pdf')
    ])
    
    print(f"Found {len(invoice_files)} invoices to process")
    print(f"Master DB: {len(master_db['vendors'])} vendors, {len(master_db['items'])} items, "
          f"{len(master_db['categories'])} categories, {len(master_db['historical_invoices'])} historical invoices\n")
    
    results = []
    for filepath in invoice_files:
        result = process_single_invoice(client, filepath, master_db)
        results.append(result)
    
    return results


# ============================================================
# 9. Q&A SYSTEM
# ============================================================

def answer_aggregate_questions(results):
    """Generate aggregate analytics from processing results."""
    total = len(results)
    auto_post = [r for r in results if r["decision"] == "AUTO_POST"]
    human_approval = [r for r in results if r["decision"] == "HUMAN_APPROVAL"]
    denied = [r for r in results if r["decision"] == "DENY"]
    
    # Issue counts
    all_issues = []
    for r in results:
        all_issues.extend(r.get("issues", []))
    
    issue_types = {}
    for issue in all_issues:
        t = issue["type"]
        issue_types[t] = issue_types.get(t, 0) + 1
    
    # Category distribution
    category_counts = {}
    for r in results:
        cat = r.get("category", "Unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Vendor distribution  
    vendor_counts = {}
    for r in results:
        v = r.get("vendor_name", "Unknown")
        vendor_counts[v] = vendor_counts.get(v, 0) + 1
    
    # Total amounts
    total_amount = sum(r.get("grand_total", 0) or 0 for r in results)
    denied_amount = sum(r.get("grand_total", 0) or 0 for r in denied)
    approved_amount = sum(r.get("grand_total", 0) or 0 for r in auto_post)
    
    summary = {
        "total_invoices": total,
        "auto_post_count": len(auto_post),
        "human_approval_count": len(human_approval),
        "deny_count": len(denied),
        "issue_breakdown": issue_types,
        "category_distribution": category_counts,
        "vendor_distribution": vendor_counts,
        "total_amount": total_amount,
        "denied_amount": denied_amount,
        "approved_amount": approved_amount,
        "duplicate_count": issue_types.get("DUPLICATE", 0),
        "unregistered_vendor_count": issue_types.get("UNREGISTERED_VENDOR", 0),
        "amount_mismatch_count": issue_types.get("AMOUNT_MISMATCH", 0),
        "bank_mismatch_count": issue_types.get("BANK_ACCOUNT_MISMATCH", 0),
        "invalid_date_count": issue_types.get("INVALID_DATE", 0),
    }
    
    return summary


def qa_chatbot(results, summary, question):
    """Answer questions about the processed results using Claude."""
    client = anthropic.Anthropic()
    
    context = f"""You are an AI invoice processing assistant. You have processed {summary['total_invoices']} invoices.

Here is the summary of results:
{json.dumps(summary, ensure_ascii=False, indent=2)}

Here are the detailed results for each invoice:
{json.dumps(results, ensure_ascii=False, indent=2)}

Answer the following question based on the data above. Be precise and provide specific numbers.
Answer in the same language as the question.
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": context + "\n\nQuestion: " + question}
        ]
    )
    
    return response.content[0].text


# ============================================================
# 10. MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    DATA_DIR = "/home/claude/competition"
    DB_PATH = os.path.join(DATA_DIR, "master_invoices_database.db")
    
    # Process all invoices
    results = process_all_invoices(DATA_DIR, DB_PATH)
    
    # Generate summary
    summary = answer_aggregate_questions(results)
    
    # Save results
    output = {
        "results": results,
        "summary": summary
    }
    
    with open("/home/claude/results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("PROCESSING COMPLETE")
    print("="*60)
    print(f"Total invoices: {summary['total_invoices']}")
    print(f"AUTO_POST: {summary['auto_post_count']}")
    print(f"HUMAN_APPROVAL: {summary['human_approval_count']}")
    print(f"DENY: {summary['deny_count']}")
    print(f"\nIssues found:")
    for issue_type, count in summary['issue_breakdown'].items():
        print(f"  {issue_type}: {count}")
    print(f"\nTotal amount: {summary['total_amount']:,}₮")
    print(f"Denied amount: {summary['denied_amount']:,}₮")
