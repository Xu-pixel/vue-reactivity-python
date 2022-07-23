from dataclasses import dataclass

bucket = set()
activeEffect  = None

def effect(fn):
    global activeEffect
    activeEffect = fn
    fn()


class Proxy(dict):
    def __init__(self,target) -> None:
        self['target'] = target
    
    def __setattr__(self, __name: str, __value) -> None:
        setattr(self['target'],__name,__value)
        for fn in bucket:
            fn()

    def __getattribute__(self, __name: str):
        if activeEffect: bucket.add(activeEffect)
        return getattr(self['target'],__name)



if __name__ == '__main__':
    @dataclass
    class Person:
        name:str
        age:int

    data = Person('wei',21)

    obj = Proxy(data)
    print(obj)
    def fn():
        print(obj)
    effect(fn)