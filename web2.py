# web2.py
#웹크롤링 선언
from bs4 import BeautifulSoup
#웹사이트 요청
import urllib.request
#정규표현식 추가
import re

#파일로저장
f = open("clien.txt", "wt", encoding="utf-8")

#페이지처리
for i in range(0, 10) :
    url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po="+str(i)
    print(url)
    #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
    hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
    #아래에 headers 값을 주기위해 hdr에 실제 있는 헤더값 아무거나 넣어줘도 된다(속이기위한 목적, 크롤링을 막는 사이트가 있기 때문에)

    #웹브라우져 헤더 추가 
    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()

    #검색이 용이한 스프객체
    soup = BeautifulSoup(data, "html.parser")  

    lst = soup.find_all("span", attrs={"data-role":"list-title-text"}) 
    for tag in lst : 
        title = tag.text.strip() 
        if re.search("아이폰", title) : #아이폰이 포함된 제목만 출력
            print(title)
            f.write(title + "\n")#파일에 쓰기

f.close()
# <span class="subject_fixed" data-role="list-title-text" title="갤럭시s26울트라 정품 케이스 판매합니다. (슬림마그넷, 미러마그넷 2개)">
#    갤럭시s26울트라 정품 케이스 판매합니다. (슬림마그넷, 미러마그넷 2개)
# </span>