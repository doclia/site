"""Serveur local qui imite Vercel (cleanUrls, 404, en-têtes et CSP de vercel.json). Usage : python3 -I controles/serve.py <racine_du_site> 8787"""
import http.server, json, pathlib, re, sys
ROOT = pathlib.Path(sys.argv[1]); PORT = int(sys.argv[2])
CFG = json.loads((ROOT / "vercel.json").read_text())
def headers_for(path, host):
    out = {}
    for rule in CFG.get("headers", []):
        rx = "^" + rule["source"].replace("(.*)", ".*") + "$"
        if not re.match(rx, path): continue
        if any(m["type"] == "host" and m["value"] == host for m in rule.get("missing", [])): continue
        for h in rule["headers"]: out[h["key"]] = h["value"]
    return out
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def log_message(s, *a): pass
    def resolve(s):
        p = s.path.split("?")[0]
        if p == "/": return p, ROOT / "index.html", 200
        f = ROOT / p.lstrip("/")
        if f.is_file() and not p.endswith(".html"): return p, f, 200
        if (ROOT / (p.lstrip("/") + ".html")).is_file(): return p, ROOT / (p.lstrip("/") + ".html"), 200
        return p, ROOT / "404.html", 404
    def do_GET(s):
        if s.path.startswith("/_vercel/insights/"):
            # Simulation locale du script de Vercel Web Analytics (vide) : seul Vercel le sert réellement
            s.send_response(200); s.send_header("Content-Type","text/javascript"); s.send_header("Content-Length","0")
            for k, v in headers_for(s.path, sys.argv[3] if len(sys.argv)>3 else "localhost").items(): s.send_header(k, v)
            s.end_headers(); return
        p, f, code = s.resolve()
        body = f.read_bytes()
        ctype = {".html":"text/html; charset=utf-8",".css":"text/css",".svg":"image/svg+xml",".png":"image/png",".woff2":"font/woff2",".js":"text/javascript",".webm":"video/webm",".mp4":"video/mp4",".avif":"image/avif",".webp":"image/webp",".jpg":"image/jpeg"}.get(f.suffix,"application/octet-stream")
        s.send_response(code); s.send_header("Content-Type", ctype); s.send_header("Content-Length", str(len(body)))
        for k, v in headers_for(p, sys.argv[3] if len(sys.argv)>3 else s.headers.get("Host","").split(":")[0]).items(): s.send_header(k, v)
        s.end_headers(); s.wfile.write(body)
    do_HEAD = do_GET
    def do_POST(s):
        s.send_response(405); s.end_headers()
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
