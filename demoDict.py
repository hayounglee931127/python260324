# demoDict.py

# 형식변환
a={1,2,3}
b=tuple(a)
print(b)
c=list(b)
c.append(4)
print(c)

#딕셔너리 형식 연습
color  = {"apple" : "red", "grape" : "purple"}
print(color)
print(len(color))

color["lemon"] ="yellow"
print(color["grape"])
del color["apple"]
print(color)

for item in color.items():
    print(item)