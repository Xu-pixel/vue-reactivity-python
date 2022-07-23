from collections import defaultdict
from dataclasses import dataclass


b = defaultdict(lambda:defaultdict(set))
@dataclass
class Person:
    name:str

c = Person('c')
d = c
print(id(c))
print(id(d))
print(b[id(c)]['b'])
c.name = 'wei'
print(id(c))

def a():
    pass

print(b[a])
del b[a]
print(b[a])

