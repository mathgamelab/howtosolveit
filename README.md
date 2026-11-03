# 발견 해설 (howtosolveit)

폴리아의 **분석법**으로, 학생이 직접 발견하며 푸는 인터랙티브 수학 해설이에요.

해설지의 풀이(종합법)는 조건에서 답까지 한 줄로 내려가지만, 그 풀이를 **어떻게 떠올렸는지**는 숨겨져 있어요.
이 프로젝트는 종이 위에서 손으로 그리며 하던 발견을, 예측하고 조작하며 거치게 만들어요.

- **메인 페이지:** [`index.html`](index.html)
- **해설 앱 (HTML 한 장):** [`app/dist/발견해설.html`](app/dist/발견해설.html) — 내려받아 더블클릭하면 열려요 (그래프·수식 라이브러리 때문에 인터넷은 필요해요).

## 원칙

1. **폴리아 4단계:** 이해 → 계획(분석법·발견) → 실행(종합법). 반성 단계는 다음 버전에서 다뤄요.
2. **‘딸깍’ 금지:** 그래프는 학생이 개형을 손으로 그려야 열려요. 슬라이더 눈금은 값을 계산한 뒤에야 열려요.
3. **예측 → 조작 → 본 것 쓰기:** 조작 전에 결과를 예측하고, 조작한 뒤에는 알아차린 것을 내 말로 쓰고 나서 모범 문장을 봐요.

## 문항

| 문항 | 결정적 발견 | 쇼츠 |
|---|---|---|
| 2025학년도 6월 모평 공통 7번 (3점) | 실근 2개 ⇔ 봉우리·골짜기가 x축에 닿을 때 | ✓ |
| 2026학년도 수능 공통 9번 (4점) | 접함 = 극값, 곡선은 늘 (0, 4)를 지나서 닿는 건 봉우리뿐 | |
| 2025학년도 10월 고1 학평 30번 (4점) | h = 위에 있는 것, 범위의 양 끝이 숨은 두 식 | ✓ |

## 구조

```
app/                 해설 앱 (JSXGraph + KaTeX, 바닐라 JS)
  build.py           data/graphs/v1/*.json → app/graphs.js, 쇼츠 영상 복사
  bundle.py          앱 전체를 HTML 한 장(app/dist/발견해설.html)으로 묶기
data/graphs/v1/      문항별 발견 그래프(JSON)와 SymPy 검사기 verify_v1.py
data/problems/       평가원 기출 수학II·미적분 133문항 목록과 평가
docs/                스키마 v1, 문항 선별, 파일럿 결과
shorts/              Manim 쇼츠 코드와 완성 영상(shorts/out/)
```

## 다시 만들기

```bash
python3 -m venv .venv && .venv/bin/pip install manim sympy pymupdf
.venv/bin/python -I data/graphs/v1/verify_v1.py data/graphs/v1/2026_수능_9.json   # 수학·누설 검사
.venv/bin/python -I app/build.py && .venv/bin/python -I app/bundle.py            # 앱 묶기
cd shorts && ../.venv/bin/manim -r 1080,1920 --fps 30 s03_2025_10_g1_30.py Short03  # 쇼츠 (LaTeX 필요)
```

## 저작권

문항의 저작권은 한국교육과정평가원과 출제 교육청에 있어요. 이 저장소에는 시험지 원본, 정답표, EBS 해설지를 넣지 않았어요 (`data/raw/`, `data/pages/`는 `.gitignore`).
