import json
import sys

data = json.loads(sys.stdin.readline())
q = int(sys.stdin.readline())

for _ in range(q):
    s = sys.stdin.readline().strip()
    cur = data
    try:
        i = 0
        while i < len(s):
            if s[i] == '.':
                i += 1
            elif s[i] == '[':
                j = s.find(']', i)
                idx = int(s[i+1:j])
                cur = cur[idx]
                i = j + 1
            else:
                j = i
                while j < len(s) and s[j] not in '.[':
                    j += 1
                key = s[i:j]
                cur = cur[key]
                i = j
        print(json.dumps(cur, separators=(',', ':')))
    except:
        print("NOT_FOUND")