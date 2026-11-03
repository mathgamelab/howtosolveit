"""data/graphs/v1/*.json 을 앱이 file:// 에서도 읽을 수 있는 JS 파일로 묶는다.

사용법: .venv/bin/python -I app/build.py
"""
import json
import pathlib
import shutil

root = pathlib.Path(__file__).resolve().parent.parent
src = root / "data" / "graphs" / "v1"
out = root / "app" / "graphs.js"

graphs = {}
for f in sorted(src.glob("*.json")):
    g = json.loads(f.read_text(encoding="utf-8"))
    graphs[g["id"]] = g

out.write_text(
    "// 자동 생성 파일 — app/build.py 로 다시 만든다. 직접 고치지 말 것.\n"
    "window.GRAPHS = " + json.dumps(graphs, ensure_ascii=False, indent=1) + ";\n",
    encoding="utf-8",
)
print(f"{len(graphs)} graph(s) -> {out.relative_to(root)}")

# 문항에 연결된 쇼츠 영상을 앱 폴더로 복사 (풀이를 마친 뒤 보여 준다)
videos = root / "app" / "videos"
videos.mkdir(exist_ok=True)
for g in graphs.values():
    if g.get("short"):
        if not (root / "shorts" / "out" / g["short"]).exists():
            print(f"(아직 없음) shorts/out/{g['short']}")
            continue
        shutil.copy2(root / "shorts" / "out" / g["short"], videos / g["short"])
        print(f"short -> app/videos/{g['short']}")
