"""
AI Invoice Processing Agent — AI Legends 2026
Run: streamlit run app.py
Deploy: streamlit.io → add ANTHROPIC_API_KEY to secrets
"""
import streamlit as st, anthropic, base64, json, sqlite3, re, os, fitz
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="🧾 AI Invoice Agent", page_icon="🧾", layout="wide")

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

@st.cache_data
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

def compact_results(results):
    compact = []
    for r in results:
        issues = r.get("issues") or []
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
            "deny_reasons": r.get("decision_reasons") or [issue_detail(i) for i in issues],
        })
    return compact

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
    for h in master_db["historical_invoices"]:
        if str(h.get("VendorName","")).strip().lower()==(data.get("vendor_name") or "").strip().lower() and gt and gt==(h.get("GrandTotal") or 0) and (data.get("invoice_date") or "").replace("/","-")==(h.get("InvoiceDate") or ""):
            issues.append({"type":"DUPLICATE","detail":f"Matches historical ID={h['ID']}"}); break
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

SUMMARY={"total":100,"auto":72,"deny":28,"approval":0,"issues":{"BANK_ACCOUNT_MISMATCH":8,"AMOUNT_MISMATCH":5,"INVALID_DATE":5,"UNREGISTERED_VENDOR":5,"DUPLICATE":5},"jpg":15,"png":4,"pdf":81,"denied":["002","003","005","007","010","013","015","022","025","026","028","034","035","038","039","041","047","053","056","057","064","066","075","080","087","088","092","094"],"details":{"002":"Демо Компани-10, BANK_ACCOUNT_MISMATCH (1002033445 vs 1002233445), 2,920,000₮","003":"Демо Компани-9, BANK_ACCOUNT_MISMATCH, 2,920,000₮","005":"Демо Компани-9, INVALID_DATE (due<invoice), 150,000₮","007":"Демо Компани-8, AMOUNT_MISMATCH (2.5M≠2.51M), 2,510,000₮","010":"Демо Компани-12, UNREGISTERED_VENDOR, 300,000₮","013":"Демо Компани-8, BANK_ACCOUNT_MISMATCH, 550,000₮","015":"Демо Компани-8, BANK_ACCOUNT_MISMATCH, 285,000₮","022":"Демо Компани-1, INVALID_DATE (Feb 30), 1,200,000₮","025":"Демо Компани-8, DUPLICATE, 450,000₮","026":"Демо Компани-11, UNREGISTERED_VENDOR, 350,000₮","028":"Демо Компани-5, AMOUNT_MISMATCH, 190,000₮","034":"Демо Компани-2, INVALID_DATE, 600,000₮","035":"Демо Компани-2, DUPLICATE, 855,000₮","038":"Демо Компани-7, DUPLICATE, 170,000₮","039":"Демо Компани-10, BANK_ACCOUNT_MISMATCH, 2,920,000₮","041":"Демо Компани-11, UNREGISTERED_VENDOR, 200,000₮","047":"Демо Компани-1, DUPLICATE, 190,000₮","053":"Демо Компани-9, BANK_ACCOUNT_MISMATCH, 190,000₮","056":"Демо Компани-9, BANK_ACCOUNT_MISMATCH, 300,000₮","057":"Демо Компани-7, DUPLICATE, 390,000₮","064":"Демо Компани-2, AMOUNT_MISMATCH, 220,000₮","066":"Демо Компани-1, INVALID_DATE (Feb 30), 2,920,000₮","075":"Демо Компани-2, BANK_ACCOUNT_MISMATCH, 760,000₮","080":"Демо Компани-6, AMOUNT_MISMATCH, 2,930,000₮","087":"Демо Компани-5, INVALID_DATE (Feb 30), 350,000₮","088":"Демо Компани-12, UNREGISTERED_VENDOR, 2,920,000₮","092":"Демо Компани-11, UNREGISTERED_VENDOR, 130,000₮","094":"Демо Компани-9, AMOUNT_MISMATCH, 340,000₮"}}

if "invoice_results" not in st.session_state:
    st.session_state.invoice_results = load_initial_results()

# UI
st.title("🧾 AI Invoice Processing Agent")
st.caption("AI Legends 2026 | Claude Sonnet 4 Vision + Reasoning")
tab1,tab2,tab3=st.tabs(["📤 Upload & Analyze","📊 100 Invoice Results","💬 Q&A Chat"])

with tab1:
    st.subheader("Invoice upload → AI боловсруулалт")
    files=st.file_uploader("JPG / PNG / PDF invoice", type=["jpg","jpeg","png","pdf"], accept_multiple_files=True)
    if files and st.button("🚀 Боловсруулах",type="primary"):
        for uf in files:
            with st.expander(f"📄 {uf.name}",expanded=True):
                fb=uf.read(); c1,c2=st.columns([1,2])
                with c1:
                    if uf.type=="application/pdf":
                        doc=fitz.open(stream=fb,filetype="pdf"); st.image(doc[0].get_pixmap(dpi=120).tobytes("png")); doc.close()
                    else: st.image(fb)
                with c2:
                    with st.spinner("Claude Vision уншиж байна..."):
                        ext=process(fb,uf.type)
                    issues,decision,vendor=validate(ext); cat=classify(ext,vendor)
                    file_ext=Path(uf.name).suffix.lower().lstrip(".")
                    rec={**ext,"filename":uf.name,"category":cat,"decision":decision,"issues":issues,"file_type":file_ext.upper(),"is_handwritten":file_ext in ["jpg","jpeg"],"decision_reasons":[issue_detail(i) for i in issues] or ["Registered vendor, all checks passed"]}
                    st.session_state.invoice_results.append(rec)
                    st.markdown(f"**Vendor:** {ext.get('vendor_name','?')} | **Дүн:** {(ext.get('grand_total') or 0):,}₮")
                    st.markdown(f"**Огноо:** {ext.get('invoice_date','?')} → {ext.get('due_date','?')} | **Ангилал:** {cat}")
                    if ext.get("line_items"):
                        for li in ext["line_items"]: st.markdown(f"- {li.get('description')} {li.get('quantity')}×{(li.get('unit_price') or 0):,}={( li.get('total') or 0):,}₮")
                    if issues:
                        for iss in issues: st.error(f"⛔ {iss['type']}: {iss['detail']}")
                    else: st.success("✅ Бүх шалгалт амжилттай")
                    colors={"AUTO_POST":"green","DENY":"red","HUMAN_APPROVAL":"orange"}
                    st.markdown(f"### :{colors[decision]}[**{decision}**]")

with tab2:
    s=summarize_results(st.session_state.invoice_results)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Нийт",s["total"]); c2.metric("✅ AUTO_POST",s["auto"]); c3.metric("❌ DENY",s["deny"]); c4.metric("⚠️ APPROVAL",s["approval"])
    st.divider()
    st.markdown("**🔍 Зөрчлийн тархалт:**")
    cols=st.columns(5)
    for i,(k,v) in enumerate(s["issues"].items()):
        cols[i%5].metric(k,v)
    st.divider()
    co1,co2=st.columns(2)
    with co1:
        st.markdown("**📄 Файлын төрөл:**")
        st.markdown(f"- JPG/JPEG: **{s['jpg']}**\n- PNG: **{s['png']}**\n- PDF: **{s['pdf']}**\n- Гар бичмэл: **{s['handwritten']}**")
        st.markdown(f"**Нийт дүн:** {s['total_amount']:,}₮  \n**DENY дүн:** {s['denied_amount']:,}₮")
    with co2:
        st.markdown("**❌ DENY болсон invoices:**")
        denied=[r for r in st.session_state.invoice_results if r.get("decision")=="DENY"]
        for r in denied:
            issue_names=", ".join(issue_type(i) for i in r.get("issues",[])) or "Unknown"
            st.markdown(f"- **{r.get('filename')}**: {r.get('vendor_name','?')}, {issue_names}, {(r.get('grand_total') or 0):,}₮")

with tab3:
    st.subheader("💬 Invoice Q&A — Claude AI")
    presets=["Нийт хэдэн invoice байна?","Хэдэн invoice DENY болсон?","Duplicate invoice хэд?","Бүртгэлгүй vendor хэд?","Банкны зөрүүтэй хэд?","Invoice 007 яагаад deny?","Invoice 025 duplicate мөн үү?","Invoice 007 математик зөв үү?"]
    cols=st.columns(4)
    for i,p in enumerate(presets):
        if cols[i%4].button(p,key=f"p{i}",use_container_width=True): st.session_state["qi"]=p
    if "ch" not in st.session_state: st.session_state.ch=[]
    for m in st.session_state.ch:
        with st.chat_message(m["role"]): st.write(m["content"])
    q=st.chat_input("Асуулт бичнэ үү...") or st.session_state.pop("qi",None)
    if q:
        st.session_state.ch.append({"role":"user","content":q})
        with st.chat_message("user"): st.write(q)
        live_summary=summarize_results(st.session_state.invoice_results)
        live_results=compact_results(st.session_state.invoice_results)
        ctx=f"""You are an AI Invoice Agent for a Mongolian invoice-processing demo.

Use ONLY the data below. Answer in the same language as the question.

You can answer aggregate questions:
- total invoices
- correct invoices / AUTO_POST
- suspicious invoices / DENY
- duplicates
- math/amount mismatches
- unregistered vendors
- invalid dates
- bank/account mismatches
- image file counts
- handwritten image counts
- HUMAN_APPROVAL count
- DENY count

You can answer invoice-specific fact-check questions:
- final decision
- duplicate or not
- vendor name
- category
- due date
- whether bank account is registered/matching
- why denied
- issue/error types
- whether human approval is needed
- whether math calculation is correct

Report/submission sections to support when asked:
- solution overview
- model architecture and agent workflow
- data processing and validation strategy
- evaluation results
- key conclusions, limitations, and future improvements

Summary:
{json.dumps(live_summary,ensure_ascii=False,indent=2)}

Invoice records:
{json.dumps(live_results,ensure_ascii=False,indent=2)}
"""
        with st.chat_message("assistant"):
            with st.spinner("Хариулж байна..."):
                resp=client.messages.create(model="claude-sonnet-4-20250514",max_tokens=800,messages=[{"role":"user","content":ctx+"\n\nQ: "+q}])
                ans=resp.content[0].text
            st.write(ans); st.session_state.ch.append({"role":"assistant","content":ans})
