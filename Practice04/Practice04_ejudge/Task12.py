import json
import sys

def diff(a, b, path=""):
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())
        for k in keys:
            new_path = f"{path}.{k}" if path else k
            if k not in a:
                diffs.append((new_path, "<missing>", json.dumps(b[k], separators=(',', ':'))))
            elif k not in b:
                diffs.append((new_path, json.dumps(a[k], separators=(',', ':')), "<missing>"))
            else:
                diffs.extend(diff(a[k], b[k], new_path))
    else:
        if a != b:
            diffs.append((path, json.dumps(a, separators=(',', ':')), json.dumps(b, separators=(',', ':'))))
    return diffs

a = json.loads(sys.stdin.readline())
b = json.loads(sys.stdin.readline())

result = diff(a, b)
if not result:
    print("No differences")
else:
    for path, old, new in sorted(result):
        print(f"{path} : {old} -> {new}")