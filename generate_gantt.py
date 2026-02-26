import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

# Read data
data_dir = os.path.join(os.path.expanduser('~'), '.claude', 'projects',
    'C--Users------Desktop-Claude-Code-Demo',
    '370f5140-6c9c-4df8-88af-62792628b142', 'tool-results')
with open(os.path.join(data_dir, 'pph_data_v4_full.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

json_data = json.dumps(data, ensure_ascii=False)

html_template = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PPH商談 ガントチャート</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI','Meiryo',sans-serif; background:#f5f7fa; color:#333; }

/* === Header === */
.header { background:linear-gradient(135deg,#1a237e,#283593); color:#fff; padding:12px 24px; display:flex; align-items:center; justify-content:space-between; position:sticky; top:0; z-index:200; }
.header h1 { font-size:18px; font-weight:600; }
.header .info { font-size:13px; opacity:0.85; }

/* === Today Dashboard === */
.today-dash { background:#fff; border-bottom:2px solid #1a237e; padding:10px 24px; position:sticky; top:48px; z-index:190; }
.today-dash h2 { font-size:14px; color:#1a237e; margin-bottom:8px; display:flex; align-items:center; gap:8px; }
.today-dash h2 .badge { background:#1a237e; color:#fff; font-size:11px; padding:2px 8px; border-radius:10px; }
.dash-toggle { cursor:pointer; font-size:12px; color:#666; margin-left:auto; user-select:none; }
.dash-toggle:hover { color:#1a237e; }
.dash-grid { display:flex; gap:12px; flex-wrap:wrap; }
.dash-card { background:#f8f9ff; border:1px solid #c5cae9; border-radius:8px; padding:10px 14px; min-width:200px; max-width:320px; flex:1; }
.dash-card h3 { font-size:12px; font-weight:700; margin-bottom:6px; display:flex; align-items:center; gap:6px; }
.dash-card h3 .icon { width:20px; height:20px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; color:#fff; font-size:10px; font-weight:700; }
.dash-card ul { list-style:none; padding:0; margin:0; }
.dash-card li { font-size:11px; padding:3px 0; border-bottom:1px solid #e8eaf6; display:flex; align-items:center; gap:6px; }
.dash-card li:last-child { border-bottom:none; }
.dash-card li .pref-tag { background:#e3f2fd; color:#1565c0; font-size:9px; padding:1px 5px; border-radius:3px; white-space:nowrap; }
.dash-card li .stage-tag { font-size:9px; padding:1px 5px; border-radius:3px; white-space:nowrap; }
.dash-card li .opp-name { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:180px; font-weight:500; }
.dash-empty { color:#9e9e9e; font-size:12px; font-style:italic; padding:8px 0; }
.dash-hidden { display:none; }

/* icon colors per event type */
.ic-survey { background:#4fc3f7; }
.ic-tmpsvy { background:#81d4fa; }
.ic-koji { background:#ff9800; }
.ic-blackout { background:#f44336; }
.ic-kanko { background:#ab47bc; }
.ic-start { background:#4caf50; }
.ic-start-tmr { background:#81c784; }
.ic-naiji { background:#607d8b; }
.ic-delivery { background:#795548; }
/* stage tag colors */
.st00{background:#f5f5f5;color:#9e9e9e}.st01{background:#e3f2fd;color:#1565c0}.st04{background:#fff3e0;color:#e65100}
.st06{background:#e8f5e9;color:#2e7d32}.st08{background:#fff3e0;color:#e65100}.st09{background:#f3e5f5;color:#7b1fa2}

/* === Controls === */
.controls { background:#fff; padding:8px 24px; border-bottom:1px solid #e0e0e0; display:flex; gap:10px; align-items:center; flex-wrap:wrap; position:sticky; top:0; z-index:180; }
.controls label { font-size:12px; font-weight:500; color:#555; }
.controls select, .controls input { padding:4px 8px; border:1px solid #ccc; border-radius:4px; font-size:12px; }
.fc { font-size:13px; color:#1a237e; font-weight:700; margin-left:12px; }

/* === Gantt Table === */
.gantt-wrapper { overflow:auto; max-height:calc(100vh - 100px); position:relative; }
table { border-collapse:separate; border-spacing:0; }
th { background:#e8eaf6; padding:3px 2px; font-size:10px; font-weight:600; border:1px solid #c5cae9; white-space:nowrap; }
th.mh { background:#c5cae9; font-size:11px; text-align:center; font-weight:700; }
td { padding:2px 4px; border:1px solid #e0e0e0; font-size:11px; vertical-align:middle; }
tr:nth-child(even) td { background:#fafafa; }
tr:hover td { background:#e8eaf6 !important; }

/* ---- Sticky columns (7 cols) ---- */
/* IMPORTANT: header sticky cells need z-index:30 (sticky top + left), body cells z-index:5 */
.col-name   { width:200px; min-width:200px; max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; position:sticky; left:0;   background:#fff; z-index:5; border-right:1px solid #c5cae9; font-size:11px; padding:3px 6px; }
.col-pref   { width:56px;  min-width:56px;  max-width:56px;  white-space:nowrap; position:sticky; left:200px; background:#fff; z-index:5; border-right:1px solid #c5cae9; font-size:10px; padding:2px 3px; text-align:center; }
.col-type   { width:56px;  min-width:56px;  max-width:56px;  white-space:nowrap; position:sticky; left:256px; background:#fff; z-index:5; border-right:1px solid #c5cae9; font-size:10px; padding:2px 3px; text-align:center; }
.col-inv    { width:56px;  min-width:56px;  max-width:56px;  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; position:sticky; left:312px; background:#fff; z-index:5; border-right:1px solid #c5cae9; font-size:10px; padding:2px 3px; text-align:center; }
.col-const  { width:56px;  min-width:56px;  max-width:56px;  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; position:sticky; left:368px; background:#fff; z-index:5; border-right:1px solid #c5cae9; font-size:10px; padding:2px 3px; text-align:center; }
.col-stage  { width:110px; min-width:110px; max-width:110px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; position:sticky; left:424px; background:#fff; z-index:5; border-right:1px solid #c5cae9; font-size:10px; padding:3px 4px; }
.col-next   { width:120px; min-width:120px; max-width:120px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; position:sticky; left:534px; background:#fff; z-index:5; border-right:2px solid #1a237e; font-size:10px; padding:3px 4px; }

/* Header sticky cells: need higher z-index for both top+left */
thead th.col-name, thead th.col-pref, thead th.col-type,
thead th.col-inv, thead th.col-const,
thead th.col-stage, thead th.col-next { z-index:30; background:#e8eaf6; }

/* Even row backgrounds for sticky cols */
tr:nth-child(even) .col-name, tr:nth-child(even) .col-pref, tr:nth-child(even) .col-type,
tr:nth-child(even) .col-inv, tr:nth-child(even) .col-const,
tr:nth-child(even) .col-stage, tr:nth-child(even) .col-next { background:#fafafa; }
/* Hover */
tr:hover .col-name, tr:hover .col-pref, tr:hover .col-type,
tr:hover .col-inv, tr:hover .col-const,
tr:hover .col-stage, tr:hover .col-next { background:#e8eaf6 !important; }

/* Header row sticky top */
thead tr:first-child th { position:sticky; top:0; z-index:20; }
thead tr:nth-child(2) th { position:sticky; top:26px; z-index:20; }
/* Header sticky cols override: top + left = highest z */
thead tr:first-child th.col-name, thead tr:first-child th.col-pref, thead tr:first-child th.col-type,
thead tr:first-child th.col-inv, thead tr:first-child th.col-const,
thead tr:first-child th.col-stage, thead tr:first-child th.col-next { z-index:40; }

.nx-wait { color:#1565c0; font-weight:600; }
.nx-alert { background:#ffebee !important; color:#c62828; font-weight:700; }

/* Date cells */
.dc { width:24px; min-width:24px; max-width:24px; height:26px; padding:0; text-align:center; font-size:9px; }
.tl { background:rgba(255,0,0,0.15) !important; border-left:2px solid #f44336 !important; border-right:2px solid #f44336 !important; }
.sat { background:#e3f2fd; }
.sat-head { background:#bbdefb !important; color:#1565c0; font-weight:700; }
.sun { background:#ffebee; }
.sun-head { background:#ffcdd2 !important; color:#c62828; font-weight:700; }

.legend { display:flex; gap:12px; padding:6px 24px; background:#fff; border-top:1px solid #e0e0e0; flex-wrap:wrap; align-items:center; font-size:11px; }
.legend-item { display:flex; align-items:center; gap:3px; }
.legend-color { width:14px; height:9px; border-radius:2px; display:inline-block; }

.s00{color:#9e9e9e}.s01{color:#2196f3}.s04{color:#ff9800}.s06{color:#4caf50}.s08{color:#e65100}.s09{color:#7b1fa2}.s10{color:#1b5e20}.sl{color:#c62828}.sp{color:#795548}

/* Sort header */
th.sortable { cursor:pointer; user-select:none; }
th.sortable:hover { background:#d1d5db !important; }
th.sort-asc::after { content:' \u25b2'; font-size:8px; }
th.sort-desc::after { content:' \u25bc'; font-size:8px; }

.has-user { color:#1565c0; font-weight:600; }
.no-user { color:#bbb; }
</style>
</head>
<body>
<div class="header">
  <h1>PPH商談 ガントチャート（進行中案件）</h1>
  <div class="info">最終更新: <span id="ut"></span> | 全データ: <span id="tc"></span>件</div>
</div>

<!-- ===== Today Dashboard ===== -->
<div class="today-dash" id="todayDash">
  <h2>
    <span>\ud83d\udcc5 本日のスケジュール</span>
    <span class="badge" id="todayCount">0件</span>
    <span class="dash-toggle" id="dashToggle" onclick="toggleDash()">\u25bc \u305f\u305f\u3080</span>
  </h2>
  <div class="dash-grid" id="dashGrid"></div>
</div>

<div class="controls" id="ctrlBar">
  <label>ステータス:</label>
  <select id="sf" onchange="render()">
    <option value="all" selected>全て</option>
    <option value="const">施工以降（08-09）</option>
    <option value="00">00_潜在案件</option><option value="01">01_見極め</option>
    <option value="02">02_メリット訴求</option><option value="03">03_提案実施</option>
    <option value="04">04_意思決定者の賛同</option><option value="05">05_リスク排除</option>
    <option value="06">06_内示</option><option value="07">07_契約締結</option>
    <option value="08">08_施工中</option><option value="09">09_完工検査</option>
  </select>
  <label>都道府県:</label>
  <select id="pff" onchange="render()"><option value="all" selected>全て</option></select>
  <label>事業区分:</label>
  <select id="ctf" onchange="render()"><option value="all" selected>全て</option></select>
  <label>現調者:</label>
  <select id="ivf" onchange="render()">
    <option value="all" selected>全て</option><option value="set">設定あり</option><option value="none">未設定</option>
  </select>
  <label>施工担当:</label>
  <select id="cuf" onchange="render()">
    <option value="all" selected>全て</option><option value="set">設定あり</option><option value="none">未設定</option>
  </select>
  <label>検索:</label>
  <input type="text" id="si" placeholder="商談名..." style="width:140px;" oninput="render()">
  <label>期間:</label>
  <select id="pf" onchange="render()">
    <option value="3">3ヶ月</option><option value="6" selected>6ヶ月</option>
    <option value="12">12ヶ月</option><option value="all">全期間</option>
  </select>
  <span class="fc" id="fc"></span>
</div>
<div class="legend">
  <div class="legend-item"><div class="legend-color" style="background:#607d8b"></div>内示</div>
  <div class="legend-item"><div class="legend-color" style="background:#b3e5fc;border:1px solid #4fc3f7"></div>仮現調</div>
  <div class="legend-item"><div class="legend-color" style="background:#4fc3f7"></div>本現調</div>
  <div class="legend-item"><div class="legend-color" style="background:#795548"></div>納品</div>
  <div class="legend-item"><div class="legend-color" style="background:#ff9800"></div>着工〜完工</div>
  <div class="legend-item"><div class="legend-color" style="background:#f44336"></div>停電</div>
  <div class="legend-item"><div class="legend-color" style="background:#ab47bc"></div>完工検査</div>
  <div class="legend-item"><div class="legend-color" style="background:#4caf50"></div>稼働開始</div>
  <div class="legend-item" style="border-left:1px solid #ccc;padding-left:10px;margin-left:6px;">
    ■確定 / <span style="opacity:0.5;">□予定</span>
  </div>
  <div class="legend-item" style="border-left:1px solid #ccc;padding-left:10px;margin-left:6px;">
    <div class="legend-color" style="background:#bbdefb;border:1px solid #90caf9"></div><span style="color:#1565c0;font-weight:600;">土</span>
    <div class="legend-color" style="background:#ffcdd2;border:1px solid #ef9a9a;margin-left:6px;"></div><span style="color:#c62828;font-weight:600;">日祝</span>
  </div>
</div>
<div class="gantt-wrapper" id="gw">
  <table id="gt"></table>
</div>

<script>
const D = __DATA_PLACEHOLDER__;
const NOW = new Date(); NOW.setHours(0,0,0,0);
const NOW_T = NOW.getTime();
document.getElementById('ut').textContent = new Date().toLocaleString('ja-JP');
document.getElementById('tc').textContent = D.length;

const HOLIDAYS = new Set([
  '2025-01-01','2025-01-13','2025-02-11','2025-02-23','2025-02-24',
  '2025-03-20','2025-04-29','2025-05-03','2025-05-04','2025-05-05',
  '2025-05-06','2025-07-21','2025-08-11','2025-09-15','2025-09-23',
  '2025-10-13','2025-11-03','2025-11-23','2025-11-24',
  '2026-01-01','2026-01-12','2026-02-11','2026-02-23','2026-03-20',
  '2026-04-29','2026-05-03','2026-05-04','2026-05-05','2026-05-06',
  '2026-07-20','2026-08-11','2026-09-21','2026-09-22','2026-09-23',
  '2026-10-12','2026-11-03','2026-11-23',
  '2027-01-01','2027-01-11','2027-02-11','2027-02-23','2027-03-21',
  '2027-03-22','2027-04-29','2027-05-03','2027-05-04','2027-05-05',
  '2027-07-19','2027-08-11','2027-09-20','2027-09-23','2027-10-11',
  '2027-11-03','2027-11-23'
]);
function isHol(d){
  const y=d.getFullYear(),m=String(d.getMonth()+1).padStart(2,'0'),day=String(d.getDate()).padStart(2,'0');
  return HOLIDAYS.has(y+'-'+m+'-'+day);
}
function pd(s){if(!s||s==='null')return null;const d=new Date(s+'T00:00:00');return isNaN(d)?null:d;}
function fd(d){return d?(d.getMonth()+1)+'/'+d.getDate():'-';}
function esc(s){if(!s)return'';return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function sc(s){
  if(!s)return'';
  if(s.startsWith('00'))return's00';if(s.startsWith('01')||s.startsWith('02')||s.startsWith('03'))return's01';
  if(s.startsWith('04')||s.startsWith('05'))return's04';if(s.startsWith('06')||s.startsWith('07'))return's06';
  if(s.startsWith('08'))return's08';if(s.startsWith('09'))return's09';if(s.startsWith('10'))return's10';
  if(s==='失注')return'sl';if(s==='ペンディング')return'sp';return'';
}
function stClass(s){
  if(!s)return'st00';
  if(s.startsWith('00'))return'st00';if(s.startsWith('01')||s.startsWith('02')||s.startsWith('03'))return'st01';
  if(s.startsWith('04')||s.startsWith('05'))return'st04';if(s.startsWith('06')||s.startsWith('07'))return'st06';
  if(s.startsWith('08'))return'st08';if(s.startsWith('09'))return'st09';return'st00';
}
function getNextEvent(r){
  const evs=[
    {f:'Naijibi__c',l:'内示'},{f:'TempSurveyDate__c',l:'仮現調'},{f:'SurveyDate__c',l:'本現調'},
    {f:'Field27__c',l:'納品'},{f:'KojiSekouyoteibi__c',l:'着工'},{f:'ScheduleOfBlackoutDates__c',l:'停電'},
    {f:'KojiKankobi__c',l:'完工検査'},{f:'Kankobi__c',l:'完工'},{f:'StartDate__c',l:'稼働開始'}
  ];
  let n=null;
  for(const e of evs){const d=pd(r[e.f]);if(d&&d>=NOW&&(!n||d<n.date))n={date:d,label:e.l};}
  return n;
}

// ===== Today Dashboard =====
function buildTodayDash(){
  // Use string-based date comparison to avoid timezone issues
  const todayStr = NOW.getFullYear()+'-'+String(NOW.getMonth()+1).padStart(2,'0')+'-'+String(NOW.getDate()).padStart(2,'0');
  const TMR = new Date(NOW); TMR.setDate(TMR.getDate()+1);
  const tmrStr = TMR.getFullYear()+'-'+String(TMR.getMonth()+1).padStart(2,'0')+'-'+String(TMR.getDate()).padStart(2,'0');

  // Basic events matched on exact date string = today (no status restriction)
  const events=[
    {f:'TempSurveyDate__c', label:'\u4eee\u73fe\u8abf'},
    {f:'SurveyDate__c',     label:'\u672c\u73fe\u8abf'},
    {f:'Naijibi__c',        label:'\u5185\u793a'},
    {f:'Field27__c',        label:'\u7d0d\u54c1'},
    {f:'ScheduleOfBlackoutDates__c', label:'\u505c\u96fb'},
    {f:'KojiKankobi__c',   label:'\u5b8c\u5de5\u691c\u67fb'},
  ];

  // Categories
  const cats = ['\u4eee\u73fe\u8abf','\u672c\u73fe\u8abf','\u5185\u793a','\u7d0d\u54c1','\u505c\u96fb','\u5b8c\u5de5\u691c\u67fb',
    '\u7740\u5de5\u4e88\u5b9a\uff08\u672c\u65e5\uff09','\u65bd\u5de5\u4e2d',
    '\u958b\u901a\u4e88\u5b9a\uff08\u672c\u65e5\uff09','\u958b\u901a\u4e88\u5b9a\uff08\u660e\u65e5\uff09'];
  let todayItems = {};
  cats.forEach(c => { todayItems[c] = []; });

  let totalCount = 0;
  D.forEach(r => {
    const stg = r.StageName || '';
    // Basic date events (string comparison)
    events.forEach(e => {
      const v = r[e.f];
      if(v && v === todayStr){
        todayItems[e.label].push(r);
        totalCount++;
      }
    });
    const kojiStr = r.KojiSekouyoteibi__c || '';
    const kankoStr = r.Kankobi__c || '';
    // Today's construction start (status 08 only)
    if(kojiStr === todayStr && stg.startsWith('08')){
      todayItems['\u7740\u5de5\u4e88\u5b9a\uff08\u672c\u65e5\uff09'].push(r);
      totalCount++;
    }
    // Construction in progress (status 08/09 only, string compare YYYY-MM-DD)
    if(kojiStr && kankoStr && todayStr > kojiStr && todayStr < kankoStr
       && (stg.startsWith('08') || stg.startsWith('09'))){
      todayItems['\u65bd\u5de5\u4e2d'].push(r);
      totalCount++;
    }
    // Opening date = Kankobi (completion date), for status 08/09
    if(kankoStr && (stg.startsWith('08') || stg.startsWith('09'))){
      if(kankoStr === todayStr){
        todayItems['\u958b\u901a\u4e88\u5b9a\uff08\u672c\u65e5\uff09'].push(r);
        totalCount++;
      } else if(kankoStr === tmrStr){
        todayItems['\u958b\u901a\u4e88\u5b9a\uff08\u660e\u65e5\uff09'].push(r);
        totalCount++;
      }
    }
  });

  document.getElementById('todayCount').textContent = totalCount + '\u4ef6';

  const grid = document.getElementById('dashGrid');
  let html = '';

  // Display order with icons
  const displayOrder = [
    {label:'\u958b\u901a\u4e88\u5b9a\uff08\u672c\u65e5\uff09', icon:'\u2605', icCls:'ic-start'},
    {label:'\u958b\u901a\u4e88\u5b9a\uff08\u660e\u65e5\uff09', icon:'\u2606', icCls:'ic-start-tmr'},
    {label:'\u7740\u5de5\u4e88\u5b9a\uff08\u672c\u65e5\uff09', icon:'\u5de5', icCls:'ic-koji'},
    {label:'\u672c\u73fe\u8abf', icon:'\u73fe', icCls:'ic-survey'},
    {label:'\u4eee\u73fe\u8abf', icon:'\u4eee', icCls:'ic-tmpsvy'},
    {label:'\u65bd\u5de5\u4e2d', icon:'\u4e2d', icCls:'ic-koji'},
    {label:'\u505c\u96fb',   icon:'\u505c', icCls:'ic-blackout'},
    {label:'\u5b8c\u5de5\u691c\u67fb', icon:'\u691c', icCls:'ic-kanko'},
    {label:'\u7d0d\u54c1',   icon:'\u7d0d', icCls:'ic-delivery'},
    {label:'\u5185\u793a',   icon:'\u793a', icCls:'ic-naiji'},
  ];

  let hasAny = false;
  displayOrder.forEach(e => {
    const items = todayItems[e.label];
    if(!items || items.length === 0) return;
    hasAny = true;
    const isTmr = e.label === '\u958b\u901a\u4e88\u5b9a\uff08\u660e\u65e5\uff09';
    const cardBorder = isTmr ? 'border:1px dashed #66bb6a;' : '';
    html += '<div class="dash-card" style="'+cardBorder+'">';
    html += '<h3><span class="icon '+e.icCls+'">'+e.icon+'</span>'+e.label+'<span style="color:#666;font-weight:400;font-size:11px;">('+items.length+'\u4ef6)</span></h3>';
    html += '<ul>';
    items.forEach(r => {
      const pref = r.Prefecture || '';
      const st = r.StageName || '';
      const stc = stClass(st);
      const kankoD = pd(r.Kankobi__c);
      const kojiD = pd(r.KojiSekouyoteibi__c);
      html += '<li>';
      if(pref) html += '<span class="pref-tag">'+esc(pref)+'</span>';
      html += '<span class="opp-name" title="'+esc(r.Name)+'">'+esc(r.Name)+'</span>';
      // Show relevant sub-date per card type
      if(e.label === '\u65bd\u5de5\u4e2d' && kankoD){
        html += '<span style="font-size:9px;color:#2e7d32;margin-left:auto;white-space:nowrap;">\u5b8c\u5de5:'+fd(kankoD)+'</span>';
      } else if(e.label.includes('\u7740\u5de5') && kankoD){
        html += '<span style="font-size:9px;color:#2e7d32;margin-left:auto;white-space:nowrap;">\u5b8c\u5de5:'+fd(kankoD)+'</span>';
      } else if(e.label.includes('\u958b\u901a') && kojiD){
        html += '<span style="font-size:9px;color:#e65100;margin-left:auto;white-space:nowrap;">\u7740\u5de5:'+fd(kojiD)+'</span>';
      }
      if(st) html += '<span class="stage-tag '+stc+'">'+esc(st.substring(0,5))+'</span>';
      html += '</li>';
    });
    html += '</ul></div>';
  });

  if(!hasAny){
    html = '<div class="dash-empty">\u2705 \u672c\u65e5\u306e\u4e88\u5b9a\u306f\u3042\u308a\u307e\u305b\u3093</div>';
  }
  grid.innerHTML = html;
}

let dashOpen = true;
function toggleDash(){
  dashOpen = !dashOpen;
  document.getElementById('dashGrid').classList.toggle('dash-hidden', !dashOpen);
  document.getElementById('dashToggle').textContent = dashOpen ? '\u25bc \u305f\u305f\u3080' : '\u25b6 \u3072\u3089\u304f';
}

buildTodayDash();

// ===== Filters =====
const prefSet=new Set(), ctSet=new Set();
D.forEach(r=>{if(r.Prefecture)prefSet.add(r.Prefecture);if(r.ConstractType__c)ctSet.add(r.ConstractType__c);});
const pfSel=document.getElementById('pff');
[...prefSet].sort().forEach(p=>{const o=document.createElement('option');o.value=p;o.textContent=p;pfSel.appendChild(o);});
const ctSel=document.getElementById('ctf');
[...ctSet].sort().forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;ctSel.appendChild(o);});

let sortCol='',sortDir='asc';
function toggleSort(col){
  if(sortCol===col){sortDir=sortDir==='asc'?'desc':'asc';}
  else{sortCol=col;sortDir='asc';}
  render();
}

function render(){
  const sf=document.getElementById('sf').value;
  const si=document.getElementById('si').value.toLowerCase();
  const pf=document.getElementById('pf').value;
  const pfv=document.getElementById('pff').value;
  const ctv=document.getElementById('ctf').value;
  const ivv=document.getElementById('ivf').value;
  const cuv=document.getElementById('cuf').value;

  let f=D.filter(r=>{
    if(si&&!r.Name.toLowerCase().includes(si))return false;
    const s=r.StageName||'';
    if(sf!=='all'){if(sf==='const'){if(!s.startsWith('08')&&!s.startsWith('09'))return false;}else if(!s.startsWith(sf))return false;}
    if(pfv!=='all'&&(r.Prefecture||'')!==pfv)return false;
    if(ctv!=='all'&&(r.ConstractType__c||'')!==ctv)return false;
    if(ivv==='set'&&!r.InvestigationUserName)return false;
    if(ivv==='none'&&r.InvestigationUserName)return false;
    if(cuv==='set'&&!r.ConstUserName)return false;
    if(cuv==='none'&&r.ConstUserName)return false;
    return true;
  });

  if(sortCol){
    f.sort((a,b)=>{
      let va,vb;
      if(sortCol==='name'){va=a.Name||'';vb=b.Name||'';}
      else if(sortCol==='pref'){va=a.Prefecture||'\uff9d';vb=b.Prefecture||'\uff9d';}
      else if(sortCol==='type'){va=a.ConstractType__c||'\uff9d';vb=b.ConstractType__c||'\uff9d';}
      else if(sortCol==='inv'){va=a.InvestigationUserName||'\uff9d';vb=b.InvestigationUserName||'\uff9d';}
      else if(sortCol==='const'){va=a.ConstUserName||'\uff9d';vb=b.ConstUserName||'\uff9d';}
      else if(sortCol==='stage'){va=a.StageName||'';vb=b.StageName||'';}
      else if(sortCol==='next'){
        const ea=getNextEvent(a),eb=getNextEvent(b);
        va=ea?ea.date.getTime():9999999999999;
        vb=eb?eb.date.getTime():9999999999999;
        return sortDir==='asc'?va-vb:vb-va;
      }
      else{va='';vb='';}
      if(typeof va==='string'){const c=va.localeCompare(vb,'ja');return sortDir==='asc'?c:-c;}
      return sortDir==='asc'?va-vb:vb-va;
    });
  }else{
    f.sort((a,b)=>{
      const da=pd(a.KojiSekouyoteibi__c)||pd(a.Kankobi__c)||new Date('2099-01-01');
      const db=pd(b.KojiSekouyoteibi__c)||pd(b.Kankobi__c)||new Date('2099-01-01');
      return da-db;
    });
  }

  document.getElementById('fc').textContent=f.length+'\u4ef6 / '+D.length+'\u4ef6\u4e2d';

  let sd,ed;
  if(pf==='all'){sd=new Date('2025-01-01');ed=new Date('2027-06-30');}
  else{
    const m=parseInt(pf);
    sd=new Date(NOW.getFullYear(),NOW.getMonth(),1);
    ed=new Date(NOW);ed.setMonth(ed.getMonth()+m+1);ed.setDate(0);
  }

  let mons=[],cm=-1,md=0,cd=new Date(sd);
  while(cd<=ed){const m=cd.getFullYear()*100+cd.getMonth();if(m!==cm){if(cm!==-1)mons.push({m:cm,d:md});cm=m;md=0;}md++;cd.setDate(cd.getDate()+1);}
  if(md>0)mons.push({m:cm,d:md});

  // Header 1 - sticky cols + months
  const scs=['name','pref','type','inv','const','stage','next'];
  const scl=['\u5546\u8ac7\u540d','\u770c','\u533a\u5206','\u73fe\u8abf\u8005','\u65bd\u5de5\u62c5\u5f53','\u30b9\u30c6\u30fc\u30bf\u30b9','\u6b21\u306e\u4e88\u5b9a'];
  const scc=['col-name','col-pref','col-type','col-inv','col-const','col-stage','col-next'];
  let mr='<tr>';
  for(let i=0;i<scs.length;i++){
    let cls=scc[i]+' sortable';
    if(sortCol===scs[i])cls+=' sort-'+(sortDir==='asc'?'asc':'desc');
    mr+='<th class="'+cls+'" rowspan="2" style="font-size:11px;cursor:pointer;" onclick="toggleSort(\''+scs[i]+'\')">'+scl[i]+'</th>';
  }
  mons.forEach(m=>{const y=Math.floor(m.m/100),mn=(m.m%100)+1;mr+='<th class="mh" colspan="'+m.d+'">'+y+'/'+mn+'</th>';});
  mr+='</tr>';

  // Header 2 - day numbers
  let dr='<tr>';cd=new Date(sd);
  while(cd<=ed){
    const dw=cd.getDay(),hol=isHol(cd),isSat=(dw===6),isSun=(dw===0),isTl=(cd.getTime()===NOW_T),dn=cd.getDate();
    let cls='dc',hc='';
    if(hol||isSun){cls+=' sun';hc=' sun-head';}else if(isSat){cls+=' sat';hc=' sat-head';}
    if(isTl)cls+=' tl';
    dr+='<th class="'+cls+hc+'" title="'+(cd.getMonth()+1)+'/'+dn+(hol?' (\u795d)':'')+'">'+dn+'</th>';
    cd.setDate(cd.getDate()+1);
  }
  dr+='</tr>';

  // Body rows
  let tb='';
  f.forEach(r=>{
    const koji=pd(r.KojiSekouyoteibi__c),kanko=pd(r.Kankobi__c),kojiK=pd(r.KojiKankobi__c);
    const stD=pd(r.StartDate__c),bl=pd(r.ScheduleOfBlackoutDates__c);
    const ts=pd(r.TempSurveyDate__c),sv=pd(r.SurveyDate__c);
    const dl=pd(r.Field27__c),nj=pd(r.Naijibi__c);
    const kk=r.KojiSekouKakuteibi__c===true||r.KojiSekouKakuteibi__c==='true';

    const nxEv=getNextEvent(r);
    let nxH='',nxC='col-next';
    if(nxEv){nxC+=' nx-wait';nxH=nxEv.label+'\u5f85\u3061 '+fd(nxEv.date);}
    else{nxC+=' nx-alert';nxH='\u26a0 \u4e88\u5b9a\u306a\u3057';}

    const pref=r.Prefecture||'-';
    const ctype=r.ConstractType__c||'-';
    const invName=r.InvestigationUserName||'';
    const constName=r.ConstUserName||'';
    const invCls=invName?'has-user':'no-user';
    const constCls=constName?'has-user':'no-user';

    tb+='<tr>';
    tb+='<td class="col-name" title="'+esc(r.Name)+'">'+esc(r.Name)+'</td>';
    tb+='<td class="col-pref">'+esc(pref)+'</td>';
    tb+='<td class="col-type">'+esc(ctype)+'</td>';
    tb+='<td class="col-inv '+invCls+'" title="'+esc(invName||'\u672a\u8a2d\u5b9a')+'">'+(invName?esc(invName):'-')+'</td>';
    tb+='<td class="col-const '+constCls+'" title="'+esc(constName||'\u672a\u8a2d\u5b9a')+'">'+(constName?esc(constName):'-')+'</td>';
    tb+='<td class="col-stage '+sc(r.StageName)+'">'+(r.StageName||'')+'</td>';
    tb+='<td class="'+nxC+'" title="'+(nxEv?nxEv.label+'\u5f85\u3061 '+fd(nxEv.date):'\u4e88\u5b9a\u306a\u3057')+'">'+nxH+'</td>';

    cd=new Date(sd);
    while(cd<=ed){
      const dw=cd.getDay(),hol=isHol(cd),isSat=(dw===6),isSun=(dw===0),isTl=(cd.getTime()===NOW_T),t=cd.getTime();
      let cls='dc';
      if(hol||isSun)cls+=' sun';else if(isSat)cls+=' sat';
      if(isTl)cls+=' tl';
      let bg='',tt='';
      if(nj&&t===nj.getTime()){bg='background:#607d8b;';tt='\u5185\u793a\u65e5:'+fd(nj);}
      if(ts&&t===ts.getTime()){bg='background:#b3e5fc;border:2px solid #4fc3f7;';tt='\u4eee\u73fe\u8abf:'+fd(ts);}
      if(sv&&t===sv.getTime()){bg='background:#4fc3f7;';tt='\u672c\u73fe\u8abf:'+fd(sv);}
      if(dl&&t===dl.getTime()){bg='background:#795548;';tt='\u7d0d\u54c1:'+fd(dl);}
      if(koji&&kanko&&t>=koji.getTime()&&t<=kanko.getTime()){
        bg=kk?'background:#ff9800;':'background:#ffe0b2;';
        tt='\u7740\u5de5:'+fd(koji)+' \u301c \u5b8c\u5de5:'+fd(kanko)+(kk?' (\u78ba\u5b9a)':' (\u4e88\u5b9a)');
      }else if(koji&&!kanko&&t===koji.getTime()){
        bg='background:#ffe0b2;border-left:3px solid #ff9800;';tt='\u7740\u5de5(\u4e88\u5b9a):'+fd(koji);
      }
      if(bl&&t===bl.getTime()){bg='background:#f44336;';tt='\u505c\u96fb\u65e5:'+fd(bl);}
      if(kojiK&&t===kojiK.getTime()){bg='background:#ab47bc;';tt='\u5b8c\u5de5\u691c\u67fb:'+fd(kojiK);}
      if(stD&&t===stD.getTime()){bg='background:#4caf50;';tt='\u7a3c\u50cd\u958b\u59cb:'+fd(stD);}
      const st=bg?' style="'+bg+'"':'';
      const ttt=tt?' title="'+tt+'"':'';
      tb+='<td class="'+cls+'"'+st+ttt+'></td>';
      cd.setDate(cd.getDate()+1);
    }
    tb+='</tr>';
  });

  document.getElementById('gt').innerHTML='<thead>'+mr+dr+'</thead><tbody>'+tb+'</tbody>';

  setTimeout(()=>{
    const tds=document.querySelectorAll('.tl');
    if(tds.length>0)tds[0].scrollIntoView({inline:'center',block:'nearest'});
  },100);
}

render();
</script>
</body>
</html>'''

# Replace placeholder with actual data
html_content = html_template.replace('__DATA_PLACEHOLDER__', json_data)

outpath = os.path.join(os.path.expanduser('~'), 'Desktop', 'Claude_Code_Demo', 'pph_gantt_chart.html')
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Gantt chart HTML created: {outpath}')
print(f'Total records: {len(data)}')
