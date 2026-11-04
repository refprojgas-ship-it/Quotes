import json, os, re, datetime, urllib.request
month = datetime.date.today().strftime("%Y-%m")
try:
    if json.load(open("quotes.json")).get("month") == month and os.environ.get("FORCE") != "1":
        print("Bulan ini sudah dibuat."); raise SystemExit
except FileNotFoundError:
    pass
prompt = ('Buat 36 quotes orisinal berbahasa Indonesia, singkat (maks 22 kata), indah dan bermakna. '
 'Kode kategori c: 0=cinta,1=kehidupan,2=semangat,3=Tuhan (netral, universal),4=psikologis,5=ilmu. '
 'Masing-masing 6 quotes per kategori. Jangan mengutip tokoh. Balas HANYA JSON array: [{"c":0,"t":"..."}]. Bulan: ' + month)
req = urllib.request.Request("https://api.anthropic.com/v1/messages",
  data=json.dumps({"model":"claude-sonnet-5-5","max_tokens":4000,"messages":[{"role":"user","content":prompt}]}).encode(),
  headers={"x-api-key":os.environ["ANTHROPIC_API_KEY"],"anthropic-version":"2023-06-01","content-type":"application/json"})
text = json.load(urllib.request.urlopen(req))["content"][0]["text"]
arr = json.loads(re.search(r"\[.*\]", text, re.S).group(0))
arr = [q for q in arr if isinstance(q.get("t"), str) and q.get("c") in range(6)]
assert len(arr) >= 18, "hasil terlalu sedikit"
json.dump({"month": month, "quotes": arr}, open("quotes.json", "w"), ensure_ascii=False, indent=1)
print("OK", len(arr))
