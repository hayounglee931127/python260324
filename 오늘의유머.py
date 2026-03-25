# 오늘의유머.py
#웹크롤링 선언
from bs4 import BeautifulSoup
#웹사이트 요청
import urllib.request
#정규표현식 추가
import re

#파일로저장
f = open("todayHumor.txt", "wt", encoding="utf-8")

#페이지처리
for i in range(1, 11) :
    url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page="+str(i)
    print(url)
    #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
    hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
    #아래에 headers 값을 주기위해 hdr에 실제 있는 헤더값 아무거나 넣어줘도 된다(속이기위한 목적, 크롤링을 막는 사이트가 있기 때문에)

    #웹브라우져 헤더 추가 
    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()

    #검색이 용이한 스프객체
    soup = BeautifulSoup(data, "html.parser")  
    #필요한 태그만 필터링
    lst = soup.find_all("td", attrs={"class":"subject"}) 
    for tag in lst : 
        title = tag.find("a").text.strip() 
        if re.search("한국", title) : #아이폰이 포함된 제목만 출력
            print(title)
            f.write(title + "\n")#파일에 쓰기

f.close()
# <td class="subject">
# <a href="/board/view.php?table=bestofbest&amp;no=482447&amp;s_no=482447&amp;page=2" target="_top">모르는 사람 와서 숨었는데 살짝 덜 숨은 냥이</a>
# <span class="list_memo_count_span"> [12]</span>  
# <span style="margin-left:4px;"><img src="//www.todayhumor.co.kr/board/images/list_icon_photo.gif" style="vertical-align:middle; margin-bottom:1px;"> </span> 
# </td>