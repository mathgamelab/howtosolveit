# 파일럿 드라이런 결과 (7문항) — 2026-10-28

대상: `docs/selection.md`의 파일럿 7문항. 문항마다 발견 그래프 JSON·SymPy 검산 스크립트·평가 보고서가
`data/graphs/`에 있다.

## 결과 요약

| 문항 | 패턴 | 정답 | 검산 | 결정적 발견 (학생이 하는 조작) |
|---|---|---|---|---|
| 2025 6월 7 | 수평선 쓸기 | ④ 일치 | 24/24 | k 슬라이더를 밀며 x절편 개수 1→2→3→2→1 — "2개"는 봉우리/골이 축에 닿는 두 순간뿐 |
| 2026 수능 9 | 수평선+접함 | ④ 일치 | 23/23 | a를 줄이며 y=5와 교점 3→2→1; 골은 y=4 아래에 머물러 봉우리만 닿을 수 있음 |
| 2026 9월 13 | 직선 회전 | ④ 일치 | 21/21 | (−2,0) 중심으로 직선 회전, 접하는 k=−2, 6 중 접점이 x=0에 오는 쪽만 분자와 상쇄 |
| 2026 수능 15 | 가로지르기=극값 | ④ 일치 | 39/39 | a를 밀어 왼쪽 반직선이 포물선에 **접하는** 순간; 접함≠가로지름이라 a=4 포함 |
| 2026 6월 13 | 넓이 상쇄 | ④ 일치 | 22/22 | x=k를 끌며 누적 적분 S(t)가 0으로 돌아오는 순간 = A+C=B |
| 2027 6월 15 | 창 밀기 | ④ 일치 | 21/21 | 근 r,s를 끌어 "조건이 성립하는 p의 집합"이 (0,3)이 되게 — 이중근은 x=0에 있어야 함 |
| 2026 수능 28 | 점 끌기(미적) | ⑤ 일치 | 30/30 | P를 끌어 접선 기울기 1인 곳에서 t=s → t/s=기울기 ⇒ t=s·f'(s) |

- 7문항 모두 정답표와 일치, 수치 주장 180개 전부 SymPy 통과.
- 검산이 실제 오류를 잡은 사례 2건: 2027 6월 15 (초안의 p-집합 오류), 2026 수능 15 (h(x) 조각 상수 3개 오류).
  → "LLM 생성 + CAS 검산" 층은 필수라는 것이 확인됨.
- 7문항 모두 **분석법 트리의 결정적 노드가 캔버스 조작**으로 끝났고, 계산은 마지막 1~2노드뿐.

## 스키마 v0에서 드러난 문제 (7개 보고서 종합, 빈도순)

### 1. 누설(딸깍) 경로가 그래프 말고도 많다 — 7/7
- **슬라이더 눈금·수치 표시**: 특별한 순간에 k값을 읽으면 계산이 사라짐 (6월 7, 6월 13은 선택지 간격 1/12).
  → `slider.readout: hidden | coarse | hidden-until:<q>`; 빌드 시 "눈금 해상도 > 선택지 간격" 자동 검사.
- **객체 내부 식 노출**: `point-on-curve x: "-3*a"` 자체가 답 (수능 9). → expr은 렌더 전용, 학생에겐 라벨만.
- **predict.accept가 정답 키**: 틀리면 다시 묻기만 하는 구조는 반복 시도로 답이 샘 (6월 15, 수능 15).
  → `on-fail: hint-id` + `max-attempts`, `grade: soft|hard` (soft는 기록만 하고 나중에 대조).
- **noticing이 체크포인트 통과 즉시 완성 문장으로 뜸** = "발견 뒤 딸깍". → 학생이 한 줄 먼저 쓰고 모범 noticing을 본다.
- **공식 딸깍**: 접선 문제에서 진짜 누설은 그래프가 아니라 접선 방정식을 바로 쓰는 힌트 (수능 28). 힌트에도 reveal 단계 필요.

### 2. `reveal`과 predict 재사용 — 6/7
- `after-predict`만으로 부족: `always | after-predict:<q> | after-checkpoint:<id> | after-synthesis`.
- 같은 곡선이 장면 여러 개에 나올 때 예측을 반복시키지 말 것: `predicted-in: "q3"`.
- 장면 간 슬라이더 상태 승계: `scene.extends`.

### 3. 체크포인트 표현력 — 6/7
- 접함은 측도 0인 상태라 연속 슬라이더로 못 맞춤 → `slider.step` 필수, `snap-to: tangent`, tolerance 단위 명시.
- AND/여러 순간: `checkpoints: [...]`, `all/any`, 다중 구간 `slider-in-range`.
- 새 타입 필요: `sweep-invariant`(∀ 슬라이더값), `set-equals`(매개변수 축 위 집합), `region-compose`(영역 조합),
  `expr-input`(대수 변형 관문), `value-matches`.

### 4. 객체 타입 부족 — 5/7
- 조각함수(`domain`, `group`), 고정 `point`, `vline`, 좌표축 참조(`@x-axis`), 유리함수 `hole-at`.
- `intersections`에 `distinct`/`merge-tolerance`, 그리고 **교점 vs 가로지름 구분** (`sign-changes`) — 수능 15의 핵심 개념이 v0로는 표현 불가.
- `area-between.signed`, `mode: by-sign`, 슬라이더에 묶인 `function.domain`(누적 곡선), `integral-of` 파생 타입.
- **매개변수 축 객체 `param-set`** (조건이 성립하는 p의 집합을 축 위에 불 켜기) — 2027 6월 15는 발견이 그래프가 아니라 매개변수 축에서 일어남.
- 다중 패널, 축 이름 바꾸기(역함수 장면), `view` 종횡비·눈금.

### 5. predict 어휘가 즉흥적 — 5/7
- accept 키가 문항마다 다름 (`extrema_count`, `end_behavior`, `sign_pattern`, `count_sequence`, …).
  → `predict.kind` 열거: `shape`(개형: 극값 수·증감·끝 거동), `count-table`, `sign-table`, `region`, `value`
  각각 고정 accept 스키마 + `sketch-matches` 허용오차 정의 (x? 높이?).

### 6. 트리 구조 — 4/7
- `needs`만으로 "발견 뒤 계산" 순서를 못 적음 → 노드에 `phase: discover|compute|restate`.
- 동기 부여용 약한 발견 노드는 `role: motivation|decisive|warm-up` 표시 (시간 압박 시 결정적 장면만 남기기).
- 연습 함수(문제의 f가 아닌 g)를 쓰는 워밍업 장면엔 "보기 함수" 배지 강제.
- verify 스크립트가 JSON의 `verified` 값을 자동 수확하게 (지금은 손으로 중복 작성).

## 다음 단계 제안
1. 위 1~6을 반영한 **스키마 v1** 작성 (특히 reveal/readout 누설 정책, predict.kind, checkpoint 조합).
2. 파일럿 중 가장 단순한 **2025 6월 7번**을 JSXGraph로 실제 렌더해 보기 — 발견 그래프 JSON → 캔버스 변환기의 첫 버전.
3. 그다음 2026 수능 15번(조각함수·가로지름)과 2027 6월 15번(param-set)으로 v1 객체 타입 검증.
