#db1.py
import sqlite3

#메모리에 임시로 저장
con = sqlite3.Connection(":memory:")

#커서객체 리턴
cur = con.cursor()  
#테이블 생성
cur.execute("create table PhoneBook(Name text, PhoneNumber text);")
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
# for row in cur.execute("select * from PhoneBook;"):
#     print(row)
cur.execute("select * from PhoneBook;")  #쿼리문 실행(버퍼에 결과 임시저장)
print('*******fetchone********')
print(cur.fetchone())  #한 행만 가져오기
print('*******fetchmany********')   
print(cur.fetchmany(2))  #두 행 가져오기
print('*******fetchall********')   
print(cur.fetchall())  #모든 행 가져오기지만 위에서 순차적으로  fetchone, fetchmany로 버퍼에서 가져온 행은 제외하고 가져오기 때문에 결과는 나머지 1개만 나옴
                       #버퍼 포인트 이동

cur.execute("select * from PhoneBook;") #버퍼에 결과 다시 채움
print(cur.fetchall()) 

#연결종료
con.close()