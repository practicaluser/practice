# student_models.py

from typing import Dict, Set, List
import score_validator
import grade_calculator

class Student:
    """
    학부생(기본) 클래스: 학생의 상태(데이터)와 행동(메서드)을 정의합니다.
    """
    
    # 클래스 변수: 인스턴스가 아닌 클래스 자체에 속하며, 생성된 전체 학생 수를 추적합니다.
    total_students: int = 0
    
    def __init__(self, name: str, student_id: str) -> None:
        """생성자: 학생 객체가 생성될 때 초기 상태를 설정합니다."""
        self.name: str = name
        self.student_id: str = student_id
        
        # 자료형 (딕셔너리): 과목명을 키로, 점수를 값으로 관리
        self.scores: Dict[str, int] = {}
        # 자료형 (집합 - Set): 수강한 고유 과목 목록 관리 (중복 제거 보장)
        self.subjects: Set[str] = set()
        
        # 객체가 생성될 때마다 클래스 변수를 1씩 증가시킵니다.
        Student.total_students += 1
        
    def add_score(self, subject: str, score: int) -> None:
        """단일 과목의 성적을 추가합니다."""
        # 1. 외부 모듈(score_validator)을 호출하여 점수 유효성 검사
        score_validator.validate_subject_scores({subject: score})
        
        # 2. 상태(데이터) 업데이트
        self.scores[subject] = score
        self.subjects.add(subject)

    def get_total_score(self) -> int:
        """외부 모듈(grade_calculator)을 사용하여 총점을 반환합니다."""
        score_list: List[int] = list(self.scores.values())
        return grade_calculator.calculate_total(score_list)
        
    def check_graduation_eligibility(self) -> bool:
        """
        [학부생 졸업 기준] 모든 수강 과목의 평균이 70점 이상이어야 합니다.
        (이 메서드는 하위 클래스에서 오버라이딩 됩니다.)
        """
        if not self.scores:
            return False
        
        total: int = self.get_total_score()
        average: float = total / len(self.scores)
        return average >= 70

    def get_grades(self) -> Dict[str, str]:
        """각 과목별 학점 등급(A, B, C...)을 산출하여 반환합니다."""
        return {
            subject: grade_calculator.determine_grade(score) 
            for subject, score in self.scores.items()
        }


class GraduateStudent(Student):
    """
    대학원생 클래스: Student 클래스를 '상속'받아 고유 속성과 더 엄격한 기준을 적용합니다.
    """
    
    def __init__(self, name: str, student_id: str, thesis_topic: str) -> None:
        # super()를 통해 부모 클래스(Student)의 생성자를 호출하여 기본 속성을 초기화합니다.
        super().__init__(name, student_id)
        # 대학원생만의 고유 상태(논문 주제) 추가
        self.thesis_topic: str = thesis_topic
        
    # 메서드 오버라이딩 (Method Overriding)
    def check_graduation_eligibility(self) -> bool:
        """
        [대학원생 졸업 기준] 부모 클래스의 메서드를 덮어쓰고 새로운 로직을 적용합니다.
        기준: 평균 80점 이상 및 논문 주제가 등록되어 있어야 함.
        """
        if not self.scores or not self.thesis_topic:
            return False
            
        total: int = self.get_total_score()
        average: float = total / len(self.scores)
        return average >= 80


def print_student_info(student: Student) -> None:
    """
    isinstance를 활용하여 객체 타입에 따라 분기 처리를 수행하는 헬퍼 함수입니다.
    """
    print(f"[{student.student_id}] {student.name} 학생 정보")
    
    # 내장함수 isinstance: 해당 객체가 특정 클래스(또는 그 하위 클래스)의 인스턴스인지 확인
    if isinstance(student, GraduateStudent):
        print(f" 🎓 구분: 대학원생 (논문: {student.thesis_topic})")
    else:
        print(" 🎒 구분: 학부생")
        
    print(f" - 수강 과목: {', '.join(student.subjects)}")
    print(f" - 과목별 성적 및 등급: {student.get_grades()}")
    print(f" - 총점: {student.get_total_score()}점")
    
    is_eligible = student.check_graduation_eligibility()
    print(f" - 졸업 가능 여부: {'✅ 통과' if is_eligible else '❌ 미달'}\n")


# --- 테스트 및 실행 코드 ---
# if __name__ == "__main__":
#     # 객체 생성
#     undergrad = Student("김철수", "U2026001")
#     grad = GraduateStudent("이영희", "G2026001", "AI 기반 최적화 알고리즘")
    
#     # 검증 모듈을 거쳐 성적 추가 (0~100점 범위가 아니면 여기서 예외 발생)
#     undergrad.add_score("컴퓨터구조", 75)
#     undergrad.add_score("운영체제", 65)  # 평균 70점
    
#     grad.add_score("고급데이터베이스", 85)
#     grad.add_score("분산시스템", 72)     # 평균 78.5점 (대학원생 기준 80점 미달)
    
#     # isinstance 로직이 포함된 함수 실행
#     print_student_info(undergrad)
#     print_student_info(grad)
    
#     # 클래스 변수 확인
#     print(f"시스템에 등록된 총 학생 수: {Student.total_students}명")