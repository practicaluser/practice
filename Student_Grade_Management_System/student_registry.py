# student_registry.py

import operator
from typing import List, Tuple
from student_models import Student, GraduateStudent

class StudentRegistry:
    """
    여러 학생 객체를 리스트로 보관하고 전체 목록을 관리하는 레지스트리 클래스입니다.
    """
    
    def __init__(self) -> None:
        # 자료형 (리스트): 학생 객체들을 담아둘 빈 리스트 초기화
        self.students: List[Student] = []

    def add_student(self, student: Student) -> None:
        """레지스트리에 학생 객체를 추가합니다."""
        self.students.append(student)

    def get_summary_tuples(self) -> List[Tuple[str, int, str]]:
        """
        학생 데이터 중 정렬과 출력에 필요한 데이터만 추출하여 튜플 리스트로 반환합니다.
        
        Returns:
            List[Tuple[str, int, str]]: (이름, 총점, 학번) 형태의 튜플 리스트
        """
        # 자료형 (튜플): 객체의 여러 속성 중 필요한 것만 묶어서 (이름, 총점, 학번) 튜플로 생성
        return [
            (student.name, student.get_total_score(), student.student_id) 
            for student in self.students
        ]

    def get_sorted_rankings(self) -> List[Tuple[str, int, str]]:
        """
        학생들의 총점을 기준으로 내림차순 정렬된 튜플 리스트를 반환합니다.
        """
        summary_data = self.get_summary_tuples()
        
        # 표준라이브러리 operator.itemgetter: 
        # summary_data의 각 요소(튜플)에서 1번 인덱스(총점) 값을 가져와 정렬의 기준(key)으로 삼습니다.
        # reverse=True를 통해 가장 높은 점수가 먼저 오도록 내림차순 정렬합니다.
        sorted_data = sorted(summary_data, key=operator.itemgetter(1), reverse=True)
        return sorted_data

    def print_rankings(self) -> None:
        """
        정렬된 학생 목록을 1등부터 순위를 매겨 보기 좋게 출력합니다.
        """
        sorted_rankings = self.get_sorted_rankings()
        print("="*30)
        print("🏆 학생 성적 순위 및 요약 🏆")
        print("="*30)
        
        # 내장함수 enumerate: 순회 가능한 데이터의 인덱스와 값을 함께 반환합니다.
        # start=1 파라미터를 주어 0이 아닌 1등부터 시작하도록 설정합니다.
        for rank, student_info in enumerate(sorted_rankings, start=1):
            # 언패킹을 통해 튜플 데이터를 개별 변수로 분리
            name, total_score, student_id = student_info
            print(f"{rank}등: {name} ({student_id}) - 총점: {total_score}점")


# --- 테스트 및 실행 코드 ---
# if __name__ == "__main__":
#     # 1. 레지스트리 생성
#     registry = StudentRegistry()
    
#     # 2. 더미 데이터(학생 객체) 생성 및 점수 입력
#     s1 = Student("김철수", "U2026001")
#     s1.add_score("컴퓨터구조", 85)
#     s1.add_score("운영체제", 90)  # 총점 175
    
#     s2 = Student("이영희", "U2026002")
#     s2.add_score("컴퓨터구조", 95)
#     s2.add_score("운영체제", 100) # 총점 195
    
#     s3 = GraduateStudent("박지민", "G2026001", "데이터베이스 엔진 최적화")
#     s3.add_score("고급데이터베이스", 88)
#     s3.add_score("분산시스템", 82) # 총점 170
    
#     # 3. 레지스트리에 학생 등록
#     registry.add_student(s1)
#     registry.add_student(s2)
#     registry.add_student(s3)
    
#     # 4. 순위 출력 실행 (정렬 및 enumerate 테스트)
#     registry.print_rankings()