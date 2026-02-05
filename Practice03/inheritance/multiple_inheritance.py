class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def info(self):
        print("Name:", self.firstname, self.lastname)


class Athlete:
    def __init__(self, sport):
        self.sport = sport

    def info(self):
        print("Sport:", self.sport)


class Student(Person, Athlete):
    def __init__(self, fname, lname, sport, year):
        Person.__init__(self, fname, lname)
        Athlete.__init__(self, sport)
        self.graduationyear = year

    def info(self):
        print(
            self.firstname,
            self.lastname,
            "| Sport:", self.sport,
            "| Graduation year:", self.graduationyear
        )


x = Student("Mike", "Olsen", "Football", 2019)
x.info()
