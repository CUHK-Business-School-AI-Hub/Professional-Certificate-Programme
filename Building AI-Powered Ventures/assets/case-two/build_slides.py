"""Build the managed Case Two block from the classroom dataset."""
from pathlib import Path
import csv, re, html, json, statistics, math
HERE=Path(__file__).resolve().parent
COURSE=HERE.parents[1]
DECK=COURSE/'slides/AI-Ventures-202612-Slides-1.html'
DATA=COURSE/'data/case2'
def rows(name):
    with (DATA/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
sales=rows('student-data/weekly_sales.csv')
plans={(r['stage'],r['sku']):r for r in rows('ground-truth/expected_plans.csv')}
actual={r['sku']:r for r in rows('ground-truth/future_weekly_actuals.csv')}
def series(sku):return [int(r['units_sold']) for r in sales if r['sku']==sku]
def n(stage,sku,key,dec=0):return f"{float(plans[stage,sku][key]):.{dec}f}"
TEAL='#1f6f63';RED='#b8402f';MUTED='#666a73';LINE='#d9d5ca'
def bars(values,labels,threshold=None,weights=None):
    left=55;top=28;bottom=260;right=850
    peak=max(max(values),threshold or 0)
    tick=10 if peak<=100 else 20
    maximum=math.ceil(peak*1.05/tick)*tick or 1
    step=(right-left)/len(values);bw=min(82,step*.65)
    out=['<svg class="c2-chart" viewBox="0 0 880 330" role="img" aria-label="Weekly sales; values printed above each bar">']
    for frac in (0,.5,1):
        y=bottom-(bottom-top)*frac
        out.append(f'<line x1="{left}" x2="{right}" y1="{y}" y2="{y}" stroke="{LINE}"/><text x="{left-12}" y="{y+7}" text-anchor="end" font-size="21" fill="{MUTED}">{maximum*frac:.0f}</text>')
    for i,v in enumerate(values):
        tick_label=re.sub(r'^T[−-](\d+)$', r'T<tspan baseline-shift="sub" font-size="70%">−\1</tspan>', labels[i])
        x=left+i*step+(step-bw)/2;h=(bottom-top)*v/maximum;fill=RED if i==len(values)-1 else TEAL
        out.append(f'<rect x="{x:.1f}" y="{bottom-h:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{fill}" opacity="{1 if i>=len(values)-4 else .45}"/><text x="{x+bw/2:.1f}" y="{bottom-h-9:.1f}" text-anchor="middle" font-size="22" fill="#1d1f24">{v}</text><text x="{x+bw/2:.1f}" y="{bottom+28}" text-anchor="middle" font-size="21" fill="{MUTED}">{tick_label}</text>')
        if weights:out.append(f'<text x="{x+bw/2:.1f}" y="{bottom+57}" text-anchor="middle" font-size="25" fill="{TEAL}">{weights[i]}</text>')
    if threshold is not None:
        y=bottom-(bottom-top)*threshold/maximum
        out.append(f'<line x1="{left}" x2="{right}" y1="{y:.1f}" y2="{y:.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="8 6"/><text x="{right}" y="18" text-anchor="end" font-size="22" fill="{RED}">3σ upper line: {threshold:.1f}</text>')
    return ''.join(out)+'</svg>'
def inventory(delay=False):
    a=[30,20,10,50,40,30,20,20,10,0];b=[30,20,10,0,0,40,30,30,20,10]
    out=['<svg class="c2-chart" viewBox="0 0 1300 320" role="img" aria-label="CASE-002 daily closing stock, including a proposed 10-unit order on 23 November">']
    def x(i):return 70+i*126
    def y(v):return 250-v*3.2
    for v in (0,20,40,60):out.append(f'<line x1="70" x2="1210" y1="{y(v)}" y2="{y(v)}" stroke="{LINE}"/><text x="53" y="{y(v)+8}" text-anchor="end" font-size="23" fill="{MUTED}">{v}</text>')
    for i in range(10):out.append(f'<text x="{x(i)}" y="286" text-anchor="middle" font-size="23" fill="{MUTED}">{16+i} Nov</text>')
    out.append('<text x="70" y="28" font-size="23" fill="#666a73">Closing stock (units)</text>')
    for vals,col in ([(a,TEAL),(b,RED)] if delay else [(a,TEAL)]):
        points=' '.join(f'{x(i)},{y(v)}' for i,v in enumerate(vals))
        out.append(f'<polyline points="{points}" fill="none" stroke="{col}" stroke-width="4"/>')
        for i,v in enumerate(vals):out.append(f'<circle cx="{x(i)}" cy="{y(v)}" r="5" fill="{col}"/>')
    if delay:
        out.append(f'<circle cx="{x(4)}" cy="250" r="13" fill="none" stroke="{RED}" stroke-width="3"/><text x="{x(4)-25}" y="213" font-size="24" fill="{RED}">10 unmet units</text><text x="{x(5)-55}" y="92" font-size="23" fill="{RED}">+50 arrives late</text>')
        out.append(f'<text x="850" y="28" font-size="23" fill="{TEAL}">Original</text><text x="1000" y="28" font-size="23" fill="{RED}">2-day delay</text>')
    else:out.append(f'<text x="{x(3)-70}" y="62" font-size="23" fill="{TEAL}">+50 inbound</text>')
    out.append(f'<text x="{x(7)-50}" y="127" font-size="23" fill="{TEAL}">+10 new order</text>')
    return ''.join(out)+'</svg>'
def table(headers,body,widths=None,compact=False):
    cols='<colgroup>'+''.join(f'<col style="width:{w}%">' for w in widths)+'</colgroup>' if widths else ''
    return f'<table class="c2-table {"compact" if compact else ""}">{cols}<thead><tr>'+''.join(f'<th>{v}</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{v}</td>' for v in r)+'</tr>' for r in body)+'</tbody></table>'
def card(title,body,warn=False):return f'<div class="c2-card{" warn" if warn else ""}"><h3>{title}</h3><p>{body}</p></div>'
def checks(items):return '<ul class="c2-checks">'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def loopstrip():return '<div class="c2-loop-strip"><b>Save</b> → <b>Load</b> → <b>Apply</b> → <b>Maintain</b></div>'
text=DECK.read_text();logo=re.search(r'<img class="school-logo"[^>]+>',text).group()
slides=[];index=[]
def add(title,phase,loop,lead,body,bottom='',notes='',source=''):
    num=59+len(slides)
    # Keep bottom notes only where they add an essential rule or action.
    if num not in {61,63,64,69,72,78,81}:
        if bottom: notes += ' Teaching reminder: ' + re.sub('<[^>]*>', '', bottom)
        bottom=''
    if not source and num in {62,64,68,77,81}:
        source='Synthetic classroom data · Snapshot: 16 Nov 2026'
    bottom_html=f'<p class="c2-bottom">{bottom}</p>' if bottom else ''
    references_html=f'<p>Sources: {source}</p>' if source else ''
    nav=''.join(f'<strong>{p}</strong>' if p==phase else f'<span>{p}</span>' for p in ['Delegate','Evaluate','Coach']) if phase else '<strong>API setup</strong>'
    label=re.sub('<[^>]*>',' ',title)
    slides.append(f'''
      <section class="slide case-two {'c2-no-bottom' if not bottom else ''}" id="slide-{num}" aria-label="Slide {num}: {html.escape(label,quote=True)}" aria-hidden="true" inert>
        {logo}<h2>{title}</h2><p class="c2-loop">{loop}</p><p class="phase-label">{nav}</p>
        <p class="c2-lead">{lead}</p><div class="c2-body">{body}</div>
        {bottom_html}
        <aside class="speaker-notes" hidden>{notes}{references_html}</aside><span class="page-number" aria-hidden="true">{num}</span>
      </section>
''')
    index.append({'slide':num,'title':label,'phase':phase or 'Preparation','loop':loop})
slides.append(f'''<section class="slide case-one case-title case-two" id="slide-59" aria-label="Slide 59: Case Two: Replenishment Dashboard" aria-hidden="true" inert>
{logo}<p class="case-kicker">CASE TWO</p><h2>Replenishment<br>Dashboard</h2>
<p class="case-subtitle">Build an inventory app with AI,<br>then add AI to the app.</p>
<p class="c2-versions"><b>Stage 1:</b> Apply rules without an LLM at runtime.<br><b>Stage 2:</b> Work with an AI copilot to refine the plan.</p>
<div class="c2-cover-art"><svg viewBox="0 0 470 355" role="img" aria-label="An inventory chart and a chat message">
<rect x="15" y="20" width="410" height="265" fill="#ffffff" fill-opacity=".45" stroke="#a9bfb6"/><path d="M50 70v170h340" fill="none" stroke="#b9b5aa" stroke-width="2"/>
<path d="M60 100l65 45 65 40 65-100 65 55 65 45" fill="none" stroke="#1f6f63" stroke-width="5"/>
<rect x="185" y="230" width="280" height="105" rx="8" fill="#f7f6f1" stroke="#b8402f"/><path d="M210 260h205M210 285h150M210 310h180" stroke="#b8402f" stroke-width="3"/>
</svg></div><p class="case-method"><b>Delegate</b><span>·</span><b>Evaluate</b><span>·</span><b>Coach</b></p>
<span class="page-number" aria-hidden="true">59</span>
<aside class="speaker-notes" hidden>Continue the learner-owned protective-case business. Build and evaluate the ordinary program before adding the API-connected chatbot. Use Delegate, Evaluate, Coach throughout. The illustration does not claim an implemented dashboard.</aside></section>''')
index.append({'slide':59,'title':'Case Two: Replenishment Dashboard','phase':'Introduction','loop':''})
add('What Should You Reorder?','Delegate','Loop 1 · Build the dashboard','You run a cross-border business selling protective cases.',
'''<p class="c2-story">Every week, you review <strong>200 SKUs</strong>.<br>Some are selling fast. Some have stock on the way.</p>
<div class="c2-three" style="margin-top:40px">'''+card('Which products?','Which products need<br>replenishment?')+card('How much?','How many units<br>should you order?')+card('When?','Will the stock<br>arrive in time?')+'</div>',
'Delegate a usable weekly decision tool. Define how you will check it.',
'Do not introduce wholesale, campaign or clearance answers yet. Ask what decisions the dashboard should support. The learner owns the purpose and acceptance criteria.')
add('Start with Two Data Files','Delegate','Loop 1 · Facts and boundaries','Use the same frozen snapshot throughout the exercise.',
'''<div class="c2-two">'''+card('products.csv','200 SKUs<br>Stock, lead time and safety-stock days<br>Up to one inbound shipment per SKU')+card('weekly_sales.csv','13 complete weeks<br>17 Aug – 15 Nov 2026<br>Weekly units sold')+'''</div>
<div class="c2-chain"><article><h3>Historical facts</h3><p>Sales history ends on 15 November.</p></article><span class="c2-arrow">→</span><article><h3>Planning snapshot</h3><p>16 November, before daily sales.</p></article></div>''',
'Note: A zero is an observation. A blank is missing information.',
'Use student-data.zip only. Missing required fields must produce a specific data issue. No historical daily sales are supplied. Later daily demand values are forecasts. Instructor truth stays separate until the evaluation stage.',
'Download: <a href="../data/case2/student-data.zip">Student data package</a> · 200 SKUs / 2,600 weekly records')
add('Give Recent Sales More Weight','Delegate','Loop 1 · Agree the rule','An experience-based rule for forecasting weekly sales.',
'''<div class="c2-sales-equation">Forecast weekly sales = <strong>0.4 × T<sub>−1</sub> + 0.3 × T<sub>−2</sub> + 0.2 × T<sub>−3</sub> + 0.1 × T<sub>−4</sub></strong></div>
<div class="c2-term-grid">
  <div><h3>T<sub>−1</sub></h3><p>Sales in the most recent<br>complete week</p><span>9–15 Nov 2026</span><b>91 units</b><small>Weight: 0.4</small></div>
  <div><h3>T<sub>−2</sub></h3><p>Sales two complete<br>weeks ago</p><span>2–8 Nov 2026</span><b>70 units</b><small>Weight: 0.3</small></div>
  <div><h3>T<sub>−3</sub></h3><p>Sales three complete<br>weeks ago</p><span>26 Oct–1 Nov 2026</span><b>63 units</b><small>Weight: 0.2</small></div>
  <div><h3>T<sub>−4</sub></h3><p>Sales four complete<br>weeks ago</p><span>19–25 Oct 2026</span><b>56 units</b><small>Weight: 0.1</small></div>
</div>
<div class="c2-sales-result"><p><strong>CASE-001: 75.6 units / week</strong></p><p>Daily forecast = 75.6 ÷ 7 = <strong>10.8 units / day</strong></p></div>''',
'',
'The coefficients are a rule drawn from operating experience. Each T with a negative subscript denotes units sold in a past complete week, not subtraction from T. The most recent completed week receives weight 0.4. The four weights sum to one. This is a weekly forecast; divide by seven for the uniform daily forecast used in this exercise.')
add('Calculate the Replenishment Quantity','Delegate','Loop 1 · Agree the rule','Plan the quantity and check delivery timing separately.',
'''<div class="c2-rule">Coverage days = <strong>lead time + safety-stock days</strong></div>
<div class="c2-rule">Target demand = <strong>daily forecast × coverage days</strong></div>
<div class="c2-rule">Suggested order = <strong>ceil(max(0, target demand − stock − eligible inbound))</strong></div>
<p class="c2-small" style="margin-top:24px">For a 10-day window starting 16 Nov, include receipts on 16–25 Nov.<br>A receipt on 26 Nov belongs outside that window.</p>''',
'Round the final order quantity up. Flag missing inputs.',
'Eligibility is as_of_date <= available_date < as_of_date + coverage_days. Current stock excludes inbound. The aggregate rule plans full forecast demand without optimising timing or deducting expected lost sales. It does not guarantee absence of stockout.')
add('Check When Stock Will Be Available','Delegate','Loop 1 · Agree the timeline','Enough supply can still arrive too late.',
inventory()+'''<p class="c2-small" style="margin-top:15px">Opening stock: 40 · Daily demand: 10 · Existing inbound: 50 on 19 Nov<br>Proposed order: 10, available on 23 Nov · Forecast window: 16–25 Nov</p>''',
'Keep stock at zero or above. Record unmet demand separately.',
'The curve includes the proposed ten-unit order. A seven-day lead time from 16 November means availability on 23 November. Sales=min(available,demand); closing stock=available-sales; unmet demand=demand-sales and is lost, not backordered. Chart points are day-end stock.')
add('Delegate: Define the First Version','Delegate','Loop 1 · The five-element brief','Could a new collaborator build it from this brief?',
table(['Element','What you ask the agent to do'],[
('Goal','Build a weekly replenishment dashboard.'),
('Facts','Use the supplied data and agreed business rules.'),
('Examples','Use the interface sketch on the next slide as a layout example.'),
('Standards','Apply the agreed rules correctly and flag missing inputs.'),
('Boundaries','Preserve raw data. Generate recommendations for review.')],[21,79],True),
'Ask for a working page, calculation evidence and a short run guide.',
'Use the five elements from slide 33. The completeness check from slide 41 includes outcome, context, quality, evidence and boundary. Save the confirmed brief. Ordinary development tools are enough; no model API is needed yet.')
add('Build the First Version','Delegate','Loop 1 · Agent delivery','Ask the agent to build an app that runs without an LLM.',
'''<div class="c2-two"><div class="c2-dashboard"><p class="c2-kicker">Interface sketch</p><div class="c2-dash-kpis"><div><b>Stock</b>Overall position</div><div><b>Orders</b>Recommended units</div><div><b>Issues</b>Needs review</div></div><div class="c2-dash-grid"><div><h3>SKU list &amp; filters</h3><table><tr><td>CASE-001</td><td>Inspect →</td></tr><tr><td>CASE-002</td><td>Inspect →</td></tr><tr><td>CASE-003</td><td>Inspect →</td></tr></table></div><div><div class="c2-dash-mini">Weekly sales<br>History and weights</div><div class="c2-dash-mini">Daily stock<br>Receipts and shortages</div></div></div></div><div>'''+checks(['Load the sample data.','Inspect an individual SKU.','Change an input and recalculate.'])+'''<p class="c2-note">Save the first results<br>for comparison.</p></div></div>''',
'AI helps build the program. The dashboard runs without an LLM.',
'This is a layout sketch, not an implemented product screenshot. Learners have Codex build and run the app, inspect its actual screen and preserve the initial calculation output for a fair comparison.')
add('Evaluate: Does the App Calculate Correctly?','Evaluate','Loop 1 · Factual checks','Check CASE-001 against a calculation you do by hand.',
'''<div class="c2-two"><div><div class="c2-rule">75.6 ÷ 7 = <strong>10.8 units / day</strong></div><div class="c2-rule">10.8 × (7 + 3) = <strong>108 units</strong></div><div class="c2-rule">108 − 40 − 0 = <strong>68 units to order</strong></div></div><div>'''+checks(['<b>CASE-003:</b> enough stock → 0.','<b>CASE-005:</b> round up → 13.','<b>CASE-006:</b> zero demand → 0.','<b>Missing input:</b> flag it; do not assume 0.'])+'</div></div>',
'Check arithmetic, time units and missing-data behaviour.',
'These are reference checks, not claims that an app has passed. CASE-005: 17/7*10−12=12.2857..., which rounds up to 13. Preserve these checks after changes.')
v13=series('CASE-013')
add('Evaluate: Does the Forecast Make Sense?','Evaluate','Loop 1 · Compare with actual demand','CASE-013: the calculation is correct, but the forecast is high.',
f'''<div class="c2-two chart-left"><div>{bars(v13,[f'T−{13-i}' for i in range(13)])}<p class="c2-small">Observed weekly sales · Look at the most recent week.</p></div><div><p class="c2-kicker">Next-week demand</p><div class="c2-metric-pair"><div><p class="c2-big">{n('A','CASE-013','weekly_forecast_units',1)}</p><p class="c2-unit">forecast</p></div><div><p class="c2-big">{actual['CASE-013']['customer_demand']}</p><p class="c2-unit">actual</p></div></div><p class="c2-note">What happened in the week<br>with 140 units sold?</p></div></div>''',
'Find the cause of the gap before changing the rule.',
'Reveal this synthetic next-week comparison after the initial run has been saved. Compare forecast to customer_demand; stockouts can reduce realised sales. Do not let the original build read instructor files or disclose campaign and clearance facts yet.')
baseline=v13[:9];threshold=statistics.mean(baseline)+3*statistics.stdev(baseline)
add('Coach: Handle Exceptional Sales','Coach','Loop 1 · Diagnose and revise','An unusually high week may include a one-off wholesale order.',
f'''<div class="c2-two"><div class="c2-card warn"><h3>CASE-013</h3><p>Baseline mean (T<sub>−13</sub> to T<sub>−5</sub>): <strong>28.0</strong><br>Sample standard deviation: <strong>5.32</strong><br>Upper 3σ line: <strong>{threshold:.2f}</strong></p><p>Recent week: <strong>140 units</strong><br>Possible cause: a one-off wholesale order.</p></div><div><p class="c2-kicker">Ask the agent to update the app and rules.md</p><pre class="c2-code">Flag recent weeks above mean + 3σ.
Review the flagged observations.
Exclude confirmed exceptional weeks.
Renormalise the remaining weights.
Preserve the original sales.</pre></div></div>''',
'Inspect the rule change, then rerun the original task.',
'Use T−13 through T−5 and sample SD with n−1. The high week must not raise its own baseline. Treat wholesale as a possible explanation, then review the flagged weeks before excluding them. The instructor event record supplies the confirmation for this simulation. Excluding T−1 leaves weights 0.3,0.2,0.1 summing to 0.6; retain their time positions and divide by 0.6. A flag alone is not proof of wholesale.')
add('Evaluate: Rerun After Coaching','Evaluate','Loop 1 · Close the loop','Rerun the checks. Actual next-week demand is still 27 units.',
table(['Reference check','First version','After coaching'],[
('CASE-013 forecast / week',n('A','CASE-013','weekly_forecast_units',1),n('B','CASE-013','weekly_forecast_units',2)),
('CASE-013 order',n('A','CASE-013','recommended_order_units'),n('B','CASE-013','recommended_order_units')),
('CASE-001 order','68','68 — unchanged'),('CASE-196','Needs data','Still needs data')],[45,25,30])+loopstrip(),
'Record what improved, what stayed correct and what remains unresolved.',
'Stage B reference. CASE-013 becomes (0.3*28+0.2*29+0.1*27)/0.6=28.1667, not exactly the future demand of 27. Compare the actual app to these expectations. Save the failure, rule diff and recheck. This closes the first loop before the model API.')

add('Next Step: Add a chatbot as copilot','Delegate','Stage 2 · Build an AI-powered product','Work with a copilot to interpret context and refine the plan.',
'''<div class="c2-chain" style="margin-top:0"><article><h3>Stage 1 · Build with AI</h3><p>A rule-based dashboard<br>No LLM at runtime</p></article><span class="c2-arrow">→</span><article><h3>Stage 2 · Build an AI-powered product</h3><p>A dashboard with an AI copilot<br>You decide; the copilot assists</p></article></div>
<div class="c2-three" style="margin-top:32px">'''+card('Share new knowledge','Give the copilot business facts and temporary updates it does not yet have.')+card('Explore options together','Ask questions, compare scenarios and refine the plan with the copilot.')+card('Support business judgment','Let the copilot clarify instructions and explain exceptions. You make the decisions.')+'</div>',
'',
'This is the transition between two development stages. Stage 1 uses AI to build ordinary software and completes a Delegate, Evaluate, Coach loop. Stage 2 adds an LLM-powered copilot that works alongside the user. The user supplies context, considers alternatives and confirms decisions; the copilot helps interpret information, propose adjustments and explain results. The existing calculator still computes quantities; proposed changes remain subject to review. Obtain API access on the next page before delegating this new version.')

add('Get API Access for the Next Version',None,'Preparation for Loop 2','What if the app needs an LLM while it is running?',
'''<div class="c2-three">'''+card('1. Claim credits','ChatGPT<br><strong>Settings → Billing</strong><br>Activate the Pro API benefit.')+card('2. Create a key','API Platform<br><strong>Project → API Keys</strong><br>Create a new secret key.')+card('3. Save locally','Ask the agent to prepare<br>a backend <strong>.env</strong> file.<br>Paste the key there yourself.')+'''</div>
<div class="c2-api-ready"><pre class="c2-code"># Backend .env
OPENAI_API_KEY=your_private_key

# .gitignore
.env</pre><div><p class="c2-kicker">Before you continue</p><p class="c2-small">Pro eligibility: a paid subscription active for at least 7 days.<br>Check credits in the linked API organization.<br>Keep the key out of chat and frontend code.</p></div></div>''',
'Make one small API call before continuing.',
'Use the same account email and an API organization the learner owns. The first grant can be prorated and monthly credits expire at cycle end. Create the key in that organization. This is setup between loops. Use the PDF for illustrated steps and the DeepSeek alternative. No key is embedded in this deck.',
'<a href="../guides/API%20Access%20Guide.pdf" target="_blank">Illustrated API Access Guide</a> · <a href="https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions" target="_blank" rel="noopener">Official credit benefit</a> · Checked 18 Nov 2026')
add('Delegate: Build the Copilot','Delegate','Loop 2 · Build the new version','Build a copilot that helps users review and refine the plan.',
'''<blockquote class="c2-quote">“Add a chatbot copilot to help me review the replenishment plan.<br>Let me supply context, compare options and confirm proposed changes.<br>Recalculate, explain the results and save confirmed context for future requests.”</blockquote>
<div class="c2-three" style="margin-top:25px">'''+card('Understand','Interpret the information<br>I provide.')+card('Update','Propose changes<br>for my review.')+card('Recalculate','Use the existing<br>calculation tools.')+'</div>',
'Return the working feature and evidence that each check passes.',
'Five-element brief: goal=chat feature; facts=current dataset and calculator; examples=the existing dashboard and CASE-001 acceptance check; standards=correct SKU, source values and shared calculations; boundaries=preview before applying, preserve raw data, keep secrets backend-only. This is a development request to Codex. Later operating requests are made through the product.')
add('What Changes at Runtime?','Delegate','Loop 2 · Inspect the new design','You provide context and confirm changes. The copilot assists.',
'''<div class="c2-architecture">
<svg width="1376" height="415" viewBox="0 0 1376 415" style="position:absolute;inset:0" aria-hidden="true"><defs><marker id="c2-arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0 0L10 5L0 10" fill="none" stroke="#1f6f63"/></marker></defs><path d="M280 80H450" fill="none" stroke="#1f6f63" stroke-width="2" marker-end="url(#c2-arrowhead)"/><path d="M280 280H375V155H450" fill="none" stroke="#1f6f63" stroke-width="2" marker-end="url(#c2-arrowhead)"/><path d="M910 150H1045" fill="none" stroke="#1f6f63" stroke-width="2" marker-end="url(#c2-arrowhead)"/><path d="M1055 190H920" fill="none" stroke="#1f6f63" stroke-width="2" marker-end="url(#c2-arrowhead)"/><path d="M690 265V290" fill="none" stroke="#1f6f63" stroke-width="2" marker-end="url(#c2-arrowhead)"/></svg>
<div class="arch" style="left:0;top:10px;width:280px;height:145px"><h3>Dashboard</h3><p>Revised quantities<br>and explanations</p></div>
<div class="arch" style="left:0;top:210px;width:280px;height:145px"><h3>Chatbot copilot</h3><p>You ask, review<br>and confirm</p></div>
<div class="arch" style="left:460px;top:65px;width:450px;height:200px"><h3>Backend: context + tools</h3><p>Saves confirmed context<br>Runs calculation tools<br>Returns updated results</p></div>
<div class="arch model" style="left:1055px;top:75px;width:321px;height:190px"><h3>LLM through API</h3><p>Interprets the message<br>Suggests an update</p></div>
<div class="arch" style="left:460px;top:300px;width:450px;height:110px"><h3>Shared data and calculator</h3><p>One source of numerical results</p></div>
<p class="arch-label" style="left:940px;top:110px">request</p><p class="arch-label" style="left:930px;top:210px">response</p></div>''',
'The model requests actions. Your backend executes the tools.',
'The LLM does not directly edit a browser or database here. The backend orchestrates model-tool interaction and executes allowed functions on current application state. Both interfaces use the same calculator. Ask the agent to trace one input through this design.')
add('Evaluate: Check the New App','Evaluate','Loop 2 · Test the product behaviour','Test through the interface a user will see.',
table(['Test','Expected behaviour'],[
('Ask about CASE-001','Cite the selected SKU and explain its 68-unit order.'),
('Change stock from 40 to 50','After confirmation, both the table and answer show 58 units.'),
('Ask about missing data','State what is missing; ask for the needed information.'),
('Make the API unavailable','Show the error; ordinary calculations still work.')],[37,63]),
'Compare the answer, tool result and dashboard against the same inputs.',
'Restore stock to 40 after the temporary change. Simulate API failure safely in the local exercise. Use independent arithmetic and inspect browser behaviour. A connection test alone does not prove feature correctness.')
add('Share Context with the Copilot','Coach','Loop 2 · Add business context','Some business information is not recorded in the sales table.',
'''<div class="c2-three">'''+card('Which products?','Identify the affected SKU<br>or group of products.')+card('Which dates?','Specify the event period<br>or effective date.')+card('What changed?','Explain the business fact<br>or operating decision.')+'''</div>
<div class="c2-loop-strip" style="margin-top:48px"><b>Your context</b> → <b>Copilot proposal</b> → <b>Your confirmation</b> → <b>Updated plan</b></div>''',
'',
'This page introduces how a business owner works with the copilot by supplying additional context. The copilot supports human judgment; the user confirms changes and owns the decision. The LLM interprets a message and the backend proposes a scoped update. The user reviews it before it is saved and used by the calculation tools. Do not introduce a separate software-debugging loop here. If a real implementation fault occurs, fix and recheck it as needed, without diverting the teaching narrative.')
v33=series('CASE-033');th33=statistics.mean(v33[:9])+3*statistics.stdev(v33[:9])
add('Evaluate: What Is Missing from the Data?','Evaluate','Loop 2 · Business context','“Prepare the next weekly plan.” Now inspect CASE-033.',
f'''<div class="c2-two chart-left"><div>{bars(v33,[f'T−{13-i}' for i in range(13)],threshold=th33)}<p class="c2-small">The recent weeks do not cross the 3σ line.</p></div><div><p class="c2-kicker">Next-week demand</p><div class="c2-metric-pair"><div><p class="c2-big">{n('B','CASE-033','weekly_forecast_units',1)}</p><p class="c2-unit">forecast</p></div><div><p class="c2-big">{actual['CASE-033']['customer_demand']}</p><p class="c2-unit">actual</p></div></div><p class="c2-note">What business information<br>could explain the difference?</p></div></div>''',
'A correct calculation can still lack important context.',
'The operational delegation in Loop 2 is to generate the next plan from current data and saved rules. Evaluate that plan, then coach the product with facts. Reveal this comparison before naming the campaign. The 3-sigma line is computed from the nine older weeks.')
add('Coach: Explain the Member Day Campaign','Coach','Loop 2 · Explain the business event','Tell the copilot which SKU, which weeks and what changed.',
'''<div class="c2-two"><div><blockquote class="c2-quote">“CASE-033 was included in Member Day promotions on <strong>2–8 November</strong> and <strong>9–15 November</strong>.<br>Sales were about <strong>50% higher than normal</strong>.<br>There is no campaign next week.”</blockquote></div><div class="c2-card"><h3>Inspect the proposed adjustment</h3><p>150 ÷ 1.5 = <strong>100</strong><br>144 ÷ 1.5 = <strong>96</strong></p><p>Normalise only those event weeks.<br>Retain the original sales records.</p></div></div>
<p class="c2-note">Save the method in rules.md and the event details separately; reload both for the next run.</p>''',
'Review the scope. Confirm the change. Run the same calculation again.',
'Events cover complete weeks with an assumed 1.5 multiplier. Divide by 1.5 rather than subtracting 50%. Preview affected rows and persist the event after confirmation. Keep earlier wholesale exclusions if both conditions affect one week. This is a teaching assumption to validate in production.')
add('Evaluate: Check the Revised Recommendation','Evaluate','Loop 2 · Same standards, new facts','The adjustment should affect only the intended records.',
table(['Reference check','Before context','After confirmation'],[
('CASE-033 forecast / week',n('B','CASE-033','weekly_forecast_units',1),n('C','CASE-033','weekly_forecast_units',1)),
('CASE-033 order',n('B','CASE-033','recommended_order_units'),n('C','CASE-033','recommended_order_units')),
('CASE-001 order','68','68 — unchanged')],[45,25,30])+'<p class="c2-note">Reload the app. Does a new request use the saved context?</p>',
'Reload the saved event and confirm the result is reproducible.',
'Reference stages B and C. Forecast 98.4 differs from actual demand 92; correction is not perfect prediction. Show an adjusted demand basis without rewriting the recorded sales. Check a new request or reload so the event persists beyond the previous chat turn.')
add('Coach: Explain a Clearance Decision','Coach','Loop 2 · Record a business constraint','Your clearance decision overrides the order recommendation.',
'''<div class="c2-two"><blockquote class="c2-quote">“CASE-063 is marked for clearance from <strong>16 November</strong>.<br>Do not place any new replenishment orders for it.”</blockquote><div class="c2-card"><h3>After confirmation</h3><p class="c2-big">0</p><p>units to order<br>Reason: clearance</p><p>Demand remains visible.<br>Existing inbound stays scheduled.</p></div></div>
<p class="c2-note">Check the SKU and effective date before applying the policy.</p>''',
'Re-evaluate: zero new orders for this SKU; normal rules for other SKUs.',
'CASE-063 has a stage C order of 233 and stage D order of zero. Demand stays 70.2 units/week. Clearance changes the action, not forecast demand. Persist a dated SKU-specific decision and a general precedence rule. Do not cancel existing inbound. Use the original request and a normal control for the rerun.')
add('Evaluate: Check an Inbound Delay','Evaluate','Loop 2 · Preview and verify a scenario','“The CASE-002 shipment is delayed by two days.”',
inventory(delay=True)+'''<div class="c2-three" style="gap:25px;margin-top:12px"><p class="c2-small"><strong>Inbound:</strong> 19 → 21 Nov</p><p class="c2-small"><strong>Order:</strong> still 10 units</p><p class="c2-small"><strong>20 Nov:</strong> 10 unmet units</p></div>''',
'Did the app change only this shipment date, leaving the lead time for new orders unchanged?',
'Reference from delay_scenarios.csv. Both curves include ten new units on 23 November. Existing fifty-unit shipment shifts from 19 to 21 November, staying inside the ten-day window. If the model changes new-order lead time or all SKUs, diagnose that scope error, coach it and rerun the same scenario.')
add('Your Turn: Complete the Loop','Delegate','Independent practice','Use the context provided by your instructor.',
'''<div class="c2-three">'''+card('CASE-061','Apply the relevant<br>business context.')+card('CASE-003','Check that a normal SKU<br>remains correct.')+card('CASE-196','Handle missing<br>information.')+'''</div>
<div class="c2-loop-strip"><b>Delegate</b> the task → <b>Evaluate</b> with evidence → <b>Coach</b> the next run</div>
<p class="c2-note">Show your result, the evidence you checked, and one saved improvement you reused.</p>''',
'Demonstrate what changed and what stayed correct.',
'Do not reveal the combined-case answer on the page. At this stage the instructor provides the relevant records. CASE-061 combines wholesale, Member Days and clearance. Grade against stage D and inspect rule priority. Require calculation evidence and persisted context.')
add('From Sample Data to Production','Coach','Carry the method into real work','Keep the same loop when connecting real business data.',
'''<div class="c2-chain"><article><h3>Enterprise data</h3><p>ERP · WMS · Database<br>Sales, stock and shipments</p></article><span class="c2-arrow">→</span><article><h3>Controlled backend</h3><p>APIs · Permissions<br>Rules and run records</p></article><span class="c2-arrow">→</span><article><h3>Your product</h3><p>Dashboard · Copilot<br>Evidence and review</p></article></div>
<div class="c2-two" style="margin-top:30px">'''+card('Confirm with IT / data teams','Field meanings, update frequency,<br>access and write-back permissions.')+card('Confirm with business owners','Forecast rules, exceptions,<br>approval and ongoing evaluation.')+'</div>',
'Delegate clearly. Evaluate actual outcomes. Coach and retain the improvements.',
'Production data comes through backend services, controlled APIs or approved pipelines. Keep database credentials and model keys on the server. Synthetic exercise results are not production accuracy evidence. Maintain confirmed rules and context as the business changes. Day 2 remains unchanged.')
assert len(slides)==25,len(slides)
assert index[-1]['slide']==83
css='\n/* CASE TWO MANAGED CSS START */\n'+(HERE/'style.css').read_text()+'\n/* CASE TWO MANAGED CSS END */\n'
block='\n<!-- CASE TWO MANAGED SLIDES START -->\n'+''.join(slides)+'\n<!-- CASE TWO MANAGED SLIDES END -->\n'
if '<!-- CASE TWO MANAGED SLIDES START -->' in text:
    text=re.sub(r'\n<!-- CASE TWO MANAGED SLIDES START -->.*?<!-- CASE TWO MANAGED SLIDES END -->\n',lambda _:block,text,flags=re.S)
    text=re.sub(r'\n/\* CASE TWO MANAGED CSS START \*/.*?/\* CASE TWO MANAGED CSS END \*/\n',lambda _:css,text,flags=re.S)
else:
    assert len(re.findall(r'<section class="slide\b',text))==58
    text=text.replace('    .page-number {',css+'\n    .page-number {',1)
    text=text.replace('\n    </main>',block+'\n    </main>',1)
text=re.sub(r'(id="position"[^>]*>)1 / \d+(</output>)',r'\g<1>1 / 83\2',text)
text=text.replace('Day 1 principles and Case One slides for','Day 1 principles, product intelligence and replenishment slides for')
DECK.write_text(text)
(HERE/'slide-map.json').write_text(json.dumps(index,indent=2)+'\n')
print('Built Case Two: slides 59–83; 25 pages.')

