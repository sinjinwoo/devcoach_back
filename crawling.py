"""
crawling.py  (★ 크롤링 로직은 요청대로 ‘그대로’ 유지)
────────────────────────────────────────────────────────
- 검색 → 채용 목록 수집
- 상세 iframe → JPG·TXT 저장

!! 수정 사항 !!
1. 프로젝트 루트(project_root) 기준 경로 전역 선언
2. JPG·TXT 저장 시 company/ 폴더 아래로 저장
   (크롤링 로직은 변경하지 않음, 단순 경로만 변경)
"""

from pathlib import Path
import requests
from bs4 import BeautifulSoup

# =====================================================
# 0️⃣  프로젝트 루트 & company 폴더 경로  (경로 관련 추가)
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent          # ─┐ 현재 .py 위치
COMPANY_DIR  = PROJECT_ROOT / "company"                 #   ├─ ./company
COMPANY_DIR.mkdir(exist_ok=True)                        #   └─ 없으면 생성

# =====================================================
# 0️⃣  공용 headers  (변경 없음)
# =====================================================
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

# =====================================================
# 1️⃣  검색 페이지에서 채용 목록 크롤링  (변경 없음)
# =====================================================
def fetch_recruitment_info(company_name):
    """
    회사명 검색 → 채용공고 리스트(list[list]) 반환
    """
    main_url = "https://www.saramin.co.kr"
    url_front = (
        "https://www.saramin.co.kr/zf_user/jobs/list/job-category"
        "?cat_mcls=2&keydownAccess=&searchType=search&searchword="
    )
    url_back = "&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y"
    url = url_front + str(company_name) + url_back

    response = requests.get(url, headers=headers)
    recruitment_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        div_common_recruilt_list = soup.find('div', attrs={"class": "common_recruilt_list"})
        div_list_body = div_common_recruilt_list.find('div', attrs={"class": "list_body"})
        div_box_item = div_list_body.find_all('div', attrs={"class", 'box_item'})
        for num in range(len(div_box_item)):
            company_data = []
            div_company_nm = div_box_item[num].find('div', attrs={"class": "company_nm"})
            company_nm = div_company_nm.find('a') or div_company_nm.find('span')  # 예외 처리

            div_notification_info = div_box_item[num].find('div', attrs={"class": "notification_info"})
            a_str_tit = div_notification_info.find('a', attrs={"class", "str_tit"})
            a_href = a_str_tit['href']

            company_group_name = company_nm.get_text(strip=True)
            company_title = a_str_tit.get_text(strip=True)
            if company_name in company_group_name:
                company_data.append(company_group_name)
                company_data.append(company_title)
                company_data.append(main_url + a_href)

                div_recruit_info = div_box_item[num].find('div', attrs={"class": "recruit_info"})
                p_class_list = div_recruit_info.find_all('p')
                for p in p_class_list:
                    company_data.append(p.get_text(strip=True))
                recruitment_data.append(company_data)
    else:
        print(f"[!] 요청 실패 - 상태 코드: {response.status_code}")

    return recruitment_data


def convert_to_recruitment_info(recruitment_data):
    """
    2차원 리스트 → dict 리스트 변환
    (원본 로직 유지, key 개수 초과분은 무시)
    """
    keys = ["name", "job", "url", "place", "career", "education"]
    recruitment_dict_list = []
    for recruitment in recruitment_data:
        recruitment_dict = {keys[i]: recruitment[i] for i in range(min(len(recruitment), len(keys)))}
        recruitment_dict_list.append(recruitment_dict)
    return recruitment_dict_list


# =====================================================
# 2️⃣  이미지 URL 보정 (변경 없음)
# =====================================================
def replace_image_url(image_url):
    main_url = "https://www.saramin.co.kr"
    if "www." in image_url:
        split_image_url = image_url.split("www.")[1]
        url = "https://www." + split_image_url
    elif "/recruit" in image_url:
        split_image_url = image_url.split("/recruit")[1]
        url = main_url + "/recruit" + split_image_url
    else:
        url = image_url  # fallback
    return url


# =====================================================
# 3️⃣  상세 페이지 크롤링 → company/ 에 저장
#     (크롤링 로직 동일, 단 저장 경로만 company/ 로 변경)
# =====================================================
def fetch_and_store_job_content(company_url, company_name):
    main_url = "https://www.saramin.co.kr"
    company_number = company_url.split("rec_idx=")[1].split("&")[0]
    iframe_url = f"{main_url}/zf_user/jobs/relay/view-detail?rec_idx={company_number}&amp;rec_seq=0"

    response = requests.get(iframe_url, headers=headers)
    if response.status_code != 200:
        print(f"[!] 요청 실패 - 상태 코드: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # ------------ 이미지 저장 ------------
    img = soup.find("img")
    if img and img.has_attr("src"):
        img_url = replace_image_url(img["src"])
        try:
            img_response = requests.get(img_url, headers=headers)
            if img_response.status_code == 200:
                img_path = COMPANY_DIR / f"{company_name}.jpg"           # ← company/ 경로
                with img_path.open("wb") as img_file:
                    img_file.write(img_response.content)
                print(f"[✔] 이미지 저장 완료: {img_path.name}")
            else:
                print(f"[!] 이미지 요청 실패 - 상태 코드: {img_response.status_code}")
        except Exception as e:
            print(f"[!] 이미지 다운로드 오류: {e}")

    # ------------ 텍스트 저장 ------------
    td_tags = soup.find_all("td")
    txt_path = COMPANY_DIR / f"{company_name}.txt"                      # ← company/ 경로
    with txt_path.open("w", encoding="utf-8") as f:
        for td in td_tags:
            text = td.get_text(strip=True)
            f.write(text + "\n" if text else " ")

    print(f"[✔] 텍스트 저장 완료: {txt_path.name}")


# =====================================================
# 4️⃣  간단 테스트 (크롤링 로직 변경 없음)
# =====================================================
if __name__ == "__main__":
    target_company = "지아이티"
    raw_list = fetch_recruitment_info(target_company)
    dict_list = convert_to_recruitment_info(raw_list)

    if dict_list:
        info = dict_list[0]  # 첫 번째 공고로 테스트
        print(f"▶ 상세 페이지: {info['url']}")
        fetch_and_store_job_content(info["url"], info["name"])
    else:
        print("❌ 검색 결과 없음")