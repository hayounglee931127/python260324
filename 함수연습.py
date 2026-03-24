#1)함수를 정의
def setValue(newValue):
    #지역변수
    x=newValue
    print("함수내부 : ",x)

#2)함수호출
retValue = setValue(3)
print(retValue)

#3)함수정의
def swap(x,y):
    return y,x

#4)함수호출
print(swap(3,4))

#함수내부에서 이름 해석 규칙(LGB)
x=5 #전역변수
def func(a):
    return a+x

#호출
print(func(1))

def func2(a):
    x=10 #지역변수
    return a+x

#호출
print(func2(1))

#함수의 기본값
def times(a=10, b=20):
    return a*b

#호출
print(times())
print(times(5))
print(times(5,6))

def connectURI(server, port):
    strURL = "https://"+server+":"+port
    return strURL

print(connectURI("naver.com","80"))
print(connectURI(port="8080", server="multi.com"))

#가변인자
def union(*ar):
    #지역변수
    result = []
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)
    return result

print(union("HAM","EGG"))
print(union("HAM","EGG","SPAM"))

#람다함수 정의
g= lambda x,y:x*y
print(g(3,4))
print(g(5,6))
print((lambda x:x*x)(3))
print(dir())
print(globals())