"""
AI Invoice Processing Agent — AI Legends 2026
Run: streamlit run app.py
Deploy: streamlit.io → add ANTHROPIC_API_KEY to secrets
"""
import streamlit as st, anthropic, base64, csv, json, sqlite3, re, os, fitz
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="AI Нэхэмжлэхийн Агент", page_icon="🧾", layout="wide")

# API KEY
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Anthropic API Key", type="password")
if not api_key:
    st.warning("👈 API key оруулна уу"); st.stop()
client = anthropic.Anthropic(api_key=api_key)

# DB
DB_PATH = Path(__file__).parent / "master_invoices_database.db"
@st.cache_resource
def load_db():
    conn = sqlite3.connect(str(DB_PATH)); conn.row_factory = sqlite3.Row; c = conn.cursor()
    c.execute("SELECT * FROM Vendors"); vendors = [dict(r) for r in c.fetchall()]
    c.execute("SELECT * FROM InvoiceCategories"); categories = [dict(r) for r in c.fetchall()]
    c.execute("SELECT i.*, ic.Name as CategoryName, v.Account as VendorAccount FROM Invoices i LEFT JOIN InvoiceCategories ic ON i.InvoiceCategoryID=ic.ID LEFT JOIN Vendors v ON i.VendorName=v.Name")
    historical = [dict(r) for r in c.fetchall()]; conn.close()
    return {"vendors":vendors,"categories":categories,"historical_invoices":historical}
master_db = load_db()

RESULTS_PATH = Path(__file__).parent / "full_results.json"
RESULTS_CSV_PATH = Path(__file__).parent / "invoice_results.csv"

def load_initial_results():
    if not RESULTS_PATH.exists():
        return []
    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("results", [])

def issue_type(issue):
    return issue.get("type") or issue.get("t") or "UNKNOWN"

def issue_detail(issue):
    return issue.get("detail") or issue.get("d") or ""

def summarize_results(results):
    issue_counts = {}
    for r in results:
        for issue in r.get("issues") or []:
            t = issue_type(issue)
            issue_counts[t] = issue_counts.get(t, 0) + 1
    denied = [r for r in results if r.get("decision") == "DENY"]
    return {
        "total": len(results),
        "auto": sum(1 for r in results if r.get("decision") == "AUTO_POST"),
        "deny": len(denied),
        "approval": sum(1 for r in results if r.get("decision") == "HUMAN_APPROVAL"),
        "issues": issue_counts,
        "jpg": sum(1 for r in results if str(r.get("file_type") or r.get("filename","").split(".")[-1]).upper() in ("JPG", "JPEG")),
        "png": sum(1 for r in results if str(r.get("file_type") or r.get("filename","").split(".")[-1]).upper() == "PNG"),
        "pdf": sum(1 for r in results if str(r.get("file_type") or r.get("filename","").split(".")[-1]).upper() == "PDF"),
        "handwritten": sum(1 for r in results if r.get("is_handwritten") is True),
        "total_amount": sum(r.get("grand_total") or 0 for r in results),
        "denied_amount": sum(r.get("grand_total") or 0 for r in denied),
    }

def full_summary(results):
    s = summarize_results(results)
    issues = s["issues"]
    return {
        "total_invoices": s["total"],
        "auto_post_count": s["auto"],
        "human_approval_count": s["approval"],
        "deny_count": s["deny"],
        "issue_breakdown": issues,
        "total_amount": s["total_amount"],
        "denied_amount": s["denied_amount"],
        "jpg_count": s["jpg"],
        "png_count": s["png"],
        "pdf_count": s["pdf"],
        "handwritten_count": s["handwritten"],
        "duplicate_count": issues.get("DUPLICATE", 0),
        "unregistered_vendor_count": issues.get("UNREGISTERED_VENDOR", 0),
        "amount_mismatch_count": issues.get("AMOUNT_MISMATCH", 0),
        "bank_mismatch_count": issues.get("BANK_ACCOUNT_MISMATCH", 0),
        "invalid_date_count": issues.get("INVALID_DATE", 0),
    }

def line_items_total(record):
    return sum((li.get("total") or 0) for li in record.get("line_items") or [])

def persist_results(results):
    output = {"results": results, "summary": full_summary(results)}
    if RESULTS_PATH.exists():
        try:
            existing = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
            if "qa_answers" in existing:
                output["qa_answers"] = existing["qa_answers"]
        except Exception:
            pass
    RESULTS_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    fieldnames = [
        "Filename", "Invoice#", "Vendor", "Bank", "Account", "Email",
        "Invoice_Date", "Due_Date", "Grand_Total", "Category", "Decision",
        "Issues", "Issue_Details", "File_Type", "Handwritten",
        "Line_Items_Count", "Line_Items_Total"
    ]
    with RESULTS_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            issues = r.get("issues") or []
            writer.writerow({
                "Filename": r.get("filename"),
                "Invoice#": r.get("invoice_number"),
                "Vendor": r.get("vendor_name"),
                "Bank": r.get("bank_name"),
                "Account": r.get("account_number"),
                "Email": r.get("email"),
                "Invoice_Date": r.get("invoice_date"),
                "Due_Date": r.get("due_date"),
                "Grand_Total": r.get("grand_total"),
                "Category": r.get("category"),
                "Decision": r.get("decision"),
                "Issues": ", ".join(issue_type(i) for i in issues),
                "Issue_Details": " | ".join(issue_detail(i) for i in issues),
                "File_Type": r.get("file_type"),
                "Handwritten": r.get("is_handwritten"),
                "Line_Items_Count": len(r.get("line_items") or []),
                "Line_Items_Total": line_items_total(r),
            })

def compact_results(results):
    compact = []
    for r in results:
        issues = r.get("issues") or []
        duplicate_issue = next((i for i in issues if issue_type(i) == "DUPLICATE"), None)
        compact.append({
            "filename": r.get("filename"),
            "invoice_number": r.get("invoice_number"),
            "vendor_name": r.get("vendor_name"),
            "category": r.get("category"),
            "decision": r.get("decision"),
            "due_date": r.get("due_date"),
            "invoice_date": r.get("invoice_date"),
            "grand_total": r.get("grand_total"),
            "bank_name": r.get("bank_name"),
            "account_number": r.get("account_number"),
            "file_type": r.get("file_type"),
            "is_handwritten": r.get("is_handwritten"),
            "duplicate": any(issue_type(i) == "DUPLICATE" for i in issues),
            "bank_account_registered": not any(issue_type(i) == "BANK_ACCOUNT_MISMATCH" for i in issues),
            "math_correct": not any(issue_type(i) == "AMOUNT_MISMATCH" for i in issues),
            "human_approval_required": r.get("decision") == "HUMAN_APPROVAL",
            "issue_types": [issue_type(i) for i in issues],
            "issue_details": [issue_detail(i) for i in issues],
            "duplicate_with": duplicate_issue.get("matched_invoice") if duplicate_issue else None,
            "deny_reasons": r.get("decision_reasons") or [issue_detail(i) for i in issues],
        })
    return compact

def normalized_line_items(record):
    items = []
    for item in record.get("line_items") or []:
        desc = re.sub(r"\s+", " ", (item.get("description") or "").strip().lower())
        items.append((
            desc,
            item.get("quantity") or 0,
            item.get("unit_price") or 0,
            item.get("total") or 0,
        ))
    return tuple(sorted(items))

def normalized_invoice_fingerprint(record):
    vendor = re.sub(r"\s*[-–—]\s*", "-", (record.get("vendor_name") or "").strip().lower())
    invoice_date = (record.get("invoice_date") or "").replace("/", "-")
    total = record.get("grand_total") or 0
    account = (record.get("account_number") or "").strip()
    line_items = normalized_line_items(record)
    if not vendor or not invoice_date or not total:
        return None
    return vendor, invoice_date, total, account, line_items

def normalized_business_key(record):
    vendor = re.sub(r"\s*[-–—]\s*", "-", (record.get("vendor_name") or "").strip().lower())
    invoice_date = (record.get("invoice_date") or "").replace("/", "-")
    total = record.get("grand_total") or 0
    if not vendor or not invoice_date or not total:
        return None
    return vendor, invoice_date, total

def find_duplicate_result(extracted):
    fingerprint = normalized_invoice_fingerprint(extracted)
    business_key = normalized_business_key(extracted)
    if not business_key:
        return None
    for existing in st.session_state.get("invoice_results", []):
        if fingerprint and normalized_invoice_fingerprint(existing) == fingerprint:
            return existing, "exact_content"
    for existing in st.session_state.get("invoice_results", []):
        if normalized_business_key(existing) == business_key:
            return existing, "same_vendor_date_total"
    return None

def duplicate_match_payload(record):
    if not record:
        return None
    return {
        "filename": record.get("filename"),
        "invoice_number": record.get("invoice_number"),
        "vendor_name": record.get("vendor_name"),
        "invoice_date": record.get("invoice_date"),
        "grand_total": record.get("grand_total"),
    }

def validate(data):
    issues = []
    for i,li in enumerate(data.get("line_items") or []):
        exp=(li.get("quantity") or 0)*(li.get("unit_price") or 0); tot=li.get("total") or 0
        if exp and tot and exp!=tot: issues.append({"type":"AMOUNT_MISMATCH","detail":f"Line {i+1}: {li.get('quantity')}×{li.get('unit_price'):,}={exp:,}, shows {tot:,}"})
    ls=sum((li.get("total") or 0) for li in data.get("line_items") or []); gt=data.get("grand_total") or 0
    if ls and gt and ls!=gt: issues.append({"type":"AMOUNT_MISMATCH","detail":f"Sum {ls:,} ≠ total {gt:,}"})
    vname=re.sub(r"\s*[-–—]\s*","-",(data.get("vendor_name") or "").strip().lower())
    vendor=next((v for v in master_db["vendors"] if re.sub(r"\s*[-–—]\s*","-",v["Name"].lower())==vname),None)
    if not vendor: issues.append({"type":"UNREGISTERED_VENDOR","detail":f"'{data.get('vendor_name')}' not in DB"})
    if vendor:
        inv_acc=(data.get("account_number") or "").strip()
        if inv_acc and inv_acc!=vendor["Account"]: issues.append({"type":"BANK_ACCOUNT_MISMATCH","detail":f"Account: {inv_acc} vs DB: {vendor['Account']}"})
    def pd(s):
        if not s: return None
        try: return datetime.strptime(s.replace("/","-"),"%Y-%m-%d")
        except: return None
    id_,dd_=pd(data.get("invoice_date")),pd(data.get("due_date"))
    if data.get("invoice_date") and not id_: issues.append({"type":"INVALID_DATE","detail":f"Cannot parse '{data.get('invoice_date')}'"})
    if id_ and dd_ and dd_<id_: issues.append({"type":"INVALID_DATE","detail":"Due date before invoice date"})
    if (data.get("invoice_date") or "").replace("/","-").endswith("02-30"): issues.append({"type":"INVALID_DATE","detail":"Feb 30 does not exist"})
    existing_duplicate = find_duplicate_result(data)
    if existing_duplicate:
        existing_record, match_type = existing_duplicate
        matched = duplicate_match_payload(existing_record)
        label = matched.get("filename") or f"invoice #{matched.get('invoice_number')}"
        if match_type == "exact_content":
            detail = f"Өмнө хадгалсан {label} нэхэмжлэхтэй яг ижил агуулгатай байна: vendor + огноо + дүн + данс + мөрүүд ижил"
        else:
            detail = f"Өмнө хадгалсан {label} нэхэмжлэхтэй давхцах магадлалтай: vendor + огноо + дүн ижил"
        issues.append({
            "type":"DUPLICATE",
            "detail":detail,
            "match_type":match_type,
            "matched_invoice": matched,
        })
    else:
        for h in master_db["historical_invoices"]:
            if str(h.get("VendorName","")).strip().lower()==(data.get("vendor_name") or "").strip().lower() and gt and gt==(h.get("GrandTotal") or 0) and (data.get("invoice_date") or "").replace("/","-")==(h.get("InvoiceDate") or ""):
                issues.append({
                    "type":"DUPLICATE",
                    "detail":f"Мастер DB дахь historical invoice ID={h['ID']} бичлэгтэй давхцаж байна: vendor + огноо + дүн ижил",
                    "matched_invoice":{"historical_id":h["ID"],"vendor_name":h.get("VendorName"),"invoice_date":h.get("InvoiceDate"),"grand_total":h.get("GrandTotal")},
                }); break
    deny={"AMOUNT_MISMATCH","BANK_ACCOUNT_MISMATCH","UNREGISTERED_VENDOR","INVALID_DATE","DUPLICATE"}
    decision="DENY" if any(i["type"] in deny for i in issues) else ("AUTO_POST" if vendor else "HUMAN_APPROVAL")
    return issues,decision,vendor

def classify(data,vendor):
    desc=" ".join((li.get("description") or "") for li in data.get("line_items") or []).lower()
    if vendor:
        cc={}
        for h in master_db["historical_invoices"]:
            if str(h.get("VendorName","")).strip()==vendor["Name"]:
                cid=h.get("InvoiceCategoryID")
                if cid: cc[cid]=cc.get(cid,0)+1
        if cc:
            best=max(cc,key=cc.get); cat=next((c["Name"] for c in master_db["categories"] if c["ID"]==best),None)
            if cat: return cat
    kw={"Тээвэр, логистик":["тээвэр","шатахуун","хүргэлт","ачаа","гааль","логистик"],"Засвар үйлчилгээ":["засвар","лифт","сантехник","дээвэр","техник","барилга","цэвэрлэгээ"],"МТ зардал":["сервер","интернэт","лиценз","програм","кибер","домэйн","ssl","монитор","принтер"],"Түрээсийн зардал":["түрээс","оффис","форклифт"],"Даатгал":["даатгал"],"Ашиглалтын зардал":["цахилгаан","дулаан","ус","хог"]}
    best,bestN="Бусад",0
    for cat,words in kw.items():
        n=sum(1 for w in words if w in desc)
        if n>bestN: best,bestN=cat,n
    return best

PROMPT='Extract ALL data from this Mongolian invoice. Return ONLY JSON (no markdown): {"invoice_number":"str","vendor_name":"str","bank_name":"str","account_number":"str","email":"str","invoice_date":"YYYY-MM-DD","due_date":"YYYY-MM-DD","line_items":[{"description":"str","quantity":number,"unit_price":number,"total":number}],"grand_total":number}. Read handwriting carefully.'

def process(fb,ft):
    if ft=="application/pdf":
        doc=fitz.open(stream=fb,filetype="pdf"); ib=doc[0].get_pixmap(dpi=200).tobytes("png"); doc.close(); mt="image/png"
    else: ib=fb; mt="image/jpeg" if ft in ["image/jpeg","image/jpg"] else "image/png"
    b64=base64.standard_b64encode(ib).decode()
    resp=client.messages.create(model="claude-sonnet-4-20250514",max_tokens=2000,messages=[{"role":"user","content":[{"type":"image","source":{"type":"base64","media_type":mt,"data":b64}},{"type":"text","text":PROMPT}]}])
    text=resp.content[0].text.strip().replace("```json","").replace("```","").strip()
    return json.loads(text)

if "invoice_results" not in st.session_state:
    st.session_state.invoice_results = load_initial_results()
if "processed_uploads" not in st.session_state:
    st.session_state.processed_uploads = []
if "ch" not in st.session_state:
    st.session_state.ch = [{
        "role": "assistant",
        "content": "Сайн байна уу. Нэхэмжлэхийн үр дүн, DENY шалтгаан, давхардал, тооцооллын алдаа, vendor эсвэл тайлангийн хэсгүүдийн талаар асуугаарай."
    }]

def build_chat_context():
    return f"""You are an AI Invoice Agent for a Mongolian invoice-processing demo.
Use ONLY the data below. Answer in the same language as the question.
Support aggregate analytics, invoice-specific fact-checks, and report/submission sections.

Aggregate topics: total invoices, AUTO_POST, DENY, HUMAN_APPROVAL, duplicates, amount mismatch,
unregistered vendors, invalid dates, bank/account mismatches, image counts, handwritten counts.

Fact-check topics: final decision, duplicate status, vendor, category, due date, bank account match,
deny reason, issue types, human approval, math correctness.

Summary:
{json.dumps(summarize_results(st.session_state.invoice_results),ensure_ascii=False,indent=2)}

Invoice records:
{json.dumps(compact_results(st.session_state.invoice_results),ensure_ascii=False,indent=2)}
"""

def ask_agent(question):
    resp=client.messages.create(model="claude-sonnet-4-20250514",max_tokens=900,messages=[{"role":"user","content":build_chat_context()+"\n\nQ: "+question}])
    return resp.content[0].text

def render_invoice_result(record):
    issue_names=", ".join(issue_type(i) for i in record.get("issues",[])) or "Байхгүй"
    issue_details="\n".join(f"- {issue_type(i)}: {issue_detail(i)}" for i in record.get("issues",[]))
    return f"""**{record.get('filename','uploaded invoice')}**

Vendor: {record.get('vendor_name') or '?'}  
Дүн: {(record.get('grand_total') or 0):,}₮  
Огноо: {record.get('invoice_date') or '?'} -> {record.get('due_date') or '?'}  
Ангилал: {record.get('category') or '?'}  
Шийдвэр: **{record.get('decision')}**  
Алдаа: {issue_names}
{issue_details}
"""

def process_upload(uploaded_file):
    fb=uploaded_file.read()
    ext=process(fb,uploaded_file.type)
    issues,decision,vendor=validate(ext)
    cat=classify(ext,vendor)
    file_ext=Path(uploaded_file.name).suffix.lower().lstrip(".")
    record={**ext,"filename":uploaded_file.name,"category":cat,"decision":decision,"issues":issues,"file_type":file_ext.upper(),"is_handwritten":file_ext in ["jpg","jpeg"],"decision_reasons":[issue_detail(i) for i in issues] or ["Registered vendor, all checks passed"]}
    st.session_state.invoice_results.append(record)
    st.session_state.processed_uploads.insert(0,record)
    st.session_state.ch.append({"role":"assistant","content":render_invoice_result(record)})
    persist_results(st.session_state.invoice_results)
    return record

# UI
st.markdown("""
<style>
    .stApp { background: #ffffff; }
    [data-testid="stSidebar"] { background: #f7f7f8; border-right: 1px solid #e5e7eb; }
    .block-container { max-width: 1060px; padding-top: 1.25rem; padding-bottom: 5rem; }
    .topbar { display: flex; align-items: center; gap: 12px; padding-bottom: 16px; border-bottom: 1px solid #e5e7eb; margin-bottom: 16px; }
    .brand { width: 34px; height: 34px; border-radius: 8px; background: #111827; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; }
    .topbar h1 { margin: 0; font-size: 24px; letter-spacing: 0; }
    .topbar p { margin: 2px 0 0; color: #6b7280; font-size: 13px; }
    .metric-strip { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-bottom: 18px; }
    .metric-card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px 14px; background: #fff; }
    .metric-card .label { color: #6b7280; font-size: 12px; margin-bottom: 5px; }
    .metric-card .value { color: #111827; font-size: 22px; font-weight: 700; }
    [data-testid="stChatMessageContent"] { border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px 16px; background: #fff; }
    .stButton > button { border-radius: 8px; border: 1px solid #e5e7eb; background: #fff; color: #111827; font-weight: 500; }
    .stButton > button:hover { border-color: #c7cbd1; background: #f9fafb; color: #111827; }
</style>
""", unsafe_allow_html=True)

s=summarize_results(st.session_state.invoice_results)

with st.sidebar:
    st.markdown("### Нэхэмжлэхийн Агент")
    st.caption("Мэргэжлийн нэхэмжлэх шалгах орчин")
    st.divider()
    st.metric("Нэхэмжлэх", s["total"])
    st.metric("AUTO_POST", s["auto"])
    st.metric("DENY", s["deny"])
    st.metric("HUMAN_APPROVAL", s["approval"])
    st.divider()
    st.caption("Нэхэмжлэх оруулах")
    files=st.file_uploader("JPG, PNG, PDF", type=["jpg","jpeg","png","pdf"], accept_multiple_files=True, label_visibility="collapsed")
    if st.button("Шинжлэх", type="primary", use_container_width=True, disabled=not files):
        for uf in files:
            with st.spinner(f"{uf.name} файлыг шинжилж байна"):
                process_upload(uf)
        st.rerun()
    st.divider()
    st.caption("Жишээ асуултууд")
    for i,p in enumerate(["Нийт хэдэн нэхэмжлэх байна?","Хэдэн invoice DENY болсон?","Duplicate invoice хэд?","Invoice 007 яагаад deny?","Invoice 025 duplicate мөн үү?","Invoice 094 математик зөв үү?"]):
        if st.button(p,key=f"preset_{i}",use_container_width=True):
            st.session_state["qi"]=p
            st.rerun()

st.markdown("""
<div class="topbar">
    <div class="brand">AI</div>
    <div><h1>AI Нэхэмжлэхийн Агент</h1><p>Боловсруулсан нэхэмжлэхүүдтэй чатлаж, баримт шалгаж, шинэ файл шинжилнэ.</p></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-strip">
    <div class="metric-card"><div class="label">Нийт нэхэмжлэх</div><div class="value">{s["total"]}</div></div>
    <div class="metric-card"><div class="label">Автомат бүртгэл</div><div class="value">{s["auto"]}</div></div>
    <div class="metric-card"><div class="label">Татгалзсан</div><div class="value">{s["deny"]}</div></div>
    <div class="metric-card"><div class="label">Татгалзсан дүн</div><div class="value">{s["denied_amount"]:,}₮</div></div>
</div>
""", unsafe_allow_html=True)

chat_tab, uploads_tab, results_tab = st.tabs(["Чат", "Оруулсан нэхэмжлэх", "Үр дүн"])

with chat_tab:
    for m in st.session_state.ch:
        with st.chat_message(m["role"], avatar="🤖" if m["role"]=="assistant" else "👤"):
            st.markdown(m["content"])
    q=st.chat_input("Нэхэмжлэх, шийдвэр, vendor, алдаа эсвэл тайлангийн талаар асууна уу") or st.session_state.pop("qi",None)
    if q:
        st.session_state.ch.append({"role":"user","content":q})
        with st.chat_message("user", avatar="👤"):
            st.markdown(q)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Бодож байна"):
                ans=ask_agent(q)
            st.markdown(ans)
        st.session_state.ch.append({"role":"assistant","content":ans})

with uploads_tab:
    if not st.session_state.processed_uploads:
        st.info("Энэ session-д шинэ нэхэмжлэх оруулаагүй байна. Зүүн талын upload хэсгийг ашиглана уу.")
    for r in st.session_state.processed_uploads:
        with st.expander(f"{r.get('filename')} · {r.get('decision')}", expanded=False):
            c1,c2,c3=st.columns(3)
            c1.metric("Нийлүүлэгч", r.get("vendor_name") or "?")
            c2.metric("Дүн", f"{(r.get('grand_total') or 0):,}₮")
            c3.metric("Ангилал", r.get("category") or "?")
            st.markdown(f"**Огноо:** {r.get('invoice_date') or '?'} -> {r.get('due_date') or '?'}")
            if r.get("line_items"):
                st.dataframe(r["line_items"], use_container_width=True, hide_index=True)
            issues=r.get("issues") or []
            if issues:
                for issue in issues:
                    st.error(f"{issue_type(issue)}: {issue_detail(issue)}")
            else:
                st.success("Бүх шалгалт амжилттай.")

with results_tab:
    c1,c2=st.columns([1,1])
    with c1:
        st.subheader("Алдааны задаргаа")
        st.dataframe([{"Алдаа":k,"Тоо":v} for k,v in sorted(s["issues"].items())], use_container_width=True, hide_index=True)
        st.subheader("Файлын төрөл")
        st.dataframe([
            {"Төрөл":"JPG/JPEG","Тоо":s["jpg"]},
            {"Төрөл":"PNG","Тоо":s["png"]},
            {"Төрөл":"PDF","Тоо":s["pdf"]},
            {"Төрөл":"Гар бичмэл","Тоо":s["handwritten"]},
        ], use_container_width=True, hide_index=True)
    with c2:
        st.subheader("DENY болсон нэхэмжлэх")
        denied=[r for r in st.session_state.invoice_results if r.get("decision")=="DENY"]
        rows=[{"Нэхэмжлэх":r.get("filename"),"Нийлүүлэгч":r.get("vendor_name"),"Алдаа":", ".join(issue_type(i) for i in r.get("issues",[])),"Дүн":r.get("grand_total")} for r in denied]
        st.dataframe(rows, use_container_width=True, hide_index=True)
