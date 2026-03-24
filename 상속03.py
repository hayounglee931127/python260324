# 이 파일은 사람, 관리자, 직원을 나타내는 코드를 가지고 있어요.
# 사람 틀을 만들고, 그 틀을 상속받아 관리자와 직원 틀을 만들어요.

# 사람 틀을 정의해요. 이 틀은 사람의 정보를 가지고 있어요.
class Person:
    # 이건 틀을 만들 때 처음에 하는 일이에요. id와 name을 받아서 저장해요.
    def __init__(self, id, name):
        # id는 사람의 번호예요. 이 번호로 사람을 구분해요.
        self.id = id
        # name은 사람의 이름이에요.
        self.name = name

    # 이건 사람의 정보를 출력하는 방법이에요.
    def printInfo(self):
        # f는 특별한 방법으로 글자를 만들어요. 변수의 값을 넣어서 보여줘요.
        print(f"ID: {self.id}, Name: {self.name}")

# 관리자 틀을 정의해요. 이 틀은 사람 틀을 상속받아요. 그래서 사람의 모든 것을 가지고 있어요.
class Manager(Person):
    # 이건 관리자 틀을 만들 때 처음에 하는 일이에요. 사람의 id, name과 관리자의 title을 받아요.
    def __init__(self, id, name, title):
        # 부모 틀(사람 틀)의 __init__을 불러요. id와 name을 저장해요.
        super().__init__(id, name)
        # title은 관리자의 직책이에요. 예를 들어 "팀장" 같은 거예요.
        self.title = title

    # 이건 관리자의 정보를 출력하는 방법이에요. 사람의 정보도 같이 출력해요.
    def printInfo(self):
        # 부모 틀의 printInfo를 불러요. 사람의 정보를 출력해요.
        super().printInfo()
        # 관리자의 모든 정보를 출력해요.
        print(f"ID: {self.id}, Name: {self.name}, Title: {self.title}")

# 직원 틀을 정의해요. 이 틀은 사람 틀을 상속받아요. 그래서 사람의 모든 것을 가지고 있어요.
class Employee(Person):
    # 이건 직원 틀을 만들 때 처음에 하는 일이에요. 사람의 id, name과 직원의 skill을 받아요.
    def __init__(self, id, name, skill):
        # 부모 틀(사람 틀)의 __init__을 불러요. id와 name을 저장해요.
        super().__init__(id, name)
        # skill은 직원의 재주나 능력이에요. 예를 들어 "컴퓨터 프로그래밍" 같은 거예요.
        self.skill = skill

    # 이건 직원의 정보를 출력하는 방법이에요. 사람의 정보도 같이 출력해요.
    def printInfo(self):
        # 부모 틀의 printInfo를 불러요. 사람의 정보를 출력해요.
        super().printInfo()
        # 직원의 모든 정보를 출력해요.
        print(f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}")

# 이 아래는 테스트 코드예요. 틀들이 제대로 작동하는지 확인해요.
if __name__ == "__main__":
    # 사람 틀을 테스트해요.
    # 첫 번째 사람을 만들어요. id는 1, 이름은 Alice예요.
    person1 = Person(1, "Alice")
    # 사람의 정보를 출력해요.
    person1.printInfo()
    # 빈 줄을 출력해요. 보기 좋게 하기 위해서예요.
    print()

    # 두 번째 사람을 만들어요. id는 2, 이름은 Bob이에요.
    person2 = Person(2, "Bob")
    # 사람의 정보를 출력해요.
    person2.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 관리자 틀을 테스트해요.
    # 첫 번째 관리자를 만들어요. id는 3, 이름은 Charlie, 직책은 Senior Manager예요.
    manager1 = Manager(3, "Charlie", "Senior Manager")
    # 관리자의 정보를 출력해요.
    manager1.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 두 번째 관리자를 만들어요. id는 4, 이름은 Diana, 직책은 Project Manager예요.
    manager2 = Manager(4, "Diana", "Project Manager")
    # 관리자의 정보를 출력해요.
    manager2.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 직원 틀을 테스트해요.
    # 첫 번째 직원을 만들어요. id는 5, 이름은 Eve, 재주는 Python Programming이에요.
    employee1 = Employee(5, "Eve", "Python Programming")
    # 직원의 정보를 출력해요.
    employee1.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 두 번째 직원을 만들어요. id는 6, 이름은 Frank, 재주는 Data Analysis이에요.
    employee2 = Employee(6, "Frank", "Data Analysis")
    # 직원의 정보를 출력해요.
    employee2.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 더 많은 테스트를 해요. 다양한 사람, 관리자, 직원을 만들어요.
    # 세 번째 사람을 만들어요. id는 7, 이름은 Grace예요.
    person3 = Person(7, "Grace")
    # 사람의 정보를 출력해요.
    person3.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 세 번째 관리자를 만들어요. id는 8, 이름은 Henry, 직책은 Team Lead예요.
    manager3 = Manager(8, "Henry", "Team Lead")
    # 관리자의 정보를 출력해요.
    manager3.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 세 번째 직원을 만들어요. id는 9, 이름은 Ivy, 재주는 Machine Learning이에요.
    employee3 = Employee(9, "Ivy", "Machine Learning")
    # 직원의 정보를 출력해요.
    employee3.printInfo()
    # 빈 줄을 출력해요.
    print()

    # 네 번째 직원을 만들어요. id는 10, 이름은 Jack, 재주는 Web Development이에요.
    employee4 = Employee(10, "Jack", "Web Development")
    # 직원의 정보를 출력해요.
    employee4.printInfo()
    # 빈 줄을 출력해요.
    print()
