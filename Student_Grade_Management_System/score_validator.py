from typing import List, Dict

# 1. 사용자 정의 예외 클래스
class InvalidScoreError(Exception):
    """점수가 허용된 범위(0~100)를 벗어났을 때 발생하는 예외입니다."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


# 2. 리스트 형태의 성적 검증 로직
def validate_score_list(scores: List[int]) -> bool:
    """
    입력된 점수 리스트가 모두 0~100점 사이인지 검증합니다.
    
    Args:
        scores (List[int]): 검증할 점수들이 담긴 리스트
        
    Returns:
        bool: 모든 점수가 유효 범위 내에 있으면 True
        
    Raises:
        InvalidScoreError: 범위를 벗어난 점수가 하나라도 있을 경우 발생
    """
    # any(): 제너레이터 표현식을 순회하며 하나라도 True면 즉시 True를 반환(단축 평가)
    # 0점 미만이거나 100점을 초과하는 비정상 데이터가 '하나라도' 있는지 확인합니다.
    if any(score < 0 or score > 100 for score in scores):
        raise InvalidScoreError("입력된 점수 중 0~100 범위를 벗어난 값이 존재합니다.")
    
    # all(): 제너레이터 표현식을 순회하며 모두 True여야 True를 반환
    # 위에서 예외가 발생하지 않았다면 로직상 모두 정상 범위이겠지만, 
    # all()의 명시적 활용을 위해 모든 점수가 0 이상 100 이하인지 최종 확인 후 반환합니다.
    is_valid: bool = all(0 <= score <= 100 for score in scores)
    
    return is_valid


# 3. 딕셔너리 형태의 성적 검증 로직 (과목명: 점수)
def validate_subject_scores(subject_scores: Dict[str, int]) -> bool:
    """
    과목명과 점수가 매핑된 딕셔너리 데이터의 점수 유효성을 검증합니다.
    
    Args:
        subject_scores (Dict[str, int]): 과목명을 키로, 점수를 값으로 가지는 딕셔너리
        
    Returns:
        bool: 모든 과목의 점수가 유효 범위 내에 있으면 True
        
    Raises:
        InvalidScoreError: 범위를 벗어난 점수가 있을 경우 해당 과목명을 포함하여 예외 발생
    """
    scores: List[int] = list(subject_scores.values())
    
    # any()를 활용해 비정상 점수 감지
    if any(score < 0 or score > 100 for score in scores):
        # 어떤 과목의 점수가 잘못되었는지 추적하여 에러 메시지에 포함시킵니다.
        invalid_subjects: List[str] = [
            subject for subject, score in subject_scores.items() 
            if score < 0 or score > 100
        ]
        raise InvalidScoreError(f"잘못된 점수가 입력된 과목이 있습니다: {', '.join(invalid_subjects)}")
        
    return all(0 <= score <= 100 for score in scores)


# --- 테스트 및 실행 코드 ---
# if __name__ == "__main__":
#     # 테스트 1: 정상적인 점수 리스트 검증
#     valid_scores: List[int] = [85, 90, 100, 75]
#     print(f"정상 점수 리스트 검증 결과: {validate_score_list(valid_scores)}")  # True 출력
    
#     # 테스트 2: 예외가 발생하는 딕셔너리 검증
#     invalid_dict: Dict[str, int] = {"국어": 95, "수학": -10, "영어": 105}
    
#     try:
#         validate_subject_scores(invalid_dict)
#     except InvalidScoreError as e:
#         # 사용자 정의 예외가 정상적으로 발생하여 메시지를 출력합니다.
#         print(f"예외 발생 테스트: {e}")