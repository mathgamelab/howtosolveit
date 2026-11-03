# 발견 그래프 스키마 v1

> v0(`discovery-graph-schema.md`)로 7문항 드라이런을 해 보고 나온 문제점(`pilot-findings.md`)과,
> 선생님 블로그의 "분석법적 해설" 문체를 반영한 개정판이다.
> 예시 파일: `data/graphs/v1/2025_6월모평_7.json` / 렌더러: `app/`

## 0. 설계 원칙 (v1에서 바뀐 것 위주)

1. **발견이 먼저, 계산은 나중.** 학생이 밟는 길(`path`)은 *예측 → 조작 → 알아차림 → 계산* 순서를 기본으로 한다.
2. **딸깍 금지는 곡선만의 문제가 아니다.** 파일럿에서 누설 경로가 다섯 가지 나왔다
   (곡선 / 슬라이더 눈금 / 객체 내부 식 / predict 정답 키 / noticing 완성 문장).
   v1은 이 다섯 가지를 모두 **`reveal` 하나의 문법**으로 통제한다.
3. **블로그 문체를 구조로 옮긴다.**
   - 조건을 하나씩 "뜯어보고" → "(가)의 결론은 …" 으로 요약한다 → `understand.conditions[].digest`
   - 아직 못 쓰는 조건은 "일단 미뤄 둔다" → `deferred: true` 이고, 나중에 회수하는 단계를 `recall`로 둔다.
   - 구하는 값의 형태에서 힌트를 읽는다(답에 π²가 곱해져 있으니…) → `understand.unknown_hint`
   - "먼저 손으로 해 보고 지오지브라로 확인" → `predict` → `explore`
4. **분석법 트리와 학생의 길을 분리한다.** v0은 `needs` 트리 하나로 둘 다 표현하려다 순서가 꼬였다.
   - `analysis`: 구하는 것에서 거꾸로 묻는 **질문 트리** (화면 왼쪽에 "지금 어디쯤인가" 지도로 보여 줌)
   - `path`: 학생이 실제로 밟는 **단계의 순서** (각 단계가 트리의 어느 질문에 답하는지 `answers`로 가리킴)
5. **모든 수치는 검산된 값만 쓴다.** `verified` 블록의 값은 `verify_*.py`(SymPy)가 자동으로 모아 검사한다.

## 1. 최상위 구조

```jsonc
{
  "schema": "discovery-graph/v1",
  "id": "2025_6월모평_공통_7",
  "source": { "exam": "2025_6월모평", "number": 7, "section": "공통", "score": 3,
              "answer": "④", "unit": "수학II-미분", "choices": ["13","16","19","22","25"] },
  "statement": "LaTeX가 섞인 문제 원문",
  "polya": "understand | plan | carry-out | look-back",   // 각 단계 묶음의 라벨 (아래 path에서 사용)
  "understand": { ... },   // 2절
  "analysis":   [ ... ],   // 3절  분석법 질문 트리
  "path":       [ ... ],   // 4절  학생이 밟는 단계
  "scenes":     { ... },   // 5절  캔버스 장면
  "synthesis":  [ ... ],   // 종합법 풀이 (발견 뒤에만 열림, 기본 접힘)
  "verified":   { ... },   // 6절  SymPy가 검사하는 수치
  "leak_guard": { ... }    // 7절  누설 방지 빌드 검사 설정
}
```

## 2. understand — 이해 단계

```jsonc
"understand": {
  "unknown": "조건을 만족시키는 모든 실수 k의 값의 합",
  "unknown_hint": "'합'을 묻는다 → 그런 k가 유한 개(아마 두세 개)뿐이라는 뜻",
  "data": ["방정식 x^3-3x^2-9x+k=0"],
  "conditions": [
    { "id": "c1", "text": "서로 다른 실근의 개수가 2",
      "digest": "그래프가 x축과 '서로 다른 두 점'에서 만난다 (중근은 한 번만 센다)",
      "deferred": false }
  ]
}
```
- `digest`는 학생이 **먼저 자기 말로 쓰고** 나서 모범 문장을 보는 칸이다 (noticing과 같은 규칙).
- `deferred: true`인 조건은 이해 단계에서 "아직 쓸 수 없음" 표시만 하고, `path`의 `recall` 단계에서 다시 꺼낸다.

## 3. analysis — 분석법 질문 트리

```jsonc
"analysis": [
  { "id": "q0", "ask": "모든 k의 값의 합을 알려면?", "needs": ["q1"], "heuristic": "work-backward" },
  { "id": "q1", "ask": "실근이 2개가 되는 k는 어떤 값들인가?", "needs": ["q2","q3"], "heuristic": "vary-parameter" },
  { "id": "q2", "ask": "k를 바꾸면 그래프는 어떻게 변하나?", "needs": [], "heuristic": "draw-figure" },
  { "id": "q3", "ask": "봉우리·골짜기의 높이는?", "needs": [], "heuristic": "compute" }
]
```
- `heuristic` 어휘(폴리아): `work-backward`, `draw-figure`, `vary-parameter`, `special-case`,
  `auxiliary-element`, `look-at-unknown`, `related-problem`, `decompose`, `restate`, `compute`.
- 트리는 **보여 주기용 지도**다. 순서는 `path`가 정한다.

## 4. path — 학생이 밟는 단계

각 단계는 `kind` 하나와 공통 필드를 가진다.

| 공통 필드 | 뜻 |
|---|---|
| `id` | 단계 id (`reveal` 조건이 참조) |
| `polya` | `understand` / `plan` / `carry-out` / `look-back` |
| `answers` | 이 단계가 답하는 분석 트리 질문 id |
| `role` | `decisive`(결정적 발견) / `motivation`(동기 부여, 생략 가능) / `warm-up`(보기 함수) / `routine` |
| `scene` | 사용하는 장면 id (없으면 텍스트만) |
| `prompt` | 학생에게 보여 줄 질문·지시 |
| `hints` | 단계별 힌트 배열 `[{ "after": "attempts:2" | "seconds:90", "text": "…" }]` — 힌트도 순서대로만 열린다 |

### 4.1 `kind` 목록

| kind | 하는 일 | 통과 조건 |
|---|---|---|
| `ask` | 거꾸로 묻는 질문을 제시 (학생은 생각만, "다음"으로 진행) | 없음 |
| `digest` | 조건 하나를 뜯어보고 자기 말로 요약 → 모범 요약 공개 | 학생 입력 제출 |
| `predict` | 보기 전에 예측 (개형 스케치, 개수 순서, 부호표, 값) | `predict.kind`별 판정 (4.2) |
| `explore` | 캔버스 조작 | `checkpoint` (4.3) |
| `notice` | 방금 본 것을 학생이 한 줄로 쓴다 → 모범 noticing 공개 | 학생 입력 제출 |
| `compute` | 계산 (답을 입력) | `input.accept`와 일치 |
| `recall` | 미뤄 둔 조건(`deferred`)을 다시 꺼내 적용 | 하위 단계로 |
| `synthesis` | 종합법 풀이 공개 | — |

**규칙:** `explore` 바로 뒤에는 반드시 `notice`가 온다. 체크포인트를 통과하자마자 결론 문장이 뜨는 "발견 뒤 딸깍"을 막기 위해서다.

### 4.2 predict.kind (판정 어휘 고정)

| kind | 학생 입력 | accept 스키마 |
|---|---|---|
| `shape` | 캔버스에 손으로 곡선 스케치 | `{ "turning_points": 2, "ends": ["down","up"], "through": [[0,0]], "slope_sign_at": {"0": "-"} }` — 스케치에서 극값 수·양 끝 방향을 자동 추출해 비교 |
| `sequence` | 수열 입력 (예: 교점 개수가 바뀌는 순서) | `{ "values": [1,2,3,2,1] }` |
| `count` | 정수 하나 | `{ "value": 2 }` |
| `choice` | 보기 중 선택 | `{ "options": [...], "correct": "shift-up" }` |
| `sign-table` | 구간별 부호 | `{ "breaks": [-1,3], "signs": ["+","-","+"] }` |
| `value` | 수치 | `{ "value": "5", "tol": 0 }` |

공통: `grade: "hard" | "soft"`.
- `hard`: 맞아야 다음으로 간다. 틀리면 `on_fail`의 힌트를 연다. `max_attempts`를 넘기면 **정답을 보여 주지 않고** 비교 화면으로 넘어간다.
- `soft`: 기록만 한다. 조작이 끝난 뒤 "예측 vs 실제" 비교로 다시 보여 준다 (학습 순간).

예측이 끝나기 전에는 `accept` 값이 클라이언트에 노출되지 않아야 한다. 프로토타입은 단일 파일이라 예외로 둔다 (7절 참고).

### 4.3 checkpoint (조합 가능)

```jsonc
"checkpoint": { "all": [
  { "type": "count-equals", "of": "roots", "value": 2, "times": 2 },  // 서로 다른 순간 2번
  { "type": "visited", "slider": "k", "values": [-5, 27] }              // 두 순간 모두 거침
]}
```
| type | 뜻 |
|---|---|
| `count-equals` | 교점·부호 변화 등의 개수가 값과 같음. `times`: 서로 다른 슬라이더 값에서 몇 번 |
| `tangent-reached` | 두 객체가 접함. `metric: "vertical-gap"`, `tol` |
| `slider-in-range` | 슬라이더 값 범위 (구간 여러 개 허용) |
| `visited` | 슬라이더가 특정 값들을 모두 지나감 |
| `point-in-region` | 점이 영역 안 |
| `sweep-invariant` | 슬라이더 전 구간을 훑는 동안 술어가 항상 참 (∀) |
| `set-equals` | 매개변수 축 위의 집합이 목표와 같음 (`param-set` 객체와 짝) |
| `region-compose` | 학생이 고른 영역들의 부호 합이 목표 넓이와 같음 |
| `expr-input` | 대수 변형 관문 (식 입력, CAS로 동치 판정) |

조합은 `all: [...]`, `any: [...]`로 한다. 연속 슬라이더에서 접하는 순간은 측도가 0이라 직접 맞추기 어렵다. 그래서 `slider.step`이 특수값을 격자 위에 두도록 하거나 `snap: "tangent"`를 쓴다. 이 조건은 빌드 시 검사한다.

## 5. scenes — 장면과 객체

```jsonc
"s1": {
  "view": { "x": [-4, 6.5], "y": [-45, 40], "aspect": "free" },
  "axes": { "x": { "name": "x", "ticks": 1 }, "y": { "name": "y", "ticks": 10, "labels": false } },
  "objects": [ ... ]
}
```

### 5.1 공통 객체 필드
| 필드 | 뜻 |
|---|---|
| `id`, `type`, `label` | |
| `reveal` | **언제 보이는가.** `"always"` / `"after:<path-step-id>"` / `{"all":[…]}` — 곡선·라벨·눈금·힌트 모두 이 하나로 통제 |
| `expr` | 렌더 전용 식. **학생 화면에는 절대 출력하지 않는다.** 학생에게 보이는 것은 `label`뿐 |
| `role` | `problem` / `warm-up`(보기 함수 배지 강제) / `guide`(보조선) |

### 5.2 객체 타입
| type | 주요 필드 |
|---|---|
| `slider` | `range`, `step`, `init`, `readout: "hidden" \| "coarse" \| "numeric"`, `readout_reveal` (눈금이 열리는 시점) |
| `function` | `expr`, `domain`(슬라이더 참조 가능 → 누적 곡선), `pieces`(조각함수 `[{expr, domain, closed}]`) |
| `parametric` | `x`, `y`, `t_range` |
| `point` | 고정점 `[x,y]` |
| `point-on-curve` | `curve`, `x` 또는 `binds: "<slider>"` (끌면 슬라이더 값도 바뀌는 양방향 바인딩) |
| `vline` / `hline` | 수직선·수평선 (`x`/`y`에 슬라이더 참조 가능) |
| `tangent-at` | `curve`, `at` |
| `intersections` | `of: [a, b]` (`@x-axis`, `@y-axis` 내장 참조), `distinct: true`, `merge_tol`, `count_label` |
| `sign-changes` | `of: [a, b]` — 교점 중에서 **가로지르는 점만** 센다 (교점과 가로지름의 구분) |
| `area-between` | `of`, `from`, `to`, `signed: true`, `mode: "by-sign"` (두 색) |
| `param-set` | `axis`(슬라이더 id), `predicate`(SymPy가 평가할 수 있는 식), `mode: live \| accumulate`, `target` |
| `hole-at` | 유리함수의 구멍 |
| `compare` | 두 양의 대소만 보여 주는 저울 (값은 숨김) |
| `label` | 텍스트 |

장면은 `extends: "s1"`로 다른 장면을 이어받을 수 있다. 이어받으면 슬라이더 상태도 승계된다.
같은 곡선을 이미 예측했다면 `predicted_in: "<step-id>"`로 표시하고, 그 곡선은 다시 예측시키지 않는다.

## 6. verified — 검산

```jsonc
"verified": {
  "f": "x**3-3*x**2-9*x",
  "critical_x": ["-1", "3"], "local_max": "5", "local_min": "-27",
  "k_values": ["-5", "27"], "answer_value": "22", "answer_choice": "④"
}
```
- `compute` 단계의 `input.accept`는 반드시 `verified`의 키를 참조한다 (`"$verified.k_values"`). 손으로 쓴 숫자는 쓰지 않는다.
- `verify_*.py`는 `verified`를 읽어 SymPy로 재계산한다. JSON 안의 모든 `$verified.*` 참조가 실제로 있는 키인지도 함께 검사한다.

## 7. leak_guard — 누설 방지 빌드 검사

```jsonc
"leak_guard": { "choice_gap": 3, "max_tick_resolution": "auto" }
```
빌드(또는 저작 도구 저장) 시 자동으로 검사하는 항목:
1. **곡선 공개 순서:** `function` 객체의 `reveal`이 그 곡선을 예측하는 `predict` 단계보다 앞서 열리지 않는가.
2. **눈금 누설:** 슬라이더가 `numeric`으로 열리는 시점이 그 값을 구하는 `compute` 단계보다 앞서지 않는가. 그리고 눈금 해상도가 선택지 간격(`choice_gap`)보다 거친가.
3. **식 누설:** `label`·`prompt`·`hints`에 `verified` 값이나 객체의 `expr`이 그대로 들어 있지 않은가.
4. **예측 정답 키 누설:** `hard` predict의 `accept`는 서버 판정용이다. 클라이언트로 보내지 않는다. 단일 파일 프로토타입은 예외.
5. **noticing 누설:** 모든 `explore` 다음에 `notice`가 오는가.

## 8. v0 → v1 대응표

| v0 | v1 |
|---|---|
| `analysis[].discover` | `path`의 `predict` → `explore` → `notice` 세 단계로 분리 |
| `reveal: "after-predict"` | `reveal: "after:<step-id>"` + 조합 |
| `checkpoint` 1개 | `checkpoint: {all/any: [...]}` |
| `predict.accept` 자유 키 | `predict.kind`별 고정 accept 스키마 |
| `noticing` (즉시 공개) | `notice` 단계 (학생이 먼저 쓴다) |
| `verification.claims` 손 작성 | `verified` 값 → 스크립트가 자동 수확 |
| 없음 | `understand.conditions[].digest/deferred`, `recall`, `leak_guard`, `role`, `hints[]` 단계 공개 |
