#db2.py
import sqlite3

#영구적으로 파일에 저장(raw string notation)
con = sqlite3.connect(r"c:\work\sample2.db")

#커서객체 리턴
cur = con.cursor()  
#테이블 생성
# cur.execute("create table PhoneBook(Name text, PhoneNumber text);")
#데이터 삽입
cur.execute("insert into PhoneBook values('홍길동', '010-1234-5678');")

#매개변수로 입력
name='김철수'
phone='010-9876-5432'
cur.execute("insert into PhoneBook values(?, ?);", (name, phone))   

#다중 데이터를 입력
datalist = (('박영희', '010-1111-2222'), ('이민수', '010-3333-4444'))
cur.executemany("insert into PhoneBook values(?, ?);", datalist)

#데이터 조회
for row in cur.execute("select * from PhoneBook;"):
    print(row)

#변경사항 저장
con.commit()  

#연결종료
con.close()