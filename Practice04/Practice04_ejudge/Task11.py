import json
import sys

def patch(src, p):
    for k in p:
        if p[k] is None:
            if k in src:
                del src[k]
        elif k in src and isinstance(src[k], dict) and isinstance(p[k], dict):
            patch(src[k], p[k])
        else:
            src[k] = p[k]
    return src

src = json.loads(sys.stdin.readline())
p = json.loads(sys.stdin.readline())

result = patch(src, p)
print(json.dumps(result, separators=(',', ':'), sort_keys=True))