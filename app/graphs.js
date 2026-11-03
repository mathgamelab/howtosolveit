// 자동 생성 파일 — app/build.py 로 다시 만든다. 직접 고치지 말 것.
window.GRAPHS = {
 "2025_10월학평_고1_30": {
  "schema": "discovery-graph/v1",
  "id": "2025_10월학평_고1_30",
  "source": {
   "exam": "2025_10월학평_고1",
   "examLabel": "2025학년도 10월 고1 전국연합학력평가",
   "number": 30,
   "section": "",
   "score": 4,
   "answer": "16",
   "unit": "공통수학1-이차함수"
  },
  "statement": "두 상수 $p\\,(p>0)$, $q$에 대하여 이차함수 $f(x)=\\frac12(x-p)^2+q$가 있다. 함수 $f(x)$와 양수 $m$에 대하여 함수 $g(x)$를 $g(x)=-f(x-m)$이라 할 때, 방정식 $f(x)=g(x)$가 서로 다른 두 실근 $\\alpha,\\beta\\,(\\alpha<\\beta)$를 갖는다. 함수 $h(x)$를\n$$h(x)=\\begin{cases} f(x) & (x\\le\\alpha \\text{ 또는 } x\\ge\\beta) \\\\ g(x) & (\\alpha<x<\\beta)\\end{cases}$$\n라 할 때, 함수 $h(x)$는 다음 조건을 만족시킨다.\n\n<div class=\"box\">$x$에 대한 방정식 $h(x)=t$의 서로 다른 실근의 개수가 $2$ 이상이면서 서로 다른 모든 실근의 합이 $4p+2m$이 되도록 하는 모든 실수 $t$의 값의 범위는 $g(p)<t<5$이다.</div>\n$f(m)+g(m)=-4$일 때, $m\\times(p-q)$의 값을 구하시오. [4점]",
  "understand": {
   "unknown": "$m\\times(p-q)$ — 미지수 $p,q,m$ 세 개를 모두 정해야 한다",
   "unknown_hint": "구하는 값에 $m,p,q$가 다 들어 있어요. 미지수가 **셋**이니 식도 **셋** 필요해요. 그런데 눈에 보이는 등식은 $f(m)+g(m)=-4$ 하나뿐이에요. 그렇다면 상자 속 조건이 **식 두 개**를 숨기고 있을 거예요 — 범위 $g(p)<t<5$의 **양 끝**이 바로 그 두 개!",
   "data": [
    "$f(x)=\\frac12(x-p)^2+q$, $p>0$",
    "$g(x)=-f(x-m)$, $m>0$",
    "$f(m)+g(m)=-4$"
   ],
   "conditions": [
    {
     "id": "c1",
     "text": "$g(x)=-f(x-m)$",
     "digest": "$f(x-m)$은 $f$를 **오른쪽으로 $m$만큼** 옮긴 것, 앞의 $-$는 **$x$축에 대해 뒤집기**예요. 그러니 $g$는 꼭짓점이 $(p+m,\\,-q)$인 **위로 볼록(∩)** 포물선이에요.",
     "deferred": false
    },
    {
     "id": "c2",
     "text": "$h(x)$의 정의 ($\\alpha,\\beta$ 바깥은 $f$, 사이는 $g$)",
     "digest": "$h$는 두 그래프가 만나는 점 $\\alpha,\\beta$에서 **$f$와 $g$를 갈아타는** 함수예요. 바깥쪽은 $f$, 가운데는 $g$.",
     "deferred": false
    },
    {
     "id": "c3",
     "text": "$h(x)=t$의 실근이 2개 이상이고 합이 $4p+2m$인 $t$의 범위가 $g(p)<t<5$",
     "digest": "이 조건은 그림이 있어야 읽을 수 있어요. 지금은 '**범위의 양 끝 $g(p)$와 $5$가 그래프의 어떤 높이인가**'를 나중에 찾아야 한다는 것만 기억하고 **미뤄 둬요**.",
     "deferred": true
    }
   ]
  },
  "analysis": [
   {
    "id": "q0",
    "ask": "$m(p-q)$를 구하려면 무엇을 알아야 하나?",
    "needs": [
     "q1",
     "q4"
    ],
    "heuristic": "work-backward"
   },
   {
    "id": "q1",
    "ask": "상자 속 조건은 어떤 식 두 개를 숨기고 있나?",
    "needs": [
     "q2",
     "q3"
    ],
    "heuristic": "vary-parameter"
   },
   {
    "id": "q2",
    "ask": "$g$와 $h$의 그래프는 어떤 모양인가?",
    "needs": [],
    "heuristic": "draw-figure"
   },
   {
    "id": "q3",
    "ask": "실근의 합이 $4p+2m$이 되는 $t$는 언제인가? 그 범위의 양 끝은?",
    "needs": [],
    "heuristic": "vary-parameter"
   },
   {
    "id": "q4",
    "ask": "세 식을 연립하면 $p,q,m$은?",
    "needs": [],
    "heuristic": "compute"
   }
  ],
  "path": [
   {
    "id": "u_unknown",
    "kind": "ask",
    "polya": "understand",
    "answers": "q0",
    "prompt": "구하는 것은 $m\\times(p-q)$예요. 세어 보세요.",
    "input": {
     "fields": [
      {
       "label": "알아내야 할 미지수의 개수",
       "accept": "3"
      },
      {
       "label": "문제에 등식으로 주어진 조건의 개수",
       "accept": "1"
      }
     ]
    },
    "model": "미지수가 **셋**이면 식도 **셋** 필요한데, 등식은 $f(m)+g(m)=-4$ 하나뿐이에요. 그러니 상자 속 범위 $g(p)<t<5$의 **양 끝**이 나머지 두 식을 숨기고 있을 거예요. 상자는 그림을 그린 뒤에 읽어요.",
    "history": "<b>구하는 것</b> — 미지수 3개, 등식 1개 → 상자 범위의 양 끝이 나머지 두 식"
   },
   {
    "id": "p_g",
    "kind": "predict",
    "polya": "plan",
    "answers": "q2",
    "prompt": "그림부터 그려요. $p,q$는 아직 모르니 **일단 $p=2$, $q=-4$로** 두고 구조를 볼게요. $f$는 꼭짓점이 $(p,q)$인 ∪ 모양이에요. $g(x)=-f(x-m)$은 어떤 모양일까요?",
    "predict": {
     "kind": "choice",
     "grade": "soft",
     "options": [
      "꼭짓점 $(p+m,\\,-q)$인 ∩ 모양",
      "꼭짓점 $(p+m,\\,q)$인 ∪ 모양",
      "꼭짓점 $(p-m,\\,-q)$인 ∩ 모양",
      "꼭짓점 $(p-m,\\,q)$인 ∪ 모양"
     ],
     "correct": "꼭짓점 $(p+m,\\,-q)$인 ∩ 모양"
    },
    "explain": "$f(x-m)$은 오른쪽으로 $m$만큼 평행이동, 앞의 $-$는 $x$축에 대해 뒤집기예요."
   },
   {
    "id": "p_h",
    "kind": "predict",
    "polya": "plan",
    "answers": "q2",
    "scene": "s1",
    "prompt": "$f$(회색)와 $g$(주황)가 열렸어요. 이제 $y=h(x)$를 캔버스에 **손으로** 그려 보세요. $\\alpha,\\beta$ 바깥은 $f$, 사이는 $g$예요.",
    "predict": {
     "kind": "shape",
     "grade": "hard",
     "max_attempts": 2,
     "accept": {
      "turning_points": 3,
      "ends": [
       "up",
       "up"
      ]
     },
     "on_fail": [
      "왼쪽 끝과 오른쪽 끝은 모두 $f$예요. $f$는 양 끝에서 어디로 가나요?",
      "$\\alpha$에서 $g$로 갈아타면 올라갔다가 내려오고, $\\beta$에서 다시 $f$를 타고 올라가요. 방향이 바뀌는 곳이 몇 군데인가요?"
     ]
    }
   },
   {
    "id": "n_h",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "prompt": "진한 파란 선이 $h$예요. $h$를 한마디로 하면?",
    "input": {
     "fields": [
      {
       "label": "$h$는",
       "type": "select",
       "options": [
        "$f$와 $g$ 중 위에 있는 것",
        "$f$와 $g$ 중 아래에 있는 것",
        "$f$와 $g$의 평균"
       ],
       "accept": "$f$와 $g$ 중 위에 있는 것"
      }
     ]
    },
    "model": "$\\alpha,\\beta$ 사이에서는 $g$가 위, 바깥에서는 $f$가 위예요. 그래서 $h$는 **위에 있는 것만 이은** 그래프: 왼쪽 골짜기 → 가운데 봉우리 → 오른쪽 골짜기."
   },
   {
    "id": "p_count",
    "kind": "predict",
    "polya": "plan",
    "answers": "q3",
    "prompt": "수평선 $y=t$를 위에서 아래로 내리면, $h(x)=t$의 서로 다른 실근은 **최대 몇 개**일까요?",
    "predict": {
     "kind": "count",
     "grade": "soft",
     "accept": {
      "value": 4
     }
    }
   },
   {
    "id": "e_t",
    "kind": "explore",
    "polya": "plan",
    "answers": "q3",
    "scene": "s1",
    "role": "decisive",
    "prompt": "슬라이더 $t$로 수평선을 위아래로 움직여 보세요. 실근 개수와 함께 **합이 $4p+2m$인지**가 표시돼요. ✓가 뜨는 구간을 찾아 보세요.",
    "checkpoint": {
     "all": [
      {
       "type": "visited-range",
       "slider": "t",
       "range": [
        2.8,
        3.9
       ]
      },
      {
       "type": "visited-range",
       "slider": "t",
       "range": [
        -2,
        2.4
       ]
      },
      {
       "type": "visited-range",
       "slider": "t",
       "range": [
        4.2,
        7
       ]
      }
     ]
    },
    "hints": [
     {
      "after": "seconds:60",
      "text": "✓가 뜨는 구간의 **위 끝**과 **아래 끝**에서 수평선이 $h$의 어디를 지나는지 보세요."
     }
    ]
   },
   {
    "id": "n_t",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "role": "decisive",
    "prompt": "본 것을 확인해 봐요.",
    "input": {
     "fields": [
      {
       "label": "합이 $4p+2m$일 때 실근의 개수",
       "accept": "4"
      },
      {
       "label": "그런 $t$ 구간의 **위 끝**",
       "type": "select",
       "options": [
        "봉우리 높이 $-q$",
        "오른쪽 꺾인 점의 높이 $h(\\beta)$",
        "왼쪽 꺾인 점의 높이 $h(\\alpha)$"
       ],
       "accept": "봉우리 높이 $-q$"
      },
      {
       "label": "그런 $t$ 구간의 **아래 끝**",
       "type": "select",
       "options": [
        "봉우리 높이 $-q$",
        "오른쪽 꺾인 점의 높이 $h(\\beta)$",
        "왼쪽 꺾인 점의 높이 $h(\\alpha)$"
       ],
       "accept": "오른쪽 꺾인 점의 높이 $h(\\beta)$"
      }
     ]
    },
    "model": "바깥 두 근은 $f$의 축 $x=p$, 가운데 두 근은 $g$의 축 $x=p+m$에 대해 **대칭**이라 합이 $2p+2(p+m)=4p+2m$이에요. 그래서 범위는 $h(\\beta)<t<-q$."
   },
   {
    "id": "r_box",
    "kind": "recall",
    "polya": "plan",
    "condition": "c3",
    "answers": "q1",
    "prompt": "이제 상자를 읽을 차례예요. 찾은 범위 $h(\\beta)<t<-q$를 문제의 범위 $g(p)<t<5$와 맞대 보세요.",
    "input": {
     "fields": [
      {
       "label": "위 끝에서: $q=$",
       "accept": "$verified.q"
      },
      {
       "label": "아래 끝에서 나오는 식",
       "type": "select",
       "options": [
        "$g(\\beta)=g(p)$",
        "$g(\\alpha)=g(p)$",
        "$f(\\beta)=f(p)$"
       ],
       "accept": "$g(\\beta)=g(p)$"
      }
     ]
    },
    "model": "두 번째 식은 $h(\\beta)=g(p)$, 즉 $g(\\beta)=g(p)$예요. ($\\beta$에서 $f$와 $g$의 값이 같아요.)",
    "history": "<b>상자 조건</b> — $q=-5$, $g(\\beta)=g(p)$"
   },
   {
    "id": "p_beta",
    "kind": "predict",
    "polya": "plan",
    "answers": "q1",
    "prompt": "$g(\\beta)=g(p)$가 되려면 $\\beta$는 어디에 있어야 할까요? ($g$의 그래프는 $x=p+m$에 대해 대칭이에요.)",
    "predict": {
     "kind": "choice",
     "grade": "soft",
     "options": [
      "$\\beta=p$",
      "$\\beta=p+m$",
      "$\\beta=p+2m$",
      "$\\beta=2p+m$"
     ],
     "correct": "$\\beta=p+2m$"
    }
   },
   {
    "id": "e_beta",
    "kind": "explore",
    "polya": "plan",
    "answers": "q1",
    "scene": "s1",
    "prompt": "이제 $m$ 슬라이더가 열렸어요. $m$을 움직여 **꺾인 점 $\\beta$가 빨간 점선 위에 딱 올라가는** 순간을 찾아 보세요.",
    "checkpoint": {
     "type": "near",
     "expr": "0.5*(-m/2+Math.sqrt(8-m^2/4))^2-0.5*m^2",
     "tol": 0.04
    },
    "hints": [
     {
      "after": "seconds:60",
      "text": "$m$을 클릭한 뒤 ← → 키로 한 칸씩 움직여 보세요."
     }
    ]
   },
   {
    "id": "n_beta",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "prompt": "점선에 올라간 순간, 세로 점선 $x=p$, $x=p+m$, $x=\\beta$의 간격을 보세요.",
    "input": {
     "fields": [
      {
       "label": "$\\beta$와 $p$ 사이의 거리는 $m$의 몇 배?",
       "accept": "2"
      }
     ]
    },
    "model": "$\\beta$는 $p$를 축 $x=p+m$에 대해 뒤집은 자리, 즉 $\\beta=p+2m$이에요. $\\beta$는 $f(x)=g(x)$의 근이니 이게 **두 번째 식**이 돼요."
   },
   {
    "id": "c_m",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q4",
    "prompt": "이제야 계산이에요. $x=p+2m$을 $f(x)=g(x)$에 대입해 $m$을 구하세요.",
    "input": {
     "fields": [
      {
       "label": "$m$",
       "accept": "$verified.m"
      }
     ]
    },
    "hints": [
     {
      "after": "attempts:1",
      "text": "$f(p+2m)=\\frac12(2m)^2+q$, $g(p+2m)=-f(p+m)=-\\frac12m^2-q$예요."
     },
     {
      "after": "attempts:2",
      "text": "$2m^2+q=-\\frac12m^2-q$에 $q=-5$를 넣으면 $m^2$이 나와요. $m>0$!"
     }
    ]
   },
   {
    "id": "c_p",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q4",
    "prompt": "세 번째 식 $f(m)+g(m)=-4$로 $p$를 구하세요.",
    "input": {
     "fields": [
      {
       "label": "$p$",
       "accept": "$verified.p"
      }
     ]
    },
    "hints": [
     {
      "after": "attempts:1",
      "text": "$g(m)=-f(0)$이에요. 그래서 $f(m)+g(m)=\\frac12(m-p)^2-\\frac12p^2$."
     }
    ]
   },
   {
    "id": "c_ans",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q0",
    "prompt": "$m\\times(p-q)$의 값은?",
    "input": {
     "fields": [
      {
       "label": "$m(p-q)$",
       "accept": "$verified.answer_value"
      }
     ]
    }
   },
   {
    "id": "syn",
    "kind": "synthesis",
    "polya": "carry-out"
   }
  ],
  "scenes": {
   "s1": {
    "view": {
     "x": [
      -3,
      9.5
     ],
     "y": [
      -6,
      8
     ],
     "aspect": "free"
    },
    "axes": {
     "x": {
      "name": "x",
      "ticks": 1
     },
     "y": {
      "name": "y",
      "ticks": 1,
      "labels": true
     }
    },
    "objects": [
     {
      "id": "m",
      "type": "slider",
      "label": "m",
      "range": [
       0.5,
       4
      ],
      "step": 0.01,
      "init": 2,
      "readout": "numeric",
      "reveal": "after:p_beta"
     },
     {
      "id": "t",
      "type": "slider",
      "label": "t",
      "range": [
       -5,
       7
      ],
      "step": 0.05,
      "init": 6,
      "readout": "numeric",
      "reveal": "after:p_count"
     },
     {
      "id": "curve_f",
      "type": "function",
      "expr": "0.5*(x-2)^2-4",
      "color": "#9aa0a6",
      "label": "y=f(x)",
      "reveal": "after:p_g",
      "label_at": 2,
      "label_dy": -0.8
     },
     {
      "id": "curve_g",
      "type": "function",
      "expr": "-0.5*(x-2-m)^2+4",
      "color": "#d9822b",
      "label": "y=g(x)",
      "reveal": "after:p_g",
      "label_at": 7.4,
      "label_dy": 0.3
     },
     {
      "id": "curve_h",
      "type": "function",
      "expr": "Math.max(0.5*(x-2)^2-4, -0.5*(x-2-m)^2+4)",
      "main": true,
      "width": 5,
      "reveal": "after:p_h"
     },
     {
      "id": "line_t",
      "type": "function",
      "expr": "t",
      "role": "fixed",
      "color": "#1f8a5b",
      "label": "y=t",
      "reveal": "after:p_count"
     },
     {
      "id": "axis_p",
      "type": "vline",
      "x": "2",
      "label": "x=p",
      "reveal": {
       "any": [
        "after:n_t"
       ]
      }
     },
     {
      "id": "axis_pm",
      "type": "vline",
      "x": "2+m",
      "label": "x=p+m",
      "reveal": {
       "any": [
        "after:n_t"
       ]
      }
     },
     {
      "id": "axis_beta",
      "type": "vline",
      "x": "2+m/2+Math.sqrt(8-m^2/4)",
      "label": "x=β",
      "color": "#2f6fde",
      "reveal": "after:p_beta"
     },
     {
      "id": "line_gp",
      "type": "function",
      "expr": "-0.5*m^2+4",
      "role": "guide",
      "style": "dashed",
      "color": "#c2453a",
      "reveal": "after:p_beta"
     },
     {
      "id": "pt_gp",
      "type": "point-on-curve",
      "curve": "curve_g",
      "x": 2,
      "label": "(p, g(p))",
      "color": "#c2453a",
      "reveal": "after:p_beta"
     },
     {
      "id": "pt_beta",
      "type": "point-on-curve",
      "curve": "curve_h",
      "x": "2+m/2+Math.sqrt(8-m^2/4)",
      "label": "β",
      "color": "#2f6fde",
      "reveal": "after:p_beta"
     },
     {
      "id": "pts",
      "type": "intersections",
      "of": [
       "curve_h",
       "line_t"
      ],
      "distinct": true,
      "highlight": 4,
      "count_label": "h(x)=t 실근: {n}개",
      "sum_target": "4*2+2*m",
      "sum_ok": " · 합 = 4p+2m ✓",
      "sum_no": " · 합 ≠ 4p+2m",
      "reveal": "after:p_count"
     }
    ]
   }
  },
  "synthesis": [
   "$g(x)=-f(x-m)=-\\frac12(x-p-m)^2-q$: 꼭짓점 $(p+m,-q)$인 위로 볼록 포물선. $f(x)=g(x)$의 두 근 사이에서 $g>f$이므로 $h=\\max(f,g)$.",
   "$h(x)=t$의 실근이 4개이면 $f$의 두 근은 $x=p$, $g$의 두 근은 $x=p+m$에 대해 대칭이므로 합은 $4p+2m$. 실근이 2개·3개일 때는 합이 $4p+2m$이 될 수 없다.",
   "실근이 4개인 $t$의 범위는 $h(\\beta)<t<-q$이므로 $-q=5$, $g(\\beta)=g(p)$.",
   "$g$는 $x=p+m$에 대해 대칭이고 $\\beta>p$이므로 $\\beta=p+2m$. $f(p+2m)=g(p+2m)$에서 $2m^2-5=-\\frac12m^2+5$, $m^2=4$, $m=2$.",
   "$f(m)+g(m)=\\frac12(m-p)^2-\\frac12p^2=-4$에서 $m^2-2mp=-8$, $4-4p=-8$, $p=3$.",
   "$m\\times(p-q)=2\\times(3+5)=16$."
  ],
  "verified": {
   "f": "(x-p)**2/2+q",
   "q": "-5",
   "m": "2",
   "p": "3",
   "alpha": "1",
   "beta": "7",
   "band": [
    "3",
    "5"
   ],
   "example": {
    "p": "2",
    "q": "-4",
    "m_mirror": "4/sqrt(5)"
   },
   "answer_value": "16"
  },
  "short": "s03_2025_10월학평_고1_30.mp4",
  "leak_guard": {
   "answer_keys": [
    "answer_value"
   ]
  }
 },
 "2025_6월모평_공통_7": {
  "schema": "discovery-graph/v1",
  "id": "2025_6월모평_공통_7",
  "source": {
   "exam": "2025_6월모평",
   "examLabel": "2025학년도 6월 모의평가",
   "number": 7,
   "section": "공통",
   "score": 3,
   "answer": "④",
   "unit": "수학II-미분",
   "choices": [
    "13",
    "16",
    "19",
    "22",
    "25"
   ]
  },
  "statement": "$x$에 대한 방정식 $x^3-3x^2-9x+k=0$의 서로 다른 실근의 개수가 $2$가 되도록 하는 모든 실수 $k$의 값의 합은? [3점]",
  "understand": {
   "unknown": "조건을 만족시키는 모든 실수 $k$의 값의 합",
   "unknown_hint": "'모든 $k$의 값의 **합**'을 묻는다는 건, 그런 $k$가 무한히 많지 않고 몇 개뿐이라는 뜻이에요.",
   "data": [
    "방정식 $x^3-3x^2-9x+k=0$ ($k$는 실수)"
   ],
   "conditions": [
    {
     "id": "c1",
     "text": "서로 다른 실근의 개수가 $2$",
     "digest": "실근은 그래프 $y=x^3-3x^2-9x+k$가 $x$축과 만나는 점의 $x$좌표예요. 그러니 조건은 '그래프가 $x$축과 **서로 다른 두 점**에서 만난다'는 뜻이고, 한 점에서 닿기만 하는(중근) 경우도 한 번만 세요.",
     "deferred": false
    }
   ]
  },
  "analysis": [
   {
    "id": "q0",
    "ask": "모든 $k$의 값의 합을 알려면 무엇을 알아야 하나?",
    "needs": [
     "q1"
    ],
    "heuristic": "work-backward"
   },
   {
    "id": "q1",
    "ask": "실근이 2개가 되는 $k$는 어떤 값들이고, 몇 개인가?",
    "needs": [
     "q2",
     "q3",
     "q4"
    ],
    "heuristic": "vary-parameter"
   },
   {
    "id": "q2",
    "ask": "$k=0$일 때 그래프는 어떤 개형인가?",
    "needs": [],
    "heuristic": "draw-figure"
   },
   {
    "id": "q3",
    "ask": "$k$를 바꾸면 그래프는 어떻게 변하나?",
    "needs": [],
    "heuristic": "vary-parameter"
   },
   {
    "id": "q4",
    "ask": "봉우리·골짜기의 높이는 정확히 얼마인가?",
    "needs": [],
    "heuristic": "compute"
   }
  ],
  "path": [
   {
    "id": "u_unknown",
    "kind": "ask",
    "polya": "understand",
    "answers": "q0",
    "prompt": "먼저 **구하는 것**을 보세요. 문제는 '모든 실수 $k$의 값의 **합**'을 묻고 있어요.",
    "input": {
     "fields": [
      {
       "label": "그렇다면 조건을 만족하는 $k$는",
       "type": "select",
       "options": [
        "몇 개뿐이다",
        "무수히 많다",
        "하나도 없을 수도 있다"
       ],
       "accept": "몇 개뿐이다"
      }
     ]
    },
    "model": "$UNDERSTAND.unknown_hint",
    "history": "<b>구하는 것</b> — 합을 묻는다 → 그런 $k$는 몇 개뿐"
   },
   {
    "id": "u_digest",
    "kind": "ask",
    "polya": "understand",
    "prompt": "조건 '서로 다른 실근의 개수가 2'를 **그래프의 말**로 바꾸면?",
    "input": {
     "fields": [
      {
       "label": "그래프 $y=x^3-3x^2-9x+k$가 $x$축과",
       "type": "select",
       "options": [
        "서로 다른 두 점에서 만난다",
        "두 번 접한다",
        "한 점에서만 만난다"
       ],
       "accept": "서로 다른 두 점에서 만난다"
      }
     ]
    },
    "model": "실근은 그래프가 $x$축과 만나는 점의 $x$좌표예요. 한 점에서 닿기만 하는(중근) 경우도 **한 번만** 세요.",
    "history": "<b>조건 뜯어보기</b> — 실근 2개 ⇔ 그래프가 $x$축과 서로 다른 두 점에서 만남"
   },
   {
    "id": "p_shape",
    "kind": "predict",
    "polya": "plan",
    "answers": "q2",
    "scene": "s1",
    "prompt": "거꾸로 생각하면, 그런 $k$를 찾으려면 $k$가 그래프에 무슨 일을 하는지 알아야 해요. 그 전에 — 곡선을 **보기 전에** $k=0$일 때 $y=x^3-3x^2-9x$의 개형을 캔버스에 손으로 그려 보세요. ($y'=3x^2-6x-9$의 부호를 떠올리면 도움이 돼요.)",
    "predict": {
     "kind": "shape",
     "grade": "hard",
     "max_attempts": 2,
     "accept": {
      "turning_points": 2,
      "ends": [
       "down",
       "up"
      ]
     },
     "soft_checks": {
      "slope_sign_at": {
       "0": "-"
      }
     },
     "on_fail": [
      "봉우리·골짜기(극값)는 몇 개일까요? $y'=0$의 실근 개수를 세어 보세요.",
      "최고차항 $x^3$의 계수가 양수예요. $x$가 아주 크면 $y$는? 아주 작으면?"
     ]
    },
    "hints": [
     {
      "after": "seconds:120",
      "text": "$y'=3(x+1)(x-3)$이에요. $x=-1$과 $x=3$ 사이에서 $y'$의 부호는?"
     }
    ]
   },
   {
    "id": "n_shape",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "prompt": "실제 곡선이 열렸어요. 눈금을 읽어 보세요.",
    "input": {
     "fields": [
      {
       "label": "봉우리(극대)의 $x$좌표",
       "accept": "-1"
      },
      {
       "label": "골짜기(극소)의 $x$좌표",
       "accept": "3"
      }
     ]
    },
    "model": "극값이 두 개인 'N자' 개형이에요. 봉우리는 $x=-1$, 골짜기는 $x=3$에 있어요."
   },
   {
    "id": "p_shift",
    "kind": "predict",
    "polya": "plan",
    "answers": "q3",
    "prompt": "$k$를 $0$에서 **더 크게** 바꾸면 그래프는 어떻게 될까요?",
    "predict": {
     "kind": "choice",
     "grade": "soft",
     "options": [
      "모양이 바뀐다",
      "통째로 위로 올라간다",
      "통째로 아래로 내려간다",
      "옆으로 움직인다"
     ],
     "correct": "통째로 위로 올라간다"
    }
   },
   {
    "id": "e_shift",
    "kind": "explore",
    "polya": "plan",
    "answers": "q3",
    "scene": "s1",
    "prompt": "슬라이더 $k$를 오른쪽·왼쪽으로 움직여 보세요. (눈금은 일부러 가려 두었어요.)",
    "checkpoint": {
     "all": [
      {
       "type": "visited-range",
       "slider": "k",
       "range": [
        12,
        40
       ]
      },
      {
       "type": "visited-range",
       "slider": "k",
       "range": [
        -40,
        -12
       ]
      }
     ]
    }
   },
   {
    "id": "n_shift",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "prompt": "$k$는 그래프에 무슨 일을 했나요?",
    "input": {
     "fields": [
      {
       "label": "$k$를 키우면 그래프는",
       "type": "select",
       "options": [
        "모양은 그대로, 통째로 위로 올라간다",
        "모양이 바뀐다",
        "옆으로 움직인다"
       ],
       "accept": "모양은 그대로, 통째로 위로 올라간다"
      }
     ]
    },
    "model": "$k$는 그래프를 위아래로 **평행이동**시켜요. 그러니 '실근이 2개인 $k$'는 '그래프를 얼마나 올리거나 내려야 $x$축과 두 점에서 만나는가'라는 질문이 돼요."
   },
   {
    "id": "p_count",
    "kind": "predict",
    "polya": "plan",
    "answers": "q1",
    "prompt": "$k$를 아주 작은 값에서 아주 큰 값까지 천천히 올리면, $x$축과 만나는 점의 개수는 어떤 순서로 바뀔까요? (예: 1, 3, 1)",
    "predict": {
     "kind": "sequence",
     "grade": "soft",
     "accept": {
      "values": [
       1,
       2,
       3,
       2,
       1
      ]
     }
    }
   },
   {
    "id": "e_count",
    "kind": "explore",
    "polya": "plan",
    "answers": "q1",
    "scene": "s1",
    "role": "decisive",
    "prompt": "이제 $x$축과 만나는 점의 개수가 화면에 표시돼요. 슬라이더를 천천히 움직이며 **개수가 정확히 2가 되는 순간**을 모두 찾아 보세요.",
    "checkpoint": {
     "type": "count-equals",
     "of": "roots",
     "value": 2,
     "times": 2
    },
    "hints": [
     {
      "after": "seconds:60",
      "text": "개수가 3에서 1로 '건너뛰는' 것처럼 보이나요? 그 사이에서 한 칸씩 움직여 보세요."
     },
     {
      "after": "seconds:120",
      "text": "봉우리나 골짜기가 $x$축에 가까워질 때를 잘 보세요."
     }
    ]
   },
   {
    "id": "n_count",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "role": "decisive",
    "prompt": "개수가 2가 된 순간을 떠올려 보세요.",
    "input": {
     "fields": [
      {
       "label": "개수가 2가 되는 순간은 몇 번?",
       "accept": "2"
      },
      {
       "label": "그 순간 그래프는",
       "type": "select",
       "options": [
        "봉우리나 골짜기가 $x$축에 닿아 있었다",
        "원점을 지나고 있었다",
        "$y$축과 만나고 있었다"
       ],
       "accept": "봉우리나 골짜기가 $x$축에 닿아 있었다"
      }
     ]
    },
    "model": "개수가 2가 되는 순간은 **봉우리 또는 골짜기가 $x$축에 딱 닿을(접할) 때**뿐이에요. 그래서 구하는 $k$는 두 개: '봉우리 높이 $+k=0$'과 '골짜기 높이 $+k=0$'."
   },
   {
    "id": "c_ext",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q4",
    "prompt": "$y=x^3-3x^2-9x$의 **극댓값**과 **극솟값**을 계산해 보세요.",
    "input": {
     "fields": [
      {
       "label": "극댓값",
       "accept": "$verified.local_max"
      },
      {
       "label": "극솟값",
       "accept": "$verified.local_min"
      }
     ]
    },
    "hints": [
     {
      "after": "attempts:1",
      "text": "$y'=3(x+1)(x-3)=0$에서 $x=-1$, $x=3$이에요."
     },
     {
      "after": "attempts:2",
      "text": "$x=-1$과 $x=3$을 원래 식에 대입하세요."
     }
    ]
   },
   {
    "id": "c_k",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q1",
    "prompt": "봉우리가 $x$축에 닿으려면 그래프를 얼마나 내려야 하나요? 골짜기는 얼마나 올려야 하나요? 그때의 $k$를 각각 구하세요.",
    "input": {
     "fields": [
      {
       "label": "봉우리가 닿는 $k$",
       "accept": "$verified.k_max_touch"
      },
      {
       "label": "골짜기가 닿는 $k$",
       "accept": "$verified.k_min_touch"
      }
     ]
    },
    "on_success": "이제 슬라이더 눈금을 열어 줄게요. 직접 그 값에 맞춰 확인해 보세요."
   },
   {
    "id": "c_ans",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q0",
    "prompt": "모든 $k$의 값의 합은?",
    "input": {
     "fields": [
      {
       "label": "합",
       "accept": "$verified.answer_value"
      }
     ]
    }
   },
   {
    "id": "syn",
    "kind": "synthesis",
    "polya": "carry-out"
   }
  ],
  "scenes": {
   "s1": {
    "view": {
     "x": [
      -5,
      7
     ],
     "y": [
      -45,
      40
     ],
     "aspect": "free"
    },
    "axes": {
     "x": {
      "name": "x",
      "ticks": 1
     },
     "y": {
      "name": "y",
      "ticks": 10,
      "labels": false
     }
    },
    "objects": [
     {
      "id": "k",
      "type": "slider",
      "label": "k",
      "range": [
       -40,
       40
      ],
      "step": 1,
      "init": 0,
      "readout": "hidden",
      "readout_reveal": "after:c_k",
      "reveal": "after:p_shift"
     },
     {
      "id": "curve_f",
      "type": "function",
      "expr": "x^3-3*x^2-9*x+k",
      "label": "y = x³ − 3x² − 9x + k",
      "reveal": "after:p_shape"
     },
     {
      "id": "yint",
      "type": "point-on-curve",
      "curve": "curve_f",
      "x": 0,
      "label": "y절편",
      "reveal": "after:p_shift",
      "role": "guide"
     },
     {
      "id": "roots",
      "type": "intersections",
      "of": [
       "curve_f",
       "@x-axis"
      ],
      "distinct": true,
      "merge_tol": 1e-06,
      "count_label": "x축과 만나는 점: {n}개",
      "reveal": "after:p_count"
     }
    ]
   }
  },
  "synthesis": [
   "$f(x)=x^3-3x^2-9x+k$라 하면 $f'(x)=3x^2-6x-9=3(x+1)(x-3)$.",
   "$x=-1$에서 극댓값 $f(-1)=5+k$, $x=3$에서 극솟값 $f(3)=-27+k$.",
   "삼차방정식의 서로 다른 실근이 2개 ⇔ 극댓값 또는 극솟값이 $0$ (그래프가 $x$축에 접함).",
   "$5+k=0$에서 $k=-5$, $-27+k=0$에서 $k=27$.",
   "따라서 모든 $k$의 값의 합은 $-5+27=22$. 답 ④"
  ],
  "verified": {
   "f": "x**3-3*x**2-9*x",
   "critical_x": [
    "-1",
    "3"
   ],
   "local_max": "5",
   "local_min": "-27",
   "k_max_touch": "-5",
   "k_min_touch": "27",
   "k_values": [
    "-5",
    "27"
   ],
   "count_sequence": [
    1,
    2,
    3,
    2,
    1
   ],
   "answer_value": "22",
   "answer_choice": "④"
  },
  "short": "s01_2025_6월모평_7.mp4",
  "leak_guard": {
   "choice_gap": 3
  }
 },
 "2026_수능_공통_9": {
  "schema": "discovery-graph/v1",
  "id": "2026_수능_공통_9",
  "source": {
   "exam": "2026_수능",
   "examLabel": "2026학년도 대학수학능력시험",
   "number": 9,
   "section": "공통",
   "score": 4,
   "answer": "④",
   "unit": "수학II-미분",
   "choices": [
    "11",
    "12",
    "13",
    "14",
    "15"
   ]
  },
  "statement": "양수 $a$에 대하여 함수 $f(x)$를\n$f(x)=x^3+3ax^2-9a^2x+4$\n라 하자. 직선 $y=5$가 곡선 $y=f(x)$에 접할 때, $f(2)$의 값은? [4점]",
  "understand": {
   "unknown": "$f(2)$의 값 — 결국 양수 $a$ 하나만 정하면 된다",
   "unknown_hint": "$f(2)=8+12a-18a^2+4$예요. 그러니 구하는 것은 사실상 **$a$ 하나**예요. 그런데 $a$를 정해 줄 조건은 '$y=5$가 접한다'는 한 줄뿐이에요.",
   "data": [
    "$f(x)=x^3+3ax^2-9a^2x+4$",
    "$a>0$"
   ],
   "conditions": [
    {
     "id": "c1",
     "text": "직선 $y=5$가 곡선 $y=f(x)$에 접한다",
     "digest": "$y=5$는 $x$축에 평행한 **수평선**이에요. '접한다'는 곡선과 만나되 그 점에서 뚫고 지나가지 않고 **스치는** 것이에요. 어디에서 스칠지는 아직 몰라요 — 그림을 보며 찾아야 해요.",
     "deferred": false
    },
    {
     "id": "c2",
     "text": "$a$는 양수",
     "digest": "$a$는 아직 모르는 수이지만, **움직여 볼 수 있는 손잡이**이기도 해요. $a$가 바뀌면 곡선 모양이 바뀌고, 어느 순간 $y=5$에 스치게 될 거예요. '양수'라는 조건은 지금 당장 쓸 데가 없으니 **미뤄 두었다가** 나중에 꺼내 써요.",
     "deferred": true
    }
   ]
  },
  "analysis": [
   {
    "id": "q0",
    "ask": "$f(2)$를 알려면 무엇을 알아야 하나?",
    "needs": [
     "q1"
    ],
    "heuristic": "work-backward"
   },
   {
    "id": "q1",
    "ask": "'접한다'를 $a$에 대한 식으로 바꾸려면?",
    "needs": [
     "q2",
     "q3",
     "q4"
    ],
    "heuristic": "vary-parameter"
   },
   {
    "id": "q2",
    "ask": "$a=\\tfrac12$일 때 곡선은 어떤 개형인가?",
    "needs": [],
    "heuristic": "draw-figure"
   },
   {
    "id": "q3",
    "ask": "수평선 $y=5$는 곡선의 어디에 닿는가? 봉우리? 골짜기?",
    "needs": [],
    "heuristic": "vary-parameter"
   },
   {
    "id": "q4",
    "ask": "봉우리·골짜기의 위치와 높이를 $a$로 나타내면?",
    "needs": [],
    "heuristic": "compute"
   }
  ],
  "path": [
   {
    "id": "u_unknown",
    "kind": "ask",
    "polya": "understand",
    "answers": "q0",
    "prompt": "먼저 **구하는 것** $f(2)$를 보세요. $f(2)$를 $a$로 나타내 보세요. (예: 3+2a-a^2)",
    "input": {
     "fields": [
      {
       "label": "$f(2)=$",
       "type": "expr",
       "var": "a",
       "accept": "12+12*a-18*a**2"
      }
     ]
    },
    "model": "구하는 것은 사실상 **$a$ 하나**예요. 그런데 $a$를 정해 줄 조건은 '$y=5$가 접한다'는 한 줄뿐이에요. ('$a$는 양수'는 지금은 쓸 데가 없으니 미뤄 둬요.)",
    "history": "<b>구하는 것</b> — $f(2)$, 즉 $a$ 하나. 조건은 '접한다' 한 줄"
   },
   {
    "id": "p_shape",
    "kind": "predict",
    "polya": "plan",
    "answers": "q2",
    "scene": "s1",
    "prompt": "거꾸로: $a$를 정하려면 '접한다'를 $a$의 식으로 바꿔야 하고, 그러려면 접하는 순간 곡선이 어떤 모습인지 봐야 해요. 먼저 곡선을 **보기 전에**, $a=\\tfrac12$일 때 $y=x^3+\\tfrac32x^2-\\tfrac94x+4$의 개형을 캔버스에 손으로 그려 보세요.",
    "predict": {
     "kind": "shape",
     "grade": "hard",
     "max_attempts": 2,
     "accept": {
      "turning_points": 2,
      "ends": [
       "down",
       "up"
      ]
     },
     "on_fail": [
      "봉우리·골짜기(극값)는 몇 개일까요? $f'(x)=0$의 실근 개수를 세어 보세요.",
      "최고차항 $x^3$의 계수가 양수예요. $x$가 아주 크면 $y$는? 아주 작으면?"
     ]
    },
    "hints": [
     {
      "after": "seconds:120",
      "text": "$a=\\tfrac12$이면 $f'(x)=3x^2+3x-\\tfrac94=3\\left(x+\\tfrac32\\right)\\left(x-\\tfrac12\\right)$이에요."
     }
    ]
   },
   {
    "id": "n_shape",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "prompt": "실제 곡선이 열렸어요. 눈금을 읽어 보세요.",
    "input": {
     "fields": [
      {
       "label": "$y$절편",
       "accept": "4"
      },
      {
       "label": "봉우리(극대)는 $y$축의",
       "type": "select",
       "options": [
        "왼쪽",
        "오른쪽"
       ],
       "accept": "왼쪽"
      }
     ]
    },
    "model": "극값이 두 개인 'N자' 개형이에요. 봉우리는 $y$축 왼쪽, 골짜기는 오른쪽에 있고, $y$절편은 $4$예요."
   },
   {
    "id": "p_line",
    "kind": "predict",
    "polya": "plan",
    "answers": "q3",
    "prompt": "이 그림 위에 수평선 $y=5$를 겹치면, 지금($a=\\tfrac12$) 곡선과 **몇 번** 만날까요?",
    "predict": {
     "kind": "count",
     "grade": "soft",
     "accept": {
      "value": 3
     }
    }
   },
   {
    "id": "e_vary",
    "kind": "explore",
    "polya": "plan",
    "answers": "q3",
    "scene": "s1",
    "role": "decisive",
    "prompt": "이제 $y=5$와 만나는 점의 개수가 화면에 표시돼요. 슬라이더 $a$를 움직여 개수가 **바뀌는 순간**을 찾고, 개수가 **2**가 되는 곳에 멈춰 보세요. (눈금은 일부러 가려 두었어요.)",
    "checkpoint": {
     "type": "count-equals",
     "of": "pts",
     "value": 2,
     "times": 1
    },
    "hints": [
     {
      "after": "seconds:60",
      "text": "$a$를 줄이면 봉우리는 올라가나요, 내려가나요?"
     },
     {
      "after": "seconds:120",
      "text": "개수가 3에서 1로 '건너뛰는' 것처럼 보이나요? 슬라이더를 클릭한 뒤 ← → 키로 한 칸씩 움직여 보세요."
     }
    ]
   },
   {
    "id": "n_vary",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "role": "decisive",
    "prompt": "개수가 2가 된 순간을 떠올려 보세요.",
    "input": {
     "fields": [
      {
       "label": "그때 $y=5$는 곡선의",
       "type": "select",
       "options": [
        "봉우리 꼭대기에 닿아 있었다",
        "골짜기 바닥에 닿아 있었다",
        "곡선을 뚫고 지나가고 있었다"
       ],
       "accept": "봉우리 꼭대기에 닿아 있었다"
      }
     ]
    },
    "model": "접점에서 곡선은 수평선과 같은 방향(기울기 $0$)이니 접점은 **극점**이고, 그 **극값이 $5$**예요."
   },
   {
    "id": "p_valley",
    "kind": "predict",
    "polya": "plan",
    "answers": "q3",
    "prompt": "그런데 극점은 두 개예요. 슬라이더를 어디까지 움직이면 **골짜기**가 $y=5$에 닿을 수도 있을까요?",
    "predict": {
     "kind": "choice",
     "grade": "soft",
     "options": [
      "있다 — $a$를 키우면 골짜기도 올라온다",
      "있다 — $a$를 줄이면 골짜기도 올라온다",
      "없다 — 골짜기는 $5$까지 못 올라온다",
      "모르겠다, 확인해 보자"
     ],
     "correct": "없다 — 골짜기는 $5$까지 못 올라온다"
    }
   },
   {
    "id": "e_sweep",
    "kind": "explore",
    "polya": "plan",
    "answers": "q3",
    "scene": "s1",
    "prompt": "슬라이더를 **양 끝까지** 천천히 쓸어 보세요. 봉우리(빨강)와 골짜기(파랑)가 지나간 자리가 남아요. 곡선이 $a$와 상관없이 **늘 지나는 점**도 찾아 보세요.",
    "checkpoint": {
     "all": [
      {
       "type": "visited-range",
       "slider": "a",
       "range": [
        0.1,
        0.15
       ]
      },
      {
       "type": "visited-range",
       "slider": "a",
       "range": [
        0.55,
        0.6
       ]
      }
     ]
    }
   },
   {
    "id": "n_sweep",
    "kind": "notice",
    "polya": "plan",
    "scene": "s1",
    "role": "decisive",
    "prompt": "쓸어 보며 본 것을 확인해 봐요.",
    "input": {
     "fields": [
      {
       "label": "곡선이 $a$와 상관없이 늘 지나는 점의 $y$좌표",
       "accept": "4"
      },
      {
       "label": "골짜기는 늘 $y=4$보다",
       "type": "select",
       "options": [
        "아래에 있다",
        "위에 있다",
        "같은 높이다"
       ],
       "accept": "아래에 있다"
      }
     ]
    },
    "model": "곡선은 늘 $(0,4)$를 지나고, 봉우리는 늘 $y=4$보다 **위**, 골짜기는 늘 **아래**에 머물러요. $y=5$에 닿을 수 있는 건 **봉우리뿐** — 조건은 '**극댓값 $=5$**' 한 줄이 돼요."
   },
   {
    "id": "c_extx",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q4",
    "prompt": "이제야 계산이에요. $f'(x)=0$을 풀어 두 극점의 $x$좌표를 $a$로 나타내세요. (예: 2a, -a/2)",
    "input": {
     "fields": [
      {
       "label": "작은 근",
       "type": "expr",
       "var": "a",
       "accept": "$verified.x_left"
      },
      {
       "label": "큰 근",
       "type": "expr",
       "var": "a",
       "accept": "$verified.x_right"
      }
     ]
    },
    "hints": [
     {
      "after": "attempts:1",
      "text": "$f'(x)=3x^2+6ax-9a^2$이에요. $3$으로 묶은 뒤 인수분해해 보세요."
     },
     {
      "after": "attempts:2",
      "text": "$x^2+2ax-3a^2=(x+3a)(x-a)$"
     }
    ]
   },
   {
    "id": "r_pos",
    "kind": "recall",
    "polya": "carry-out",
    "condition": "c2",
    "answers": "q4",
    "prompt": "미뤄 둔 조건 '**$a$는 양수**'를 꺼낼 때예요.",
    "input": {
     "fields": [
      {
       "label": "$a>0$이면 봉우리(극대)는",
       "type": "select",
       "options": [
        "$x=-3a$",
        "$x=a$"
       ],
       "accept": "$x=-3a$"
      }
     ]
    },
    "model": "$a>0$이라서 $-3a<0<a$예요. N자 개형에서 왼쪽 극점이 봉우리이므로 **$x=-3a$에서 극대, $x=a$에서 극소**예요. ($a<0$이었다면 순서가 뒤바뀌어요!)",
    "history": "<b>미룬 조건 회수</b> — $a>0$이므로 $x=-3a$에서 극대, $x=a$에서 극소"
   },
   {
    "id": "c_val",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q4",
    "prompt": "극댓값과 극솟값을 $a$로 나타내세요. (예: 2a^3+1)",
    "input": {
     "fields": [
      {
       "label": "극댓값 $f(-3a)$",
       "type": "expr",
       "var": "a",
       "accept": "$verified.local_max"
      },
      {
       "label": "극솟값 $f(a)$",
       "type": "expr",
       "var": "a",
       "accept": "$verified.local_min"
      }
     ]
    },
    "hints": [
     {
      "after": "attempts:1",
      "text": "$(-3a)^3$, $3a\\cdot(-3a)^2$, $-9a^2\\cdot(-3a)$를 하나씩 계산해 더해 보세요."
     }
    ],
    "on_success": "극솟값 $4-5a^3$은 $a>0$이면 언제나 $4$보다 작아요 — 그래프에서 본 그대로죠."
   },
   {
    "id": "c_a",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q1",
    "prompt": "'극댓값 $=5$'를 풀어 $a$를 구하세요.",
    "input": {
     "fields": [
      {
       "label": "$a$",
       "accept": "$verified.a_value"
      }
     ]
    },
    "hints": [
     {
      "after": "attempts:1",
      "text": "$27a^3+4=5$에서 $a^3=\\tfrac1{27}$이에요."
     }
    ],
    "on_success": "이제 슬라이더 눈금을 열어 줄게요. 그 값 근처에서 정말 접하는지 확인해 보세요."
   },
   {
    "id": "c_ans",
    "kind": "compute",
    "polya": "carry-out",
    "answers": "q0",
    "prompt": "$f(2)$의 값은?",
    "input": {
     "fields": [
      {
       "label": "$f(2)$",
       "accept": "$verified.answer_value"
      }
     ]
    }
   },
   {
    "id": "syn",
    "kind": "synthesis",
    "polya": "carry-out"
   }
  ],
  "scenes": {
   "s1": {
    "view": {
     "x": [
      -3,
      2.5
     ],
     "y": [
      -1,
      11
     ],
     "aspect": "free"
    },
    "axes": {
     "x": {
      "name": "x",
      "ticks": 1
     },
     "y": {
      "name": "y",
      "ticks": 1,
      "labels": true
     }
    },
    "objects": [
     {
      "id": "a",
      "type": "slider",
      "label": "a",
      "range": [
       0.1,
       0.6
      ],
      "step": 0.005,
      "init": 0.5,
      "readout": "hidden",
      "readout_reveal": "after:c_a",
      "reveal": "after:p_line"
     },
     {
      "id": "curve_f",
      "type": "function",
      "expr": "x^3+3*a*x^2-9*a^2*x+4",
      "label": "y = f(x)",
      "reveal": "after:p_shape"
     },
     {
      "id": "line_5",
      "type": "function",
      "expr": "5",
      "role": "fixed",
      "style": "solid",
      "color": "#d9822b",
      "label": "y=5",
      "reveal": "after:p_line"
     },
     {
      "id": "line_4",
      "type": "function",
      "expr": "4",
      "role": "guide",
      "style": "dashed",
      "label": "y=4",
      "reveal": "after:n_sweep"
     },
     {
      "id": "yint",
      "type": "point-on-curve",
      "curve": "curve_f",
      "x": 0,
      "color": "#333",
      "reveal": "after:p_valley",
      "role": "guide"
     },
     {
      "id": "pmax",
      "type": "point-on-curve",
      "curve": "curve_f",
      "x": "-3*a",
      "label": "봉우리",
      "color": "#c2453a",
      "trace": true,
      "reveal": "after:p_valley"
     },
     {
      "id": "pmin",
      "type": "point-on-curve",
      "curve": "curve_f",
      "x": "a",
      "label": "골짜기",
      "color": "#2f6fde",
      "trace": true,
      "reveal": "after:p_valley"
     },
     {
      "id": "pts",
      "type": "intersections",
      "of": [
       "curve_f",
       "line_5"
      ],
      "distinct": true,
      "touch_tol": 0.03,
      "merge_x": 0.2,
      "highlight": 2,
      "count_label": "y=5와 만나는 점: {n}개",
      "reveal": "after:p_line"
     }
    ]
   }
  },
  "synthesis": [
   "$f'(x)=3x^2+6ax-9a^2=3(x+3a)(x-a)$이고 $a>0$이므로 $x=-3a$에서 극대, $x=a$에서 극소.",
   "극댓값 $f(-3a)=27a^3+4$, 극솟값 $f(a)=4-5a^3$.",
   "수평선 $y=5$가 접하면 접점에서 $f'=0$이므로 접점은 극점이고, 그 극값이 $5$이다.",
   "$a>0$이면 극솟값 $4-5a^3<4<5$이므로 극솟값은 $5$가 될 수 없다. 따라서 $27a^3+4=5$, $a=\\tfrac13$.",
   "(확인) $a=\\tfrac13$이면 $f(x)-5=(x+1)^2(x-1)$ — $x=-1$이 중근이므로 정말 접한다.",
   "$f(2)=8+12a-18a^2+4=8+4-2+4=14$. 답 ④"
  ],
  "verified": {
   "f": "x**3+3*a*x**2-9*a**2*x+4",
   "x_left": "-3*a",
   "x_right": "a",
   "local_max": "27*a**3+4",
   "local_min": "4-5*a**3",
   "a_value": "1/3",
   "tangent_point": [
    "-1",
    "5"
   ],
   "count_at_half": 3,
   "answer_value": "14",
   "answer_choice": "④"
  },
  "leak_guard": {
   "answer_keys": [
    "a_value",
    "answer_value"
   ]
  }
 }
};
