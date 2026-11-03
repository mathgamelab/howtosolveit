# 발견 그래프(discovery graph) 초안 스키마 v0

문제 하나에 대해 앱이 들고 있는 데이터. 종합법 풀이(정방향)가 아니라
**분석법(구하는 것에서 거꾸로 묻기)** 의 질문 트리와, 각 질문에 답하기 위해
학생이 캔버스에서 해야 하는 **발견 행위**를 적는다.

원칙
- 그래프를 "딸깍"으로 보여주지 않는다. 함수가 처음 등장할 때는 반드시
  `predict` 단계(개형 예측·스케치)가 먼저 오고, 예측이 끝난 뒤에야 실제 곡선이 열린다.
- 체크포인트는 "학생이 캔버스에서 어떤 상태를 만들었는가"로 판정한다.
- 모든 수치(접점, 경계값, 답)는 SymPy로 검산한 값만 쓴다.

```jsonc
{
  "id": "2026_수능_공통_14",
  "source": { "exam": "2026_수능", "number": 14, "score": 4, "answer": "④" },
  "statement": "문제 원문 (LaTeX)",

  // 1단계: 이해 — 주어진 것 / 구하는 것 / 조건
  "understand": {
    "given":   ["f(x) = ...", "조건 (가) ..."],
    "unknown": "k의 값의 범위",
    "condition": "교점이 정확히 3개"
  },

  // 2단계: 계획 = 분석법 질문 트리 (루트가 '구하는 것')
  "analysis": [
    {
      "id": "q0",
      "question": "k의 범위를 알려면 무엇을 알아야 하나?",
      "needs": ["q1"],
      "heuristic": "work-backward"          // polya: 거꾸로 풀기
    },
    {
      "id": "q1",
      "question": "교점 개수는 k에 따라 어떻게 변하나?",
      "needs": ["q2"],
      "heuristic": "draw-figure | vary-parameter | special-case | auxiliary-element",
      "discover": {                          // 이 질문은 캔버스에서 발견으로 답한다
        "scene": "s1",
        "predict": {                         // 딸깍 방지: 먼저 예측
          "prompt": "f(x)의 개형을 손으로 그려 보세요 (극값 개수, 증감).",
          "accept": { "extrema_count": 2, "end_behavior": "+-" }
        },
        "action": "slider k를 움직이며 y=k와 곡선의 교점 개수를 세어 보세요",
        "checkpoint": {                      // 발견했다고 인정하는 캔버스 상태
          "type": "tangent-reached",
          "object": "line_k", "target": "curve_f",
          "tolerance": 0.05
        },
        "noticing": "접할 때 교점 개수가 바뀐다"
      }
    },
    { "id": "q2", "question": "접할 때 k는 얼마인가?", "needs": [],
      "heuristic": "compute", "verified": { "k": ["-1", "3"] } }
  ],

  // 3단계: 실행 = 종합법 (기본 접힘, 발견 뒤에만 열림)
  "synthesis": [
    "f'(x)=0 에서 x=..., 극값은 ...",
    "따라서 -1 < k < 3"
  ],

  // 캔버스 장면 DSL — JSXGraph / Manim 양쪽에서 렌더
  "scenes": {
    "s1": {
      "view": [-4, 6, 6, -4],               // xmin, ymax, xmax, ymin
      "objects": [
        { "id": "curve_f", "type": "function", "expr": "x^3-3x+1",
          "reveal": "after-predict" },
        { "id": "k", "type": "slider", "range": [-5, 5], "init": 0 },
        { "id": "line_k", "type": "function", "expr": "k" },
        { "id": "pts", "type": "intersections", "of": ["curve_f", "line_k"], "count-label": true }
      ]
    }
  },

  // 검산 기록
  "verification": { "tool": "sympy", "claims": [ { "claim": "극댓값 3", "ok": true } ] }
}
```

객체 타입(1차 범위): `function`, `parametric`, `point-on-curve`, `tangent-at`,
`slider`, `intersections`, `area-between`, `polygon`, `segment`, `label`.

체크포인트 타입(1차 범위): `tangent-reached`, `count-equals`, `point-in-region`,
`slider-in-range`, `sketch-matches`(predict 전용).
