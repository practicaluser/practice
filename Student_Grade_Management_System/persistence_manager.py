# persistence_manager.py

import pickle
import os
import pandas as pd  # 엑셀 처리를 위한 라이브러리
from typing import Any, Optional, List, Dict

# --- 1. Pickle을 이용한 객체 직렬화 (기존 기능) ---

def save_to_pickle(data: Any, filename: str) -> bool:
    """객체 구조 전체를 이진 파일로 저장합니다."""
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        print(f"✅ [Pickle] 데이터가 '{filename}'에 저장되었습니다.")
        return True
    except Exception as e:
        print(f"❌ [Pickle] 저장 오류: {e}")
        return False

def load_from_pickle(filename: str) -> Optional[Any]:
    """이진 파일로부터 객체를 복원합니다."""
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"⚠️ [Pickle] '{filename}' 파일이 없습니다.")
        return None
    except (pickle.UnpicklingError, EOFError):
        print(f"❌ [Pickle] 데이터가 손상되었습니다.")
        return None


# --- 2. Pandas를 이용한 엑셀(Excel) 저장 및 로드 (추가 기능) ---

def save_to_excel(data_list: List[Dict[str, Any]], filename: str) -> bool:
    """
    딕셔너리 리스트 형태의 데이터를 엑셀 파일로 저장합니다.
    
    Args:
        data_list: [{'이름': '홍길동', '총점': 90}, ...] 형태의 데이터
        filename: 저장할 파일명 (예: 'results.xlsx')
    """
    try:
        # 데이터프레임 생성: 리스트 내의 딕셔너리 키들이 엑셀의 헤더(열 이름)가 됩니다.
        df = pd.DataFrame(data_list)
        # 엑셀 파일로 추출 (index=False: 행 번호 제외)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✅ [Excel] 데이터가 '{filename}'에 저장되었습니다.")
        return True
    except Exception as e:
        print(f"❌ [Excel] 저장 오류: {e}")
        return False

def load_from_excel(filename: str) -> Optional[List[Dict[str, Any]]]:
    """
    엑셀 파일을 읽어 딕셔너리 리스트 형태로 반환합니다.
    """
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(filename, engine='openpyxl')
        # 데이터프레임을 딕셔너리 리스트로 변환 ('records' 방식)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"⚠️ [Excel] '{filename}' 파일이 없습니다.")
        return None
    except Exception as e:
        print(f"❌ [Excel] 로드 오류: {e}")
        return None


# --- 테스트 및 실행 코드 ---
if __name__ == "__main__":
    # 테스트용 데이터 (학생 정보 딕셔너리 리스트)
    # 실제 시스템에서는 student_registry에서 추출한 튜플이나 딕셔너리를 사용하게 됩니다.
    sample_data = [
        {"학번": "U2026001", "이름": "김철수", "총점": 175, "졸업여부": "Pass"},
        {"학번": "U2026002", "이름": "이영희", "총점": 195, "졸업여부": "Pass"},
        {"학번": "G2026001", "이름": "박지민", "총점": 170, "졸업여부": "Fail"}
    ]
    
    excel_file = "student_report.xlsx"
    pickle_file = "student_objects.pkl"

    print("--- 엑셀 기능 테스트 ---")
    if save_to_excel(sample_data, excel_file):
        loaded_excel = load_from_excel(excel_file)
        print(f"불러온 엑셀 데이터: {loaded_excel}")

    print("\n--- Pickle 기능 테스트 ---")
    if save_to_pickle(sample_data, pickle_file):
        loaded_pickle = load_from_pickle(pickle_file)
        print(f"불러온 Pickle 데이터: {loaded_pickle}")