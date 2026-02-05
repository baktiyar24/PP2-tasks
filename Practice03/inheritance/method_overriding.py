class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def info(self):
        print(self.firstname, self.lastname)

class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year

    # method overriding
    def info(self):
        print(self.firstname, self.lastname, "Graduation year:", self.graduationyear)

x = Student("Mike", "Olsen", 2019)
x.info()
