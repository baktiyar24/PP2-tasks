g = 0
n = 0

def outer(commands):
    global g
    n = 0
    def inner():
        nonlocal n
        for cmd, val in commands:
            if cmd == "global":
                global g
                g += val
            elif cmd == "nonlocal":
                n += val
            elif cmd == "local":
                x = val
    inner()
    return n

commands = []
for _ in range(int(input())):
    s, v = input().split()
    commands.append((s, int(v)))

n = outer(commands)
print(g, n)