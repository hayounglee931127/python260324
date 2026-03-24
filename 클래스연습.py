#클래스연습.py

#1)클래스 정의
class Person:
    #초기화 메서드
    def __init__(self):
        self.name="default name"

    def print(self):
        print("my name is {0}".format(self.name))

#객체생성
p1=Person()
p2=Person()

p1.nm="홍길동"
p1.print() 
p2.print()



