# grade_calculator.py

import functools
from typing import List, Dict, Tuple

def calculate_total(scores: List[int]) -> int:
    """
    주어진 점수 리스트의 총점을 누적 계산하여 반환합니다.
    
    Args:
        scores (List[int]): 점수들이 담긴 리스트
        
    Returns:
        int: 모든 점수의 합 (리스트가 비어있으면 0 반환)
    """
    if not scores:
        return 0
        
    # functools.reduce: 순회 가능한 데이터(scores)의 요소를 차례대로 누적(acc)하여 단일 결과값을 만듭니다.
    # 초기값을 지정하지 않으면 리스트의 첫 번째 요소가 초기 누적값이 됩니다.
    # total: int = functools.reduce(lambda acc, current: acc + current, scores)
    # return total
    total = 0
    for score in scores:
        total += score
    return total


def determine_grade(score: int) -> str:
    """
    단일 점수를 입력받아 A~F까지의 학점 등급을 산출합니다.
    
    Args:
        score (int): 0~100 사이의 점수
        
    Returns:
        str: 산출된 학점 등급 (A, B, C, D, F)
    """
    # divmod: 점수를 10으로 나눈 몫(quotient)과 나머지(remainder)를 튜플로 반환합니다.
    # 등급 산출 로직에서는 일의 자리 나머지보다는 '몫(십의 자리 수)'이 핵심이므로 
    # 나머지는 사용하지 않겠다는 의미로 언더스코어(_) 변수에 할당합니다.
    quotient, _ = divmod(score, 10)
    
    # 몫을 기준으로 등급을 판별합니다. (예: 95점 -> 몫 9 -> A)
    # 100점의 경우 몫이 10이므로 9 이상에 포함되도록 >= 9 처리합니다.
    grade_map = {
        10: 'A',  # 100점
        9: 'A',
        8: 'B',
        7: 'C',
        6: 'D'
    }
    # grade_map에 없으면 'F' 반환
    return grade_map.get(quotient, 'F')


def map_subjects_to_scores(subjects: List[str], scores: List[int]) -> Dict[str, int]:
    """
    과목명 리스트와 점수 리스트를 병합하여 딕셔너리로 만듭니다.
    
    Args:
        subjects (List[str]): 과목명이 담긴 리스트
        scores (List[int]): 각 과목에 대응하는 점수 리스트
        
    Returns:
        Dict[str, int]: 과목명을 키(Key)로, 점수를 값(Value)으로 가지는 딕셔너리
    """
    if len(subjects) != len(scores):
        raise ValueError("과목 수와 점수 수가 일치하지 않아 매칭할 수 없습니다.")
        
    # zip: 두 리스트의 동일한 인덱스에 있는 요소들을 짝지어 튜플의 이터레이터로 만듭니다.
    # dict(): 생성된 (과목, 점수) 튜플 쌍들을 딕셔너리 형태로 변환합니다.
    mapped_data: Dict[str, int] = dict(zip(subjects, scores))
    return mapped_data


# --- 테스트 및 실행 코드 ---
# if __name__ == "__main__":
#     subject_list: List[str] = ["컴퓨터구조", "운영체제", "데이터베이스"]
#     score_list: List[int] = [95, 82, 78]
    
#     # 1. zip 테스트: 리스트 병합
#     student_scores = map_subjects_to_scores(subject_list, score_list)
#     print(f"매칭 결과: {student_scores}") 
#     # 출력: 매칭 결과: {'컴퓨터구조': 95, '운영체제': 82, '데이터베이스': 78}
    
#     # 2. 총점 계산
#     total_score = calculate_total(score_list)
#     print(f"총점: {total_score}점") 
#     # 출력: 총점: 255점
    
#     # 3. divmod 테스트: 학점 산출
#     print("과목별 학점:")
#     for subject, score in student_scores.items():
#         grade = determine_grade(score)
#         print(f" - {subject}: {score}점 ({grade}등급)")