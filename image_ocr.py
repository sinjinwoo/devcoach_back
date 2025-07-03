from pathlib import Path
import platform
import os
from PIL import Image
import pytesseract

# =========================================
# 1️⃣ 프로젝트 루트 디렉토리 계산
# =========================================
# 현재 .py 파일이 위치한 디렉토리 기준으로 프로젝트 루트 결정
PROJECT_ROOT = Path(__file__).resolve().parent
# company 폴더 경로
COMPANY_DIR = PROJECT_ROOT / "company"
# =========================================
# 2️⃣ OCR 함수 정의
# =========================================
def perform_ocr_to_txt_auto(filename: str) -> bool | None:
    """
    OS에 따라 Tesseract 경로를 자동 설정한 뒤
    company/ 폴더 안에 존재하는 이미지 파일을 OCR 처리하여
    company/ 폴더 안에 결과 txt 파일로 저장합니다.

    ✅ Windows → 명시적 경로
    ✅ Ubuntu/Linux → 기본 경로
    ✅ 이미지가 없으면 빈 txt 생성 후 None 반환
    ✅ OCR 성공 시 True 반환

    :param filename: 이미지 파일명 (예: '(주)지아이티.jpg')
    :return: 성공시 True, 실패/없음 시 None
    """

    # =========================================
    # 운영체제 감지 후 Tesseract 경로 설정
    # =========================================
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        print("🪟 Windows 환경 - Tesseract 경로 설정 완료")
    else:
        # Ubuntu 기본 경로
        print("🐧 Linux/Ubuntu 환경 - 기본 Tesseract 경로 사용")

    # =========================================
    # 경로 설정: company/ 폴더 기준
    # =========================================
    image_path = COMPANY_DIR / filename
    base_name = image_path.stem  # 확장자 없는 파일명
    output_path = COMPANY_DIR / f"{base_name}_ocr.txt"

    # =========================================
    # 이미지 파일 존재 여부 확인
    # =========================================
    if not image_path.exists():
        print(f"❌ 이미지 파일 없음: {image_path}")
        with output_path.open("w", encoding="utf-8") as f:
            f.write("")  # 빈 파일 생성
        return None

    # =========================================
    # OCR 처리
    # =========================================
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang="kor+eng")
        with output_path.open("w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ OCR 완료: {output_path}")
        return True
    except Exception as e:
        print(f"⚠️ OCR 실패: {e}")
        with output_path.open("w", encoding="utf-8") as f:
            f.write("")  # 오류 방지를 위해 빈 파일 생성
        return None
    ### OCR 변환 성공시 True 리턴
    ### OCR 변환 실패시 None 리턴, 빈 파일 생성 (오류 방지용)

# ocr_result = perform_ocr_to_txt_auto("(주)지아이티.jpg", image_dir="./", output_dir="./")
# =========================================
# 3️⃣ 테스트 실행
# =========================================
if __name__ == "__main__":
    # 테스트 파일명 지정
    test_filename = "(주)지아이티.jpg"

    result = perform_ocr_to_txt_auto(test_filename)

    if result:
        print("🎉 OCR 성공")
    else:
        print("⚠️ OCR 실패 또는 파일 없음")