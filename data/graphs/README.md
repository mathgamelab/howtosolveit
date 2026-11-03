# 발견 그래프 파일럿

각 파일럿 문항마다
- `<exam>_<n>.json` — docs/discovery-graph-schema.md 형식의 발견 그래프
- `verify_<exam>_<n>.py` — SymPy 검산 스크립트 (`.venv/bin/python -I` 로 실행)
- `report_<exam>_<n>.md` — 드라이런 평가 (발견이 진짜인가, 딸깍 누수, 검산 결과)
