"""app/ 의 index.html + style.css + graphs.js + app.js 를 HTML 한 장으로 묶는다.

JSXGraph·KaTeX 는 CDN 링크 그대로 둔다(인터넷 필요). 쇼츠 영상은 파일 안에 넣는다.
사용법: .venv/bin/python -I app/build.py && .venv/bin/python -I app/bundle.py
"""
import base64
import json
import pathlib
import re

app = pathlib.Path(__file__).resolve().parent
out = app / "dist" / "발견해설.html"


def read(name):
    return (app / name).read_text(encoding="utf-8")


def script(name):
    return "<script>\n" + read(name).replace("</script", "<\\/script") + "\n</script>"


html = read("index.html")
html = html.replace('<link rel="stylesheet" href="style.css">', "<style>\n" + read("style.css") + "\n</style>")
shorts = {}
for name in sorted(set(re.findall(r'"short": "([^"]+)"', read("graphs.js")))):
    if not (app / "videos" / name).exists():
        continue
    data = (app / "videos" / name).read_bytes()
    shorts[name] = "data:video/mp4;base64," + base64.b64encode(data).decode()
html = html.replace('<script src="graphs.js"></script>',
                    script("graphs.js") + "\n<script>window.SHORTS = " + json.dumps(shorts) + ";</script>")
html = html.replace('<script src="app.js"></script>', script("app.js"))
assert 'href="style.css"' not in html and 'src="app.js"' not in html and 'src="graphs.js"' not in html

out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"-> {out.relative_to(app.parent)} ({len(html.encode()) // 1024} KB)")
