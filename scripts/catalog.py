"""Build contact sheets and searchable offline catalog (Python + Pillow)."""
import json, html
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
try: font=ImageFont.truetype('DejaVuSans.ttf',14)
except OSError: font=ImageFont.load_default()
all_records=[]
for manifest in sorted((ROOT/'assets').glob('*/manifest.json')):
 records=json.loads(manifest.read_text());all_records+=records;group=manifest.parent.name
 sheet=Image.new('RGB',(1200,288*((len(records)+4)//5)), '#e9eeef');d=ImageDraw.Draw(sheet)
 for i,r in enumerate(records):
  p=ROOT/'previews'/group/(r['id']+'.png')
  if not p.exists():continue
  im=Image.open(p).convert('RGBA');x=(i%5)*240;y=(i//5)*288;sheet.paste(im,(x,y),im);d.text((x+12,y+240),r['id'].replace('_',' '),font=font,fill='#233844');d.text((x+12,y+262),f"{r['bytes']//1024} KB",font=font,fill='#627680')
 sheet.save(ROOT/'previews'/(group+'.jpg'),quality=88)
(ROOT/'catalog.json').write_text(json.dumps(all_records,ensure_ascii=False,indent=2)+'\n')
cards=''.join(f'<article data-search="{r["category"]} {r["id"]}"><img loading="lazy" src="previews/{r["category"]}/{r["id"]}.png" alt="{r["id"]}"><h2>{r["id"]}</h2><p>{r["category"]} · {r["bytes"]//1024} KB</p><a download href="{r["path"]}">GLB download</a></article>' for r in all_records)
(ROOT/'index.html').write_text('''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Everyday GLB Library</title><style>body{margin:0;background:#edf1f2;color:#243a42;font:16px system-ui}header{padding:40px 5vw;background:#173d40;color:white}h1{margin:0 0 10px}input{padding:14px;border-radius:8px;border:0;width:min(500px,80%);font:inherit}main{padding:25px 5vw;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px}article{background:white;border-radius:12px;padding:15px}img{width:100%;aspect-ratio:1}h2{font-size:16px;overflow-wrap:anywhere}p{color:#657c82}a{color:#236e65}article[hidden]{display:none}</style><header><h1>Everyday GLB Library</h1><p style="color:#bdd4d1">Original low-poly props · meters · Y-up · embedded materials</p><input id="search" placeholder="Search: bridge, tree, chair, nature…" aria-label="Search models"></header><main>'''+cards+'''</main><script>document.querySelector('#search').addEventListener('input',e=>{const q=e.target.value.toLowerCase().trim();document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.search.includes(q))})</script></html>''')
print('Catalog:',len(all_records),'models')
