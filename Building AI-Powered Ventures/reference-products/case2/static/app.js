'use strict';
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = v => v === null || v === undefined ? '—' : Number(v).toLocaleString('en-US', {maximumFractionDigits: 2});
const labels = {reorder:'Replenish', no_order:'No order', needs_data:'Needs data', clearance:'Clearance'};
let dashboard, selected = 'CASE-001', csrf = '', pending = null, history = [], busy = false;
async function api(path, body) {
  const response = await fetch(path, body === undefined ? {} : {method:'POST', headers:{'Content-Type':'application/json','X-CSRF-Token':csrf}, body:JSON.stringify(body)});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`);
  return result;
}
function notice(text) { $('notice').textContent=text; $('notice').hidden=!text; }
async function refresh() {
  dashboard = await api('/api/dashboard');
  $('metric-products').textContent = dashboard.rows.length;
  $('metric-reorder').textContent = dashboard.counts.reorder || 0;
  $('metric-order').textContent = `${fmt(dashboard.total_order_units)} units in proposed orders`;
  $('metric-shortage').textContent = dashboard.shortage_skus;
  $('metric-missing').textContent = dashboard.counts.needs_data || 0;
  $('current-stage').textContent = `Stage ${dashboard.stage} · v${dashboard.version}`;
  document.querySelectorAll('[data-stage]').forEach(b => b.classList.toggle('active', b.dataset.stage === dashboard.stage));
  const oldCategory = $('category').value;
  $('category').innerHTML = '<option value="">All categories</option>' + [...new Set(dashboard.rows.map(r=>r.category))].sort().map(c=>`<option>${esc(c)}</option>`).join('');
  $('category').value = oldCategory;
  renderRows();
  await showSku(selected);
}
function filteredRows() {
  const search = $('search').value.toLowerCase(), status = $('status').value, category = $('category').value;
  return dashboard.rows.filter(r=>(`${r.sku} ${r.product_name}`.toLowerCase().includes(search)) && (!category || r.category===category) && (status==='all' || r.status===status || status==='shortage' && r.first_shortage_date));
}
function renderRows() {
  const rows = filteredRows();
  $('products').innerHTML = rows.map(r=>`<tr class="${r.sku===selected?'selected':''}"><td><button class="sku-link" data-sku="${esc(r.sku)}">${esc(r.sku)}</button><span class="product-name" title="${esc(r.product_name)}">${esc(r.product_name)}</span></td><td>${fmt(r.weekly_forecast_units)}</td><td>${r.inputs.on_hand_qty === '' ? '—' : fmt(r.inputs.on_hand_qty)}</td><td><strong>${fmt(r.recommended_order_units)}</strong></td><td><span class="badge ${esc(r.status)}">${esc(labels[r.status])}</span></td></tr>`).join('') || '<tr><td colspan="5">No matching products.</td></tr>';
  $('row-count').textContent = `${rows.length} of ${dashboard.rows.length} products · Select a SKU to inspect the evidence below`;
}
function chart(values, labelsX, options={}) {
  const w=560,h=180,left=38,right=15,top=16,bottom=27;
  const max=Math.max(1,...values,...(options.second||[]))*1.12;
  const x=i=>left+i*(w-left-right)/Math.max(1,values.length-1), y=v=>h-bottom-v/max*(h-top-bottom);
  const path=arr=>arr.map((v,i)=>`${i?'L':'M'}${x(i).toFixed(2)},${y(v).toFixed(2)}`).join(' ');
  let body='';
  for(let i=0;i<4;i++){let v=max*i/3;body+=`<line class="grid" x1="${left}" y1="${y(v)}" x2="${w-right}" y2="${y(v)}"/><text x="3" y="${y(v)+3}">${Math.round(v)}</text>`;}
  if(options.bars) body += values.map((v,i)=>`<rect x="${x(i)-8}" y="${y(v)}" width="16" height="${h-bottom-y(v)}" fill="${i>=values.length-4?'#6a468f':'#d5c7e4'}" rx="2"><title>${esc(labelsX[i])}: ${fmt(v)} units</title></rect>`).join('');
  else body+=`<path class="line" d="${path(values)}"/>`;
  if(options.second) body+=`<path class="demand" d="${path(options.second)}"/>`;
  if(options.lost) body+=options.lost.map((v,i)=>v>0?`<circle cx="${x(i)}" cy="${y(values[i])}" r="4" fill="#bd5146"><title>${esc(labelsX[i])}: ${fmt(v)} lost units</title></circle>`:'').join('');
  [0,Math.floor((values.length-1)/2),values.length-1].forEach(i=>body+=`<text text-anchor="${i===0?'start':i===values.length-1?'end':'middle'}" x="${x(i)}" y="${h-6}">${esc(labelsX[i]?.slice(5))}</text>`);
  return `<svg class="chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(options.title||'Inventory chart')}">${body}</svg>`;
}
function dailyTable(rows) {
  return `<div class="table-wrap"><table><thead><tr><th>Date</th><th>Opening</th><th>Existing inbound</th><th>New order</th><th>Demand</th><th>Sales</th><th>Lost</th><th>Closing</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r.date}</td>${['opening_stock','existing_inbound','proposed_order','forecast_demand','sales','unmet_demand','closing_stock'].map(k=>`<td>${fmt(r[k])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
async function showSku(sku) {
  selected=sku;
  const d=await api('/api/sku?sku='+encodeURIComponent(sku));
  if(selected!==sku) return;
  renderRows();
  $('detail-title').textContent=d.sku;
  $('detail-name').textContent=d.product_name;
  $('detail-status').textContent=labels[d.status]; $('detail-status').className='badge '+d.status;
  const hist=[...d.history].reverse();
  const historyChart=chart(hist.map(r=>r.units_sold===''?0:Number(r.units_sold)),hist.map(r=>r.week_start),{bars:true,title:'13 weeks of raw sales. Last four weeks are highlighted.'});
  if(d.status==='needs_data') {
    $('detail-content').innerHTML=`<div class="warning">${esc(d.reason)}. Recommendation unavailable until the source is confirmed.</div><p class="small muted">Raw sales (a missing observation is marked in the table, never treated as zero for calculations).</p><table><thead><tr><th>Week</th><th>Recorded units</th></tr></thead><tbody>${hist.map(r=>`<tr><td>${esc(r.week_start)}</td><td>${r.units_sold===''?'Missing':fmt(r.units_sold)}</td></tr>`).join('')}</tbody></table>`;
    return;
  }
  const p=d.inputs;
  $('detail-content').innerHTML=`${d.reason?`<div class="warning">${esc(d.reason)}</div>`:''}<div class="facts">${[['Weekly forecast',fmt(d.weekly_forecast_units)],['Daily forecast',fmt(d.daily_forecast_units)],['On hand',fmt(p.on_hand_qty)],['Planning horizon',d.planning_days+' days'],['Eligible inbound',fmt(d.eligible_inbound_units)],['Projected lost demand',fmt(d.unmet_units_over_horizon)]].map(([k,v])=>`<div><span>${k}</span><strong>${v}</strong></div>`).join('')}</div><div class="detail-grid"><div><p class="subhead">13 weeks of recorded sales</p>${historyChart}<p class="legend">Raw observations stay unchanged. Purple = the four forecast weeks.</p><div class="formula"><code>ceil(max(0, ${fmt(d.daily_forecast_units)} × ${d.planning_days} − ${fmt(p.on_hand_qty)} − ${fmt(d.eligible_inbound_units)}))</code><strong>${fmt(d.recommended_order_units)} units ${d.status==='clearance'?'· clearance override':'to order'}</strong><span class="small muted">Display values rounded; the calculation keeps full precision.<br>Unrounded order: ${fmt(d.unrounded_order_units)} · arrival ${d.proposed_order_date}</span></div></div><div><p class="subhead">Daily stock projection · with proposed order</p>${chart(d.projection.map(r=>r.closing_stock),d.projection.map(r=>r.date),{second:d.projection.map(r=>r.forecast_demand),lost:d.projection.map(r=>r.unmet_demand),title:'Daily closing stock and forecast demand; red dots mark lost demand.'})}<p class="legend"><span class="violet">━ Closing stock</span><span class="teal">━ Daily demand</span><span>🔴 Lost demand</span></p><p class="small muted">Existing inbound: ${p.inbound_available_date?esc(p.inbound_available_date)+' · '+fmt(p.inbound_qty)+' units':'none'}<br>New order: ${d.proposed_order_date} · ${fmt(d.recommended_order_units)} units<br>First shortage: ${d.first_shortage_date||'none'} · ${fmt(d.shortage_days_count)} shortage days<br>Period ends before ${d.planning_end_exclusive}</p></div></div><details open><summary>Four-week calculation trail</summary><div class="table-wrap"><table><thead><tr><th>Week</th><th>Raw units</th><th>Normalised units</th><th>Original weight</th><th>Effective weight</th><th>Treatment</th></tr></thead><tbody>${d.calculation.map(r=>`<tr><td>${r.week_start}</td><td>${fmt(r.raw_units)}</td><td>${fmt(r.normalised_units)}</td><td>${fmt(r.original_weight)}</td><td>${fmt(r.effective_weight)}</td><td>${r.excluded?'Exclude confirmed wholesale':r.member_day_multiplier!==1?'Divide by '+r.member_day_multiplier:'Keep'}</td></tr>`).join('')}</tbody></table></div></details><details><summary>Daily stock ledger · receipts, sales and shortages</summary>${dailyTable(d.projection)}</details>`;
}
function showPreview(p) {
  pending=p;
  $('preview').hidden=false; $('preview-note').textContent=p.note;
  $('preview-count').textContent=`${p.changed_skus} SKUs change · not applied`;
  $('preview-body').innerHTML=`<table><thead><tr><th>SKU</th><th>Order before → after</th><th>Weekly demand</th><th>Lost demand</th><th>First shortage after</th></tr></thead><tbody>${p.changes.map(c=>`<tr><td>${esc(c.sku)}</td><td>${fmt(c.before.recommended_order_units)} → <strong>${fmt(c.after.recommended_order_units)}</strong></td><td>${fmt(c.before.weekly_forecast_units)} → ${fmt(c.after.weekly_forecast_units)}</td><td>${fmt(c.before.unmet_units_over_horizon)} → ${fmt(c.after.unmet_units_over_horizon)}</td><td>${esc(c.after.first_shortage_date)||'none'}</td></tr>`).join('')||'<tr><td colspan="5">No numerical changes; review the context and dates below.</td></tr>'}</tbody></table><details><summary>Exact proposed business facts and overrides</summary><pre>${esc(JSON.stringify({events:p.events,overrides:p.overrides},null,2))}</pre></details>${p.after_detail?`<details open><summary>Daily ledger after the proposed delay</summary>${dailyTable(p.after_detail.projection)}</details>`:''}`;
  $('apply').disabled=busy;
  $('preview').scrollIntoView({behavior:'smooth',block:'center'});
}
function addMessage(role, text) {
  const article=document.createElement('article'); article.className='message '+role;
  const title=document.createElement('strong'); title.textContent=role==='user'?'You':role==='error'?'Request failed':'Inventory assistant'; article.append(title);
  const p=document.createElement('p');p.textContent=text;article.append(p);$('messages').append(article);
  $('messages').scrollTop=$('messages').scrollHeight;
  return article;
}
async function sendMessage(text) {
  if(busy || !text.trim()) return;
  busy=true; $('send').disabled=true; $('apply').disabled=true; $('chat-status').textContent='Reading current data and calling tools…';
  addMessage('user',text); $('prompt').value='';
  try {
    const result=await api('/api/chat',{message:text,history});
    history.push({role:'user',content:text},{role:'assistant',content:result.answer}); history=history.slice(-10);
    const node=addMessage('bot',result.answer);
    if(result.trace.length) {
      const details=document.createElement('details'); const summary=document.createElement('summary');summary.textContent=`Evidence · ${result.trace.length} tool call${result.trace.length>1?'s':''}`;
      const pre=document.createElement('pre');pre.textContent=JSON.stringify(result.trace,null,2); details.append(summary,pre);node.append(details);
    }
    for(const preview of result.previews) {const button=document.createElement('button');button.className='quiet';button.textContent='Review this preview';button.onclick=()=>showPreview(preview);node.append(button);}
    if(result.previews.length) showPreview(result.previews.at(-1));
    $('api-status').textContent='API connected';
    $('chat-status').textContent=`${result.model} · v${result.version} · ${result.usage.input_tokens+result.usage.output_tokens} tokens`;
  } catch(error) {addMessage('error',error.message);$('chat-status').textContent='Dashboard remains available. Retry after fixing the API issue.';}
  finally {busy=false;$('send').disabled=false;$('apply').disabled=false;$('messages').scrollTop=$('messages').scrollHeight;}
}
$('products').onclick=e=>{const b=e.target.closest('[data-sku]');if(b)showSku(b.dataset.sku).catch(e=>notice(e.message));};
for(const id of ['search','status','category']) $(id).addEventListener(id==='search'?'input':'change',renderRows);
for(const b of document.querySelectorAll('[data-stage]')) b.onclick=async()=>{try{showPreview(await api('/api/preview-stage',{stage:b.dataset.stage}));}catch(e){notice(e.message);}};
for(const b of document.querySelectorAll('[data-prompt]')) b.onclick=()=>{$('prompt').value=b.dataset.prompt;$('prompt').focus();};
$('chat-form').onsubmit=e=>{e.preventDefault();sendMessage($('prompt').value);};
$('prompt').onkeydown=e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();sendMessage($('prompt').value);}};
$('ask-selected').onclick=()=>{$('prompt').value=`Explain the current replenishment recommendation for ${selected}, using the calculation and any approved business context.`;$('prompt').focus();};
$('dismiss').onclick=()=>{pending=null;$('preview').hidden=true;};
$('apply').onclick=async()=>{if(!pending)return;$('apply').disabled=true;try{await api('/api/apply',{id:pending.id});pending=null;$('preview').hidden=true;notice('Reviewed change applied. Dashboard and chatbot now use the updated state.');await refresh();}catch(e){notice(e.message);}finally{$('apply').disabled=false;}};
$('anomalies').onclick=async()=>{try{$('teacher-output').textContent=JSON.stringify(await api('/api/anomalies'),null,2);}catch(e){notice(e.message);}};
$('audit').onclick=async()=>{try{$('teacher-output').textContent=JSON.stringify(await api('/api/audit'),null,2);}catch(e){notice(e.message);}};
$('export').onclick=()=>{const columns=['sku','product_name','category','status','weekly_forecast_units','recommended_order_units','first_shortage_date','unmet_units_over_horizon'];const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';const csv=[columns.join(','),...filteredRows().map(r=>columns.map(k=>quote(r[k])).join(','))].join('\r\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download=`case2-stage-${dashboard.stage.replaceAll(' ','-')}.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
(async()=>{try{const h=await api('/api/health');csrf=h.csrf;$('api-status').textContent=h.api_key_configured?'Key configured':'API key needed';await refresh();}catch(e){notice(e.message);}})();
