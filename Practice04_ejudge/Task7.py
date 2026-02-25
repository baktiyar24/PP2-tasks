class Reverse:
    def __init__(self,word):
        self.word = word
        self.index = len(word) - 1

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < 0:
            raise StopIteration
        char = self.word[self.index]
        self.index -= 1
        return char
    
S = input()
ob = Reverse(S)
for x in ob:
    print(x, end="")


        