from pathlib import Path
from io import BytesIO
import re,base64
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'guides/API Access Guide.pdf'
W,H=595.276,841.89
M=42; CW=W-2*M
INK=HexColor('#1d1f24'); TEAL=HexColor('#1f6f63'); RED=HexColor('#b8402f'); MUTED=HexColor('#666a73'); LINE=HexColor('#d9d5ca'); BG=HexColor('#f7f6f1')
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('API Access Guide | Building AI-Powered Ventures');c.setAuthor('CUHK Business School')
logo=re.search(r'<img class="school-logo"[^>]*src="data:image/[^;]+;base64,([^"]+)"',(ROOT/'slides/AI-Ventures-202612-Slides-1.html').read_text()).group(1)
logo=ImageReader(BytesIO(base64.b64decode(logo)))
def text(txt,x,y,w=CW,size=11,color=INK,bold=False,leading=None):
 st=ParagraphStyle('p',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,leading=leading or size*1.38,textColor=color)
 p=Paragraph(txt,st); _,h=p.wrap(w,H);p.drawOn(c,x,H-y-h);return h

def rect(x,y,w,h,fill=None,stroke=LINE,r=0):
 c.setFillColor(fill or BG);c.setStrokeColor(stroke);c.setLineWidth(.7)
 if r:c.roundRect(x,H-y-h,w,h,r,stroke=1,fill=1)
 else:c.rect(x,H-y-h,w,h,stroke=1,fill=1)

def page(n,tag,title,sub):
 c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
 c.drawImage(logo,M,H-72,width=44,height=44,mask='auto')
 text('BUILDING AI-POWERED VENTURES',M+57,32,CW-57,9,TEAL,True)
 text(tag.upper(),M+57,49,CW-57,9,MUTED)
 text(title,M,94,CW,26,INK,True,29)
 text(sub,M,132,CW,11,MUTED)
 c.setStrokeColor(LINE);c.line(M,43,W-M,43)
 text('Checked 18 November 2026  |  API access for the classroom product',M,805,CW-32,7.5,MUTED)
 text(str(n),W-M-16,804,16,9,MUTED)

def link(label,url,x,y,w=CW,size=9):
 return text(f'<link href="{url}" color="#1f6f63"><u>{label}</u></link>',x,y,w,size)

def step(n,title,body,y,h=62):
 c.setFillColor(TEAL);c.circle(M+12,H-y-12,12,stroke=0,fill=1)
 c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',10);c.drawCentredString(M+12,H-y-16,str(n))
 text(title,M+36,y,CW-36,12,INK,True)
 text(body,M+36,y+22,CW-36,10.5)

def box(title,body,y,h,color=TEAL):
 rect(M,y,CW,h,HexColor('#edf3ef'),HexColor('#bdcec4'),5)
 text(title,M+16,y+13,CW-32,12,color,True)
 text(body,M+16,y+35,CW-32,10.5)

def flow(labels,y,h=67):
 gap=18; bw=(CW-gap*(len(labels)-1))/len(labels)
 for i,(title,body) in enumerate(labels):
  x=M+i*(bw+gap);rect(x,y,bw,h,HexColor('#ffffff'),HexColor('#a9bfb6'),4)
  text(title,x+10,y+11,bw-20,11,TEAL,True)
  text(body,x+10,y+32,bw-20,9.5,MUTED)
  if i<len(labels)-1:
   c.setStrokeColor(TEAL);cy=H-y-h/2;c.line(x+bw+3,cy,x+bw+gap-3,cy);c.line(x+bw+gap-7,cy+3,x+bw+gap-3,cy);c.line(x+bw+gap-7,cy-3,x+bw+gap-3,cy)
 text('Navigation map - illustrative; screen layout may vary.',M,y+h+8,CW,8,MUTED)

page(1,'Preferred route / OpenAI','Claim your Pro API credits','Course prerequisite: an eligible paid ChatGPT Pro plan with Codex access.')
flow([('1. Credits','Activate the benefit'),('2. API key','Create a credential'),('3. Test','Get one API reply')],169)
box('Before you start','Your paid Pro subscription must be at least <b>7 days old</b>. Use the same email for ChatGPT and the API account, and own the receiving API organization.',274,94)
step(1,'Open the benefit','In ChatGPT, go to <b>Settings &gt; Billing</b> and find the <b>API credits</b> benefit.',393)
flow([('ChatGPT','Settings'),('Billing','API credits benefit'),('Activate','Choose organization')],458,63)
step(2,'Link the correct organization','Choose your personal API organization, review the grant and confirm activation.',555)
step(3,'Check that the credits arrived','Open API Platform billing for the linked organization. Confirm the credit balance and expiry date.',622)
text('The first grant is prorated; unused monthly credits expire at billing-cycle end. An active grant needs no API payment method. This balance is separate from signed-in Codex usage.',M,696,CW,9.5,MUTED)
link('Open ChatGPT', 'https://chatgpt.com/',M,758,120)
link('API Platform billing','https://platform.openai.com/settings/organization/billing/overview',M+130,758,160)
link('Official benefit guide','https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions',M+310,758,200)
c.showPage()

page(2,'Preferred route / OpenAI','Create your OpenAI API key','Create the key inside the organization that received your credits.')
image=ImageReader(str(Path(__file__).parent/'openai-api-keys.webp'))
iw,ih=image.getSize();dw=CW;dh=dw*ih/iw
c.drawImage(image,M,H-169-dh,width=dw,height=dh,mask='auto')
text('Official OpenAI Help Center illustration. The green boxes show API keys and the create button; your interface may differ.',M,169+dh+9,CW,8,MUTED)
y=169+dh+43
step(1,'Choose your project','Open API Platform, select the credited organization, then use a project for this course.',y)
step(2,'Create a new secret key','Go to <b>Settings &gt; project &gt; API Keys</b>. Select <b>+ Create new secret key</b>. Give it a name such as <b>AI Ventures Class</b>.',y+68)
step(3,'Save the key privately','Copy the full key when it appears and store it securely. A key is a credential, not a credit balance. If it is lost, create a replacement.',y+148)
text('<b>Completion check:</b> You have an API key and a positive credit balance in the same organization.',M,738,CW,10.5,TEAL)
link('Open API Platform','https://platform.openai.com/',M,770,150,8)
link('Source: OpenAI project and key guide','https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform',M+180,770,330,8)
c.showPage()

page(3,'Alternative route / DeepSeek','Top up a small API balance','Optional fallback. The supplied Case 2 reference app uses OpenAI; a DeepSeek key needs a provider integration change.')
box('Recommended starting budget: about HK$10','This is a course budget, not a confirmed platform minimum. Check the checkout currency and total. If the smallest top-up is higher, check with the TA before paying more.',169,109)
flow([('Top Up','Choose an amount'),('Payment','Confirm the total'),('Billing','Verify the credit')],304,68)
step(1,'Sign in to the DeepSeek API Platform','Open <b>platform.deepseek.com</b>. Register or sign in, and complete any account checks requested by the platform.',411)
step(2,'Buy a small amount of credit','Open <b>Top Up</b> and select the amount closest to the HK$10 budget. The account may display CNY or USD; check the payment total before confirming.',480)
step(3,'Verify payment, then create a key','Check the result on <b>Billing</b>. Open <b>API keys</b>, create a key named <b>AI Ventures Class</b>, and save it privately.',563)
box('Which payment method?','Choose a payment method offered in your account and check the final amount. A successful chat-app login does not establish an API balance.',649,86)
text('Public documentation does not specify the current minimum top-up. Use the amount shown in your own checkout.',M,748,CW,8.5,MUTED)
link('Open API Platform','https://platform.deepseek.com/',M,772,140,8)
link('Top-up FAQ','https://static.deepseek.com/faq/index.html?lang=en',M+160,772,130,8)
link('Balance currencies','https://api-docs.deepseek.com/api/get-user-balance/',M+320,772,190,8)
c.showPage()

page(4,'Both routes / Ready for the product exercise','Connect it and check once','Your app uses the API key from its local backend.')
flow([('Browser','Your product interface'),('Local backend','Private key here'),('Model API','Returns a response')],169,77)
step(1,'Set the provider and key','Let Codex prepare a local environment file and explain where to enter the key. Paste it into that file yourself. Keep secrets out of chat, screenshots and Git.',289)
rect(M,369,CW,106,HexColor('#ffffff'),LINE,4)
text('Provider',M+15,380,110,10,TEAL,True);text('Private environment variable',M+135,380,340,10,TEAL,True)
text('OpenAI',M+15,407,110,11,INK,True);text('<font name="Courier">OPENAI_API_KEY</font>',M+135,407,340,10.5)
text('DeepSeek',M+15,438,110,11,INK,True);text('<font name="Courier">DEEPSEEK_API_KEY</font>',M+135,438,340,10.5)
step(2,'Ask Codex for one small test','Use the prompt below after you have saved the key. Confirm the test returns a short reply; never print the key.',501)
rect(M,570,CW,105,HexColor('#edf3ef'),HexColor('#bdcec4'),5)
text('Copy this instruction into Codex',M+16,582,CW-32,10,TEAL,True)
text('"Set up one minimal API test for my chosen provider. Read the key from the local backend environment. Ask the model to reply API ready. Use a small output limit. Show the response and any error, but never show the secret key."',M+16,605,CW-32,10.5)
text('<b>If it fails:</b> 401: check the key/provider. DeepSeek 402: check the balance. OpenAI 429: read the error - it may concern credits or rate limits.',M,693,CW,10)
text('<b>Ready:</b> key saved privately + credits confirmed + one successful model response.',M,744,CW,10,TEAL)
link('OpenAI key safety','https://developers.openai.com/api/docs/guides/api-keys',M,773,140,8)
link('DeepSeek API quickstart','https://api-docs.deepseek.com/',M+155,773,160,8)
link('DeepSeek error codes','https://api-docs.deepseek.com/quick_start/error_codes/',M+330,773,180,8)
c.showPage();c.save();print(OUT)
