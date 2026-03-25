#web1.py
from bs4 import BeautifulSoup
#from은 폴더명을 생략

#페이지를 로딩
#rt=read text, rb=read binary, 기본값이 rt 이기때문에 생략해도 무방, 하지만 명시적으로 작성하는 것이 좋음
page = open("Chap09_test.html", "rt", encoding="utf-8").read() 

#전체 페이지를 BeautifulSoup 객체로 변환
soup = BeautifulSoup(page, "html.parser") 

#전체보기
# print(soup.prettify())

# #<p>를 몽땅 검색하기
# print(soup.find_all("p"))

# 첫번째 <p>태그 검색하기
# print(soup.find("p"))

#조건검색 : <p> 태그 중에서 class 속성이 "outer-text"인 것 검색하기
# print(soup.find_all("p", class_="outer-text")) #class_의 언더바를 붙이는 이유 #class는 파이썬에서 예약어이기 때문에 언더바를 붙여서 구분한다. 
#class는 변수명으로 쓰면 안된다~

#조건검색 : attrs 속성으로 검색하기
# print(soup.find_all("p", attrs={"class":"outer-text"})) #attrs는 속성이라는 뜻, 딕셔너리 형태로 검색할 수 있다.

#id검색:id=first
# print(soup.find_all(id="first")) #id는 고유한 값이기 때문에 find_all이 아니라 find를 사용하는 것이 좋다.

#태그 내부의 문자열 : .text
# for tag in soup.find_all("p"):
#     title = tag.text.strip() #strip은 문자열의 양쪽 공백을 제거하는 함수
#     title = title.replace("\n", "") #\n은 줄바꿈 문자, replace는 문자열을 대체하는 함수
#     print(title)

#문자열처리 메서드와 정규표현식
strA = "<<< python >>>"
result = strA.strip("<>") #strip은 문자열의 양쪽에서 지정한 문자를 제거하는 함수, 여기서는 <와 >를 제거한다.
print(result)
strB = strA.replace("python", "python javascript") #replace는 문자열을 대체하는 함수, 여기서는 python을 java로 대체한다.
print(strB)
result = "spam ham egg banana".split() #split은 문자열을 지정한 구분자로 나누는 함수, 기본값이 공백이다.
print(result)  
print(":)".join(result)) #join은 문자열을 지정한 구분자로 연결하는 함수, 여기서는 :로 연결한다. 

#정규표현식: 특정한 패턴(규칙)문자열
import re

result = re.search(r"\d{4}", "올해는 2026년입니다.") #\d는 숫자(digit)를 의미, {4}는 4자리 숫자를 의미, search는 문자열에서 패턴을 검색하는 함수
print(result.group()) #group은 검색된 패턴을 반환하는 함수

result = re.search("apple", 'this is a apple.') #문자열에서 apple을 검색하는 함수
print(result.group()) #group은 검색된 패턴을 반환하는 함수
