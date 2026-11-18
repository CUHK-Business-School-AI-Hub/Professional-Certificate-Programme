import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const mod=require.resolve('@oai/artifact-tool',{paths:(process.env.NODE_PATH||'').split(path.delimiter).filter(Boolean)});
const {Workbook,SpreadsheetFile}=await import(pathToFileURL(mod).href);
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../data/case2');
const previewDir=process.env.DATA_PREVIEW_DIR;
if(previewDir)await fs.mkdir(previewDir,{recursive:true});

async function book(folder,definitions,filename){
 const wb=Workbook.create();
 for(const [name,file,numeric,dateCols,note] of definitions){
  const csv=await fs.readFile(path.join(root,folder,file),'utf8');
  const imported=await Workbook.fromCSV(csv.replace(/^\uFEFF/,''),{sheetName:'Raw'});
  const matrix=imported.worksheets.getItemAt(0).getUsedRange().values;
  const headers=matrix[0];const data=matrix.slice(1).filter(r=>r[0]!==''&&r[0]!=null);
  for(const row of data)for(let j=0;j<headers.length;j++){
   if(row[j]===''||row[j]==null)row[j]=null;
   else if(numeric.includes(headers[j]))row[j]=Number(row[j]);
   else if(dateCols.includes(headers[j]))row[j]=new Date(row[j]+'T00:00:00Z');
  }
  const sh=wb.worksheets.add(name);sh.showGridLines=false;
  sh.getRange('A1').values=[[name+' - synthetic classroom data']];sh.getRange('A1').format.font={name:'Arial',size:14,bold:true};
  sh.getRange('A2').values=[[note]];sh.getRange('A2').format.font={name:'Arial',size:10,color:'#666A73'};
  const last=data.length+4;const n=headers.length;
  const table=sh.getRangeByIndexes(3,0,data.length+1,n);table.values=[headers.map(k=>k.replaceAll('_',' ')),...data];
  table.format.font={name:'Arial',size:10,color:'#1D1F24'};table.format.rowHeight=22;
  const header=sh.getRangeByIndexes(3,0,1,n);header.format.fill='#1F6F63';header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};header.format.wrapText=true;header.format.rowHeight=44;
  header.format.horizontalAlignment='center';table.format.verticalAlignment='center';
  for(let j=0;j<n;j++){
   const key=headers[j];const col=sh.getRangeByIndexes(3,j,data.length+1,1);col.format.columnWidth=key==='product_name'?47:key==='reason'||key==='note'?55:dateCols.includes(key)?17:key==='sku'?15:23;
   const vals=sh.getRangeByIndexes(4,j,data.length,1);
   if(dateCols.includes(key)){vals.setNumberFormat('yyyy-mm-dd');vals.format.horizontalAlignment='center';}
   else if(numeric.includes(key)){vals.setNumberFormat(key.includes('forecast')||key.includes('horizon')||key==='ending_inventory_units'?'0.00':key==='uplift_multiplier'?'0.0':'0');vals.format.horizontalAlignment='right';}
  }
  const excelTable=sh.tables.add(`A4:${String.fromCharCode(64+n)}${last}`,true,name.replace(/\W/g,'')+'Data');
  excelTable.style='TableStyleLight1';
  sh.freezePanes.freezeRows(4);sh.freezePanes.freezeColumns(name==='Expected plans'?2:1);
 }
 wb.recalculate();
 console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1200})).ndjson);
 if(previewDir)for(const definition of definitions){
  const sh=wb.worksheets.getItem(definition[0]);
  const cols=Math.min(sh.getUsedRange().values[3].length,8);const end=String.fromCharCode(64+cols);
  const im=await wb.render({sheetName:sh.name,range:`A1:${end}12`,scale:1.4,format:'png'});
  await fs.writeFile(path.join(previewDir,folder+'-'+sh.name.replaceAll(' ','-')+'.png'),new Uint8Array(await im.arrayBuffer()));
 }
 const out=await SpreadsheetFile.exportXlsx(wb);await out.save(path.join(root,folder,filename));
 const inspection=path.join(root,folder,filename+'.inspect.ndjson');
 try { if(previewDir)await fs.rename(inspection,path.join(previewDir,folder+'-export.inspect.ndjson'));else await fs.unlink(inspection); } catch(e) { if(e.code!=='ENOENT')throw e; }
}
await book('student-data',[
 ['Products','products.csv',['on_hand_qty','lead_time_days','safety_stock_days','inbound_qty'],['inbound_available_date'],'Snapshot: 2026-11-16. One warehouse. Quantities in pieces.'],
 ['Weekly sales','weekly_sales.csv',['units_sold'],['week_start','week_end'],'13 complete weeks: 2026-08-17 to 2026-11-15. Empty values are missing; zero is observed.']
],'Inventory Sample Data.xlsx');
await book('ground-truth',[
 ['Expected plans','expected_plans.csv',['weekly_forecast_units','daily_forecast_units','planning_days','eligible_inbound_units','recommended_order_units','unmet_units_over_horizon','ending_inventory_units','excluded_weeks'],['first_shortage_date'],'A: initial; B: wholesale reviewed; C: Member Day context; D: clearance policy.'],
 ['Weekly actuals','future_weekly_actuals.csv',['customer_demand','units_sold','unmet_demand','inbound_received','ending_inventory'],['week_start','week_end'],'Hidden simulated week: 2026-11-16 to 2026-11-22. Demand and realised sales are distinct.'],
 ['Daily actuals','future_daily_actuals.csv',['opening_inventory','inbound_received','customer_demand','units_sold','unmet_demand','closing_inventory'],['date'],'Receipts first; sales limited by stock; unmet demand is lost, not backordered.'],
 ['Business events','business_events.csv',['uplift_multiplier','one_off_units'],['week_start','week_end','effective_date'],'Instructor only. Reveal the relevant context after validation.'],
 ['Inbound outcomes','inbound_outcomes.csv',['inbound_qty','delay_days'],['planned_available_date','actual_available_date'],'Actual receipt outcomes of existing shipments; none are new student orders.']
],'Ground Truth.xlsx');
console.log('Exported both workbooks.');
