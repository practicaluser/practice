# main.py

import sys
from typing import Optional

# 우리가 만든 모듈들 임포트
from student_models import Student, GraduateStudent, print_student_info
from student_registry import StudentRegistry
import score_validator
import persistence_manager

DB_FILE_PICKLE = "student_data.pkl"
REPORT_FILE_EXCEL = "student_report.xlsx"

def find_student_by_id(registry: StudentRegistry, student_id: str) -> Optional[Student]:
    """학번으로 레지스트리에서 학생 객체를 찾아 반환하는 헬퍼 함수"""
    for student in registry.students:
        if student.student_id == student_id:
            return student
    return None

def main():
    # 1. 시스템 초기화: 학생 레지스트리 생성
    registry = StudentRegistry()
    
    # 2. 시작 시 기존 데이터가 있다면 불러오기 (Pickle 활용)
    print("시스템을 초기화합니다...")
    loaded_data = persistence_manager.load_from_pickle(DB_FILE_PICKLE)
    
    if loaded_data is not None:
        # 불러온 데이터가 객체 리스트인지, 단순 딕셔너리 리스트인지 확인하여 처리합니다.
        processed_students = []
        for item in loaded_data:
            # 만약 아이템이 딕셔너리라면 (AttributeError의 원인)
            # 단순 데이터(제원표)를 클래스의 생성자를 통해 메모리상의 '인스턴스'로 다시 조립합니다.
            if isinstance(item, dict):
                # 키 이름 방어적 처리 (이전 테스트 데이터 호환)
                name = item.get('name', item.get('이름', '이름없음'))
                s_id = item.get('student_id', item.get('학번', '학번없음'))
                
                # 대학원생 고유 속성(논문 주제)이 있는지 확인하여 다형성 복원
                if "thesis_topic" in item or "논문주제" in item:
                    topic = item.get("thesis_topic") or item.get("논문주제", "")
                    s = GraduateStudent(name, s_id, topic)
                else:
                    s = Student(name, s_id)
                
                # 성적 데이터 복구
                if 'scores' in item:
                    scores_data = item['scores']
                    if isinstance(scores_data, dict):
                        # {과목: 점수} 형태인 경우 안전하게 검증 메서드를 태워 복원
                        for subject, score in scores_data.items():
                            s.add_score(subject, score)
                    elif isinstance(scores_data, list):
                        # 초기 테스트용 데이터([10, 20, 30]) 형태인 경우 임의 과목명으로 복원
                        for idx, score in enumerate(scores_data):
                            s.add_score(f"임시과목{idx+1}", score)

                processed_students.append(s)
            else:
                # 이미 파이썬 객체(Student/GraduateStudent 인스턴스) 형태라면 그대로 추가
                processed_students.append(item)
        
        registry.students = processed_students
        # 데이터 로드 후, 다음 번호 부여를 위해 클래스 변수 업데이트
        Student.total_students = len(registry.students)

    while True:
        print("\n" + "="*40)
        print(" 🗂️ 학생 성적 관리 시스템 메인 메뉴")
        print("="*40)
        print("1. 학생 등록 (학부생/대학원생)")
        print("2. 과목 성적 입력")
        print("3. 학생 전체 랭킹 및 상세 정보 조회")
        print("4. 시스템 데이터 저장 (Pickle - 복원용)")
        print("5. 엑셀 리포트 추출 (Excel - 보고용)")
        print("0. 프로그램 종료")
        print("="*40)
        
        choice = input("원하는 작업의 번호를 입력하세요: ")

        if choice == '1':
            print("\n[학생 등록]")
            s_type = input("1: 학부생, 2: 대학원생 선택: ")
            name = input("이름: ")
            s_id = input("학번: ")
            
            if find_student_by_id(registry, s_id):
                print("❌ 오류: 이미 존재하는 학번입니다.")
                continue

            if s_type == '1':
                student = Student(name, s_id)
                registry.add_student(student)
                print(f"✅ {name} 학부생이 등록되었습니다.")
            elif s_type == '2':
                topic = input("논문 주제: ")
                student = GraduateStudent(name, s_id, topic)
                registry.add_student(student)
                print(f"✅ {name} 대학원생이 등록되었습니다.")
            else:
                print("❌ 오류: 잘못된 선택입니다.")

        elif choice == '2':
            print("\n[성적 입력]")
            s_id = input("성적을 입력할 학생의 학번: ")
            student = find_student_by_id(registry, s_id)
            
            if not student:
                print("❌ 오류: 해당 학번의 학생을 찾을 수 없습니다.")
                continue
                
            subject = input("과목명: ")
            try:
                score = int(input("점수 (0~100): "))
                # Student 객체 내부에서 자동으로 score_validator를 호출하여 검증
                student.add_score(subject, score)
                print(f"✅ [{subject}] 과목 성적이 정상적으로 입력되었습니다.")
            except ValueError:
                print("❌ 오류: 점수는 숫자로 입력해야 합니다.")
            except score_validator.InvalidScoreError as e:
                print(f"❌ 데이터 검증 실패: {e}")

        elif choice == '3':
            if not registry.students:
                print("\n⚠️ 등록된 학생 데이터가 없습니다.")
                continue
                
            registry.print_rankings()
            
            print("\n--- 상세 정보 ---")
            for student in registry.students:
                print_student_info(student)

        elif choice == '4':
            print("\n[데이터 저장]")
            if persistence_manager.save_to_pickle(registry.students, DB_FILE_PICKLE):
                print("✅ 시스템 데이터가 안전하게 보관되었습니다.")

        elif choice == '5':
            print("\n[엑셀 리포트 추출]")
            if not registry.students:
                print("⚠️ 저장할 데이터가 없습니다.")
                continue
            
            report_data = []
            for s in registry.students:
                report_data.append({
                    "학번": s.student_id,
                    "이름": s.name,
                    "구분": "대학원생" if isinstance(s, GraduateStudent) else "학부생",
                    "총점": s.get_total_score(),
                    "졸업가능여부": "통과" if s.check_graduation_eligibility() else "미달"
                })
            
            persistence_manager.save_to_excel(report_data, REPORT_FILE_EXCEL)

        elif choice == '0':
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            auto_save = input("종료 전 데이터를 저장하시겠습니까? (y/n): ")
            if auto_save.lower() == 'y':
                persistence_manager.save_to_pickle(registry.students, DB_FILE_PICKLE)
            sys.exit()

        else:
            print("❌ 잘못된 입력입니다. 0~5 사이의 번호를 선택해주세요.")

if __name__ == "__main__":
    main()