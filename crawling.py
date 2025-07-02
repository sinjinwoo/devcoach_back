import requests
from bs4 import BeautifulSoup

#### 전역에 정의 ####
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


#### 함수 정의 ####
def fetch_recruitment_info(company_name):
    main_url = "https://www.saramin.co.kr"
    url_searchword_front = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_mcls=2&keydownAccess=&searchType=search&searchword="
    url_searchword_back = "&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y"
    url = url_searchword_front + str(company_name) + url_searchword_back
    response = requests.get(url, headers=headers)
    recruitment_data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        div_common_recruilt_list = soup.find('div',attrs ={"class" : "common_recruilt_list"})
        div_list_body = div_common_recruilt_list.find('div', attrs={"class" : "list_body"})
        div_box_item = div_list_body.find_all('div', attrs={"class", 'box_item'})
        for num in range(0,len(div_box_item),1):
            company_data = []
            div_company_nm = div_box_item[num].find('div', attrs = {"class" : "company_nm"})
            company_nm = div_company_nm.find('a')
            if(company_nm  == None):
                ### 예외처리
                company_nm = div_company_nm.find('span')
                
            div_notification_info = div_box_item[num].find('div', attrs = {"class" :"notification_info"})
            a_str_tit = div_notification_info.find('a', attrs = {"class", "str_tit"})
            a_href = a_str_tit['href']

            company_group_name = company_nm.get_text(strip=True)
            company_title = a_str_tit.get_text(strip=True)
            if (company_name in company_group_name):
                company_data.append(company_group_name)
                company_data.append(company_title)
                a_url = main_url + a_href
                company_data.append(a_url)
                
                div_recruit_info = div_box_item[num].find('div', attrs = {"class" : "recruit_info"})
                p_class_list = div_recruit_info.find_all('p')
                for p_num in range(0,len(p_class_list),1):
                    company_data.append(p_class_list[p_num].get_text(strip=True))
                recruitment_data.append(company_data)
    else:
        print(f"[!] 요청 실패 - 상태 코드: {response.status_code}")
    
    return recruitment_data

def convert_to_recruitment_info(recruitment_data):
    # 딕셔너리 형태로 변환할 필드명
    keys = ["name", "job", "url", "place", "career", "education"]
    
    # 리스트 안의 각 항목을 딕셔너리로 변환
    recruitment_dict_list = []
    for recruitment in recruitment_data:
        recruitment_dict = {keys[i]: recruitment[i] for i in range(len(recruitment))}
        recruitment_dict_list.append(recruitment_dict)
    
    return recruitment_dict_list

def replace_image_url(image_url):
    ### https://www.saraminimage.co.kr/recruit/os_hk_25/09_shinhan_img_250623.png
    ### //www.saraminimage.co.kr/recruit/os_hk_25/08_sinhan_img_250626.png
    main_url = "https://www.saramin.co.kr"
    if ("www." in image_url):
        split_image_url = image_url.split("www.")[1]
        url = "https://www." + split_image_url
    elif ("/recruit" in image_url):
        split_image_url = image_url.split("/recruit")[1]
        url = main_url + "/recruit" + split_image_url
    else:
        url = image_url ### 에러임!
    return url

def find_iframe_url(company_url, company_name):
    main_url = "https://www.saramin.co.kr"
    company_number = company_url.split("rec_idx=")[1].split("&")[0]
    
    iframe_url_front = "/zf_user/jobs/relay/view-detail?rec_idx="
    iframe_url_back = "&amp;rec_seq=0"
    
    url = main_url + iframe_url_front + company_number + iframe_url_back
    response = requests.get(url, headers=headers)
    result_text = ""
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        img = soup.find("img")
        if img is not None and img.has_attr("src"):
            img_src = img["src"]
            img_url = replace_image_url(img_src)
            try:
                img_response = requests.get(img_url, headers=headers)
                if img_response.status_code == 200:
                    with open(f"{company_name}.jpg", "wb") as img_file:
                        img_file.write(img_response.content)
                        print(f"[✔] 이미지 저장 완료: {company_name}.jpg")
                else:
                    print(f"[!] 이미지 요청 실패 - 상태 코드: {img_response.status_code}")
            except Exception as e:
                print(f"[!] 이미지 다운로드 오류: {e}")

        td = soup.find_all("td")
        with open(f"{company_name}.txt", "w", encoding="utf-8") as f:
            for i in range(0,len(td),1):
                b = td[i].get_text(strip=True)
                if(len(b) == 0):
                    continue
                f.write(b + "\n")
    else:
        print(f"[!] 요청 실패 - 상태 코드: {response.status_code}")


#### 실행 테스트 ####
#### 2025.07.02 14:03 완성 ####
data = fetch_recruitment_info("신한은행")
a = convert_to_recruitment_info(data)
print(a)
find_iframe_url(a[1]['url'], a[1]['name'])