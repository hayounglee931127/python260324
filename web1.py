#web1.py
from bs4 import BeautifulSoup
#from은 폴더명을 생략

#페이지를 로딩
#rt=read text, rb=read binary, 기본값이 rt 이기때문에 생략해도 무방, 하지만 명시적으로 작성하는 것이 좋음
page = open("Chap09_test.html", "rt", encoding="utf-8").read() 
#전체 페이지를 BeautifulSoup 객체로 변환
soup = BeautifulSoup(page, "html.parser")   
#전체보기
print(soup.prettify())
#<p>를 몽땅 검색하기
print(soup.find_all("p"))
