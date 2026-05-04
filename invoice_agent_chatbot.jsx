import { useState, useRef, useEffect } from "react";

const VENDORS=[{n:"Демо Компани-1",b:"Демо Банк 1",a:"5001122334"},{n:"Демо Компани-2",b:"Демо Банк 1",a:"1102003004"},{n:"Демо Компани-3",b:"Демо Банк 1",a:"4001122334"},{n:"Демо Компани-4",b:"Демо Банк 2",a:"5007788990"},{n:"Демо Компани-5",b:"Демо Банк 2",a:"1009900880"},{n:"Демо Компани-6",b:"Демо Банк 2",a:"1166778899"},{n:"Демо Компани-7",b:"Демо Банк 2",a:"5004455667"},{n:"Демо Компани-8",b:"Демо Банк 1",a:"4005544332"},{n:"Демо Компани-9",b:"Демо Банк 1",a:"5003322110"},{n:"Демо Компани-10",b:"Демо Банк 1",a:"1002233445"}];

function validate(d){
  const iss=[];
  (d.line_items||[]).forEach((li,i)=>{const e=(li.quantity||0)*(li.unit_price||0);if(e&&li.total&&e!==li.total)iss.push({t:"AMOUNT_MISMATCH",d:`Line ${i+1}: ${li.quantity}×${(li.unit_price||0).toLocaleString()}=${e.toLocaleString()}, shows ${(li.total||0).toLocaleString()}`})});
  const ls=(d.line_items||[]).reduce((s,l)=>s+(l.total||0),0);
  if(ls&&d.grand_total&&ls!==d.grand_total)iss.push({t:"AMOUNT_MISMATCH",d:`Sum ${ls.toLocaleString()}≠total ${(d.grand_total||0).toLocaleString()}`});
  const vn=(d.vendor_name||"").replace(/\s*[-–]\s*/g,"-").toLowerCase();
  const v=VENDORS.find(v=>v.n.replace(/\s*[-–]\s*/g,"-").toLowerCase()===vn);
  if(!v)iss.push({t:"UNREGISTERED_VENDOR",d:`"${d.vendor_name}" not in DB`});
  if(v){if(d.account_number&&d.account_number!==v.a)iss.push({t:"BANK_ACCOUNT_MISMATCH",d:`Account: ${d.account_number} vs DB ${v.a}`})}
  if(d.invoice_date?.match(/02-30|02\/30/))iss.push({t:"INVALID_DATE",d:"Feb 30 does not exist"});
  try{const id=new Date(d.invoice_date?.replace(/\//g,"-")),dd=new Date(d.due_date?.replace(/\//g,"-"));if(dd<id)iss.push({t:"INVALID_DATE",d:`Due before invoice date`})}catch{}
  return{issues:iss,decision:iss.length?"DENY":v?"AUTO_POST":"HUMAN_APPROVAL",vendor:v};
}

const SYS=`You are an AI Invoice Processing Agent. When given invoice data, analyze it. When asked questions, answer precisely citing invoice numbers. Answer in the same language as the question. Registered vendors: Демо Компани 1-10. Unregistered: 11,12+.`;

export default function App(){
  const[msgs,setMsgs]=useState([{role:"assistant",content:"Сайн байна уу! Би Invoice AI Agent. Invoice файл хавсаргах (📎) эсвэл асуулт бичнэ үү."}]);
  const[input,setInput]=useState("");
  const[loading,setLoading]=useState(false);
  const[processed,setProcessed]=useState([]);
  const endRef=useRef(null);
  const fileRef=useRef(null);

  useEffect(()=>{endRef.current?.scrollIntoView({behavior:"smooth"})},[msgs]);

  const callClaude=async(messages)=>{
    const ctx=processed.length?`\n\nProcessed invoices:\n${processed.map(p=>`${p.filename}: vendor=${p.vendor_name}, total=${p.grand_total?.toLocaleString()}₮, decision=${p.decision}, issues=${p.issues?.map(i=>i.t).join(",")||"none"}, category=${p.category}`).join("\n")}`:"";
    const r=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({model:"claude-sonnet-4-20250514",max_tokens:1000,system:SYS+ctx,messages})});
    const d=await r.json();
    return d.content?.map(c=>c.text||"").join("")||"Error";
  };

  const send=async(text)=>{
    const q=(text||input).trim();if(!q||loading)return;setInput("");
    const updated=[...msgs,{role:"user",content:q}];setMsgs(updated);setLoading(true);
    try{const a=await callClaude(updated.filter(m=>m.role!=="system").map(m=>({role:m.role==="assistant"?"assistant":"user",content:m.content})));
    setMsgs(p=>[...p,{role:"assistant",content:a}])}catch{setMsgs(p=>[...p,{role:"assistant",content:"API холболт амжилтгүй."}])}
    setLoading(false);
  };

  const handleFile=async(e)=>{
    const file=e.target.files?.[0];if(!file||loading)return;
    e.target.value="";setLoading(true);
    setMsgs(p=>[...p,{role:"user",content:`📎 ${file.name}`,isFile:true,fileName:file.name}]);
    try{
      const b64=await new Promise((res,rej)=>{const r=new FileReader();r.onload=()=>res(r.result.split(",")[1]);r.onerror=rej;r.readAsDataURL(file)});
      const mt=file.type==="application/pdf"?"application/pdf":file.type.includes("png")?"image/png":"image/jpeg";
      const content=mt==="application/pdf"
        ?[{type:"document",source:{type:"base64",media_type:mt,data:b64}},{type:"text",text:'Extract all data from this invoice. Return ONLY JSON: {"invoice_number":"str","vendor_name":"str","bank_name":"str","account_number":"str","email":"str","invoice_date":"YYYY-MM-DD","due_date":"YYYY-MM-DD","line_items":[{"description":"str","quantity":number,"unit_price":number,"total":number}],"grand_total":number}'}]
        :[{type:"image",source:{type:"base64",media_type:mt,data:b64}},{type:"text",text:'Extract all data from this Mongolian invoice. Return ONLY JSON: {"invoice_number":"str","vendor_name":"str","bank_name":"str","account_number":"str","email":"str","invoice_date":"YYYY-MM-DD","due_date":"YYYY-MM-DD","line_items":[{"description":"str","quantity":number,"unit_price":number,"total":number}],"grand_total":number}. Read handwriting carefully.'}];
      const r=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({model:"claude-sonnet-4-20250514",max_tokens:2000,messages:[{role:"user",content}]})});
      const d=await r.json();
      let txt=d.content?.[0]?.text||"{}";txt=txt.replace(/^```json\s*/,"").replace(/\s*```$/,"");
      const ext=JSON.parse(txt);
      const{issues,decision,vendor}=validate(ext);
      const cat=(ext.line_items||[]).map(l=>l.description||"").join(" ").toLowerCase();
      const category=cat.match(/тээвэр|ачаа|гааль|шатахуун|хүргэлт/)?"Тээвэр, логистик":cat.match(/засвар|лифт|цэвэрлэгээ|сантехник|техник/)?"Засвар үйлчилгээ":cat.match(/монитор|принтер|сервер|интернэт|програм|кибер|камер|домэйн|ssl/)?"МТ зардал":cat.match(/түрээс|оффис|форклифт/)?"Түрээсийн зардал":cat.match(/даатгал/)?"Даатгал":"Бусад";
      const rec={...ext,filename:file.name,issues,decision,category};
      setProcessed(p=>[rec,...p]);
      const dc=decision==="AUTO_POST"?"✅ AUTO_POST":"❌ DENY";
      let reply=`**${file.name} боловсруулсан**\n\n`;
      reply+=`Vendor: ${ext.vendor_name||"?"}\nDüн: ${ext.grand_total?.toLocaleString()||"?"}₮\nОгноо: ${ext.invoice_date||"?"} → ${ext.due_date||"?"}\nАнгилал: ${category}\n`;
      if(ext.line_items?.length){reply+="\nМөрүүд:\n";ext.line_items.forEach((li,i)=>{reply+=`  ${i+1}. ${li.description} — ${li.quantity}×${(li.unit_price||0).toLocaleString()} = ${(li.total||0).toLocaleString()}₮\n`})}
      reply+=`\nШалгалт:\n`;
      reply+=issues.length?issues.map(i=>`  ⛔ ${i.t}: ${i.d}`).join("\n"):"  ✓ Бүх шалгалт дамжсан";
      reply+=`\n\n**Шийдвэр: ${dc}**`;
      setMsgs(p=>[...p,{role:"assistant",content:reply}]);
    }catch(err){setMsgs(p=>[...p,{role:"assistant",content:`Алдаа: ${err.message}`}])}
    setLoading(false);
  };

  return(
<div style={{display:"flex",flexDirection:"column",height:"100vh",fontFamily:"'DM Sans',system-ui,sans-serif",background:"#09090b",color:"#e4e4e7"}}>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"/>

<div style={{padding:"10px 16px",borderBottom:"1px solid #1f2937",display:"flex",alignItems:"center",gap:8}}>
  <div style={{width:28,height:28,borderRadius:7,background:"linear-gradient(135deg,#4f46e5,#7c3aed)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:12,color:"#fff",fontWeight:700}}>AI</div>
  <span style={{fontWeight:600,fontSize:14}}>Invoice Agent</span>
  <span style={{fontSize:10,color:"#52525b"}}>AI Legends 2026</span>
  {processed.length>0&&<span style={{marginLeft:"auto",fontSize:10,color:"#6b7280"}}>{processed.length} processed</span>}
</div>

<div style={{flex:1,overflowY:"auto",padding:"16px"}}>
  {msgs.map((m,i)=>(
    <div key={i} style={{display:"flex",justifyContent:m.role==="user"?"flex-end":"flex-start",marginBottom:12,alignItems:"flex-start"}}>
      {m.role!=="user"&&<div style={{width:24,height:24,borderRadius:6,background:"#4f46e5",display:"flex",alignItems:"center",justifyContent:"center",fontSize:10,color:"#fff",fontWeight:700,marginRight:8,flexShrink:0,marginTop:2}}>AI</div>}
      <div style={{maxWidth:"80%",padding:"9px 13px",borderRadius:m.role==="user"?"12px 12px 4px 12px":"12px 12px 12px 4px",background:m.role==="user"?"#4f46e5":"#18181b",border:m.role==="user"?"none":"1px solid #27272a",fontSize:13,lineHeight:1.65,whiteSpace:"pre-wrap",wordBreak:"break-word"}}>
        {m.content.split(/(\*\*.*?\*\*)/g).map((part,j)=>part.startsWith("**")&&part.endsWith("**")?<strong key={j} style={{fontWeight:600}}>{part.slice(2,-2)}</strong>:<span key={j}>{part}</span>)}
      </div>
    </div>
  ))}
  {loading&&<div style={{display:"flex",alignItems:"center",gap:8,marginBottom:12}}>
    <div style={{width:24,height:24,borderRadius:6,background:"#4f46e5",display:"flex",alignItems:"center",justifyContent:"center",fontSize:10,color:"#fff",fontWeight:700}}>AI</div>
    <div style={{padding:"9px 13px",background:"#18181b",border:"1px solid #27272a",borderRadius:12,display:"flex",gap:4}}>
      {[0,1,2].map(i=><div key={i} style={{width:6,height:6,borderRadius:"50%",background:"#6366f1",animation:`b 1s ${i*.15}s infinite`}}/>)}
    </div>
  </div>}
  <div ref={endRef}/>
</div>

{!loading&&msgs.length<3&&<div style={{padding:"0 16px 8px",display:"flex",gap:6,flexWrap:"wrap"}}>
  {["Нийт хэдэн invoice байна?","Invoice 007 яагаад deny?","Банкны зөрүүтэй invoice хэд?"].map(q=>(
    <button key={q} onClick={()=>send(q)} style={{padding:"4px 10px",borderRadius:12,border:"1px solid #27272a",background:"transparent",color:"#71717a",fontSize:11,cursor:"pointer"}}>{q}</button>
  ))}
</div>}

<div style={{padding:"8px 16px 14px",borderTop:"1px solid #1f2937"}}>
  <div style={{display:"flex",alignItems:"center",gap:6,background:"#18181b",border:"1px solid #27272a",borderRadius:10,padding:"4px 4px 4px 6px"}}>
    <button onClick={()=>fileRef.current?.click()} disabled={loading} title="Invoice хавсаргах" style={{width:32,height:32,borderRadius:8,border:"none",background:"transparent",color:"#71717a",fontSize:18,cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}} onMouseOver={e=>e.target.style.color="#e4e4e7"} onMouseOut={e=>e.target.style.color="#71717a"}>&#128206;</button>
    <input ref={fileRef} type="file" accept=".jpg,.jpeg,.png,.pdf" onChange={handleFile} style={{display:"none"}}/>
    <input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()} placeholder="Асуулт бичих эсвэл invoice хавсаргах..." disabled={loading}
      style={{flex:1,padding:"6px 8px",background:"transparent",border:"none",color:"#e4e4e7",fontSize:13,outline:"none"}}/>
    <button onClick={()=>send()} disabled={loading||!input.trim()} style={{width:32,height:32,borderRadius:8,border:"none",background:input.trim()&&!loading?"#4f46e5":"transparent",color:input.trim()&&!loading?"#fff":"#52525b",fontSize:14,cursor:input.trim()?"pointer":"default",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>&#10148;</button>
  </div>
</div>

<style>{`@keyframes b{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}`}</style>
</div>);
}
