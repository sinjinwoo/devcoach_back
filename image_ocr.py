from pathlib import Path
import platform
import os
from PIL import Image
import pytesseract

# =========================================
# 1️⃣ 프로젝트 루트 디렉토리 계산
# =========================================
PROJECT_ROOT = Path(__file__).resolve().parent   # 현재 .py 위치
COMPANY_DIR  = PROJECT_ROOT / "company"          # ./company 폴더

# =========================================
# 2️⃣ OCR 함수 정의
# =========================================
def perform_ocr_to_txt_auto(company_name: str) -> bool | None:
    """
    회사명을 입력받아 company/<회사명>.jpg 파일을 OCR 처리 후
    company/<회사명>_ocr.txt 에 저장합니다.

    ✅ Windows → 명시적 Tesseract 경로
    ✅ Ubuntu/Linux → 기본 경로
    ✅ 이미지가 없으면 빈 txt 생성 후 None 반환
    ✅ OCR 성공 시 True 반환

    :param company_name: 예) '(주)지아이티'  (확장자 없이)
    :return: 성공 True, 실패/없음 시 None
    """

    # 운영체제 감지 후 Tesseract 경로 설정
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        print("🪟 Windows 환경 - Tesseract 경로 설정 완료")
    else:
        print("🐧 Linux/Ubuntu 환경 - 기본 Tesseract 경로 사용")

    # ---------------- 경로 설정 ----------------
    image_path  = COMPANY_DIR / f"{company_name}.jpg"
    output_path = COMPANY_DIR / f"{company_name}_ocr.txt"

    # 이미지 존재 확인
    if not image_path.exists():
        print(f"❌ 이미지 파일 없음: {image_path}")
        with output_path.open("w", encoding="utf-8") as f:
            f.write("")            # 빈 파일 생성
        return None

    # ---------------- OCR 처리 ----------------
    try:
        image = Image.open(image_path)
        text  = pytesseract.image_to_string(image, lang="kor+eng")

        with output_path.open("w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ OCR 완료: {output_path}")
        return True

    except Exception as e:
        print(f"⚠️ OCR 실패: {e}")
        with output_path.open("w", encoding="utf-8") as f:
            f.write("")            # 오류 방지용 빈 파일
        return None
    # OCR 성공 → True, 실패/없음 → None

# =========================================
# 3️⃣ 테스트 실행
# =========================================
if __name__ == "__main__":
    # 회사명(확장자 없이) 지정
    test_company = "(주)지아이티"

    result = perform_ocr_to_txt_auto(test_company)

    if result:
        print("🎉 OCR 성공")
    else:
        print("⚠️ OCR 실패 또는 파일 없음")