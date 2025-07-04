"""
ragas_demo.py
─────────────
Assistant 응답·질문·근거(contexts)를 수동으로 입력해
RAGAS 평가 지표(faithfulness, answer_relevancy)를 빠르게 확인하는 스크립트
"""

from ragas.metrics import faithfulness, answer_relevancy
from ragas import evaluate
from datasets import Dataset  # 👈 추가
import json
from typing import List, Dict

# ─────────────────────────────────────────
# 1) job_list → contexts 리스트 변환
# ─────────────────────────────────────────
def job_list_to_contexts(job_list: List[Dict], truncate: bool = False, max_items: int = 5) -> List[str]:
    """
    job_list (파싱된 리스트[dict])를 RAGAS용 contexts 리스트로 변환
    - truncate=True 이면 각 항목을 max_items개까지만 넣고 '... (생략)' 추가
    """
    contexts: List[str] = []

    for job in job_list:
        # 직무명
        contexts.append(f"직무명: {job.get('직무명', '')}")

        # helper 내부 함수
        def add_items(prefix: str, items: List[str]):
            for i, item in enumerate(items):
                if truncate and i >= max_items:
                    contexts.append(f"{prefix}: ... (생략)")
                    break
                contexts.append(f"{prefix}: {item}")

        add_items("담당업무", job.get("담당업무", []))
        add_items("자격요건", job.get("자격요건", []))
        add_items("필수사항", job.get("필수사항", []))
        add_items("우대사항", job.get("우대사항", []))

        # 인재상은 한 줄로 합쳐도 무방
        if "인재상" in job:
            contexts.append(f"인재상: {', '.join(job['인재상'])}")

    return contexts
    
# =====================================================
# 📝 ① 여기서 직접 입력하세요
# =====================================================
job_json_str = """
[
  {
    "직무명": "Tech PM(Project Manager)",
    "담당업무": [
      "현대 / 기아 자동차 공장 내 생산 차량에 대한 검사 설비 개발",
      "검사 설비 개발 사양 분석",
      "검사 설비 S/W 개발 (UI 및 제어 프로그램 개발)",
      "검차 설비 구축 및 외부 장비와의 인터페이스 구성",
      "검차 설비 운영 및 유지보수",
      "생산 라인 내 설비 이슈 진단 및 문제 해결",
      "고객(공장 측)과의 현장 대응 및 기술 지원"
    ],
    "자격요건": [
      "C++, C# 등 프로그래밍 언어 사용 가능자",
      "관련 프로그램 개발 경험 보유자 (경력 무관, 실무 중심이면 가능)"
    ],
    "필수사항": [
      "C++, C# 등 프로그래밍 언어 사용 가능자",
      "관련 프로그램 개발 경험 보유자 (경력 무관, 실무 중심이면 가능)"
    ],
    "우대사항": [
      "컴퓨터, 전자, 제어, 로봇, 소프트웨어공학 등 관련 전공자",
      "자동차 검차 설비에 대한 이해 보유자 (※ 경험이 없어도 실무를 통해 역량 향상 가능)",
      "자동차 통신 프로토콜(CAN, KWP 등) 이해",
      "진단기 및 진단 장비 활용 경험"
    ],
    "인재상": [
      "열정과 도전, 소통과 협력, 창의와 혁신, 학습과 성장"
    ]
  }
]
""".strip()
job_list = json.loads(job_json_str)
# (1) contexts 생성
contexts = job_list_to_contexts(job_list, truncate=True, max_items=3)

assistant_answer = """
1. 적합성 평가
   - 지원자의 답변은 Python 기반 검사 시스템 개발 경험을 기술하고 있으며, 이는 기술적 역량을 보여주려는 시도로 볼 수 있지만, 해당 직무인 Tech PM 포지션은 C++ 및 C#을 사용하는 프로그램 개발이 주 요구사항이므로 적합성이 부족합니다. 자동차 검사 설비와 관련된 경험을 통해 지원자가 이 직무에 어떤 기여를 할 수 있는지를 명확하게 제시할 필요가 있습니다. 인재상이 요구하는 '열정과 도전, 소통과 협력'과 같은 가치관에 대한 언급이나 관련 경험이 필요하며, 이를 통해 직무와의 연관성을 높이는 것이 중요합니다.

2. 보완/개선 제안
   - 지원자는 C++ 또는 C#에 대한 경험이 부족하다면 관련 언어의 학습이나 적응 의지를 강조해야 합니다. 예를 들어, “비록 주로 Python을 사용했지만, C++ 및 C#의 기본기를 학습하고 있으며, 이를 통해 검사 설비 소프트웨어 개발에 기여하고자 합니다.”라는 내용이 좋습니다. 또한, 자동차 통신 프로토콜이나 검사 설비에 대한 이해도를 높이기 위해 관련 지식을 습득한 경험이나 내용을 포함시키는 것이 필요합니다. 현장 대응에 대한 경험이 있다면 고객과의 소통 또는 문제 해결에 대한 사례도 덧붙여, 직무에 대한 적합성을 한층 강화할 수 있습니다.

3. 가산점 요소·표현
   - 지원자가 자신의 경험을 직무에 의해 요구되는 역량과 연결해야 긍정적인 인상을 줄 수 있습니다. 예를 들어, "과거 프로젝트에서 각각의 로직을 모듈화하여 유지보수를 용이하게 만들었습니다. 이러한 시스템적 사고는 검사 설비의 S/W 개발 과정에서도 큰 도움이 될 것입니다."라는 표현은 지원자의 경험을 더 잘 직무와 연결시키는 데 도움이 됩니다. 추가로, “고객의 요구 사항을 반영하여 시스템을 개선한 경험이 있으며, 이를 통해 고객과의 관계를 더욱 돈독히 하며 효과적으로 대응할 수 있습니다.”와 같은 문장은 소통과 협력 능력을 강조할 수 있습니다. 이러한 요소들을 포함시킴으로써 지원자의 전체적인 적합성을 높일 수 있습니다.
"""

user_question = """
저는 자동차 생산 공정의 품질 확보를 위해 Python 기반 검사 시스템을 개발한 경험이 있습니다. 공정 내 부품 이상을 실시간으로 감지하는 비전 검사 프로그램을 구현하며, 카메라와 PLC 장비를 연동해 데이터를 수집하고, 이상을 탐지하면 즉시 알람을 출력하는 로직을 설계했습니다. 또한 사용자 친화적인 UI를 개발해 작업자의 효율성을 높였고, 유지보수가 쉽도록 모듈화하였습니다. 이러한 경험을 바탕으로 귀사에서 검사 설비의 소프트웨어 개발과 현장 대응에 기여하겠습니다.
"""

# =====================================================
# ② RAGAS 입력 샘플 구성
# =====================================================
samples = [
    {
        "question": user_question.strip(),
        "answer":   assistant_answer.strip(),
        "contexts": [c.strip() for c in contexts],
    }
]
dataset = Dataset.from_list(samples)
# =====================================================
# ③ RAGAS 평가 실행
# =====================================================

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy]
)

print("\n🟢 RAGAS 평가 결과")
print(result)