a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
b = range(10)
c = list(range(10))

print(len(a), a)
print(len(b), b)
print(len(c), c)

print(b, [*b])

tmp = []
for x in a:
  print(x * 2)
  tmp.append(x * 2)
#a = tmp
print(tmp)

print([x*2 for x in a])
print([x for x in a if x >= 5])
print([x for x in a if x % 2 == 0])

d = {"a": 1, "test": 2}

print(len(d), d)
print(d.items())
print({k:v for k,v in d.items()})

for k,v in d.items():
  print(f"{k=} {v=}")

print([v * 2 for v in d.values()])
print([x + 1 for x in [y * 2 for y in range(10)]])

e = "abcdef"
print(e)

from collections import defaultdict

dd = defaultdict(list)
dd["abc"].append(42)
dd["abc"].append(69)
print(dd)