from collections import defaultdict
from dataclasses import dataclass

bucket = defaultdict(lambda: defaultdict(set))
activeEffect = None
effect2deps = defaultdict(list)  # list存放与副作用相关的依赖集合


class Proxy(dict):
    def __init__(self, target) -> None:
        self['target'] = target

    def __setattr__(self, __name: str, __value) -> None:
        setattr(self['target'], __name, __value)
        trigger(self['target'], __name)

    def __getattribute__(self, __name: str):
        track(self['target'], __name)
        return getattr(self['target'], __name)


def effect(fn):
    def effectFn():
        global activeEffect
        cleanup(effectFn)
        activeEffect = effectFn
        fn()
        activeEffect = None

    effectFn()


def track(target, key):
    if len(key) >= 2 and key[:2] == '__':
        return  # 内置变量不要追踪

    deps = bucket[id(target)][key]
    deps.add(activeEffect)
    effect2deps[activeEffect].append(deps)


def trigger(target, key):
    if len(key) >= 2 and key[:2] == '__':
        return
    effects = bucket[id(target)][key]
    effectsToRun = {effect for effect in effects if effect != activeEffect}
    for effect in effectsToRun:
        effect()


def cleanup(effectFn):
    for deps in effect2deps[effectFn]:
        deps.remove(effectFn)
    del effect2deps[effectFn]


if __name__ == '__main__':
    @dataclass
    class Person:
        name: str
        age: int


    data = Person('wei', 21)
    obj = Proxy(data)
    effect(lambda: (print(obj.name) if obj.age else None))
    obj.age = 0
    obj.age = 1
    obj.age = 0
    obj.age = 0
    obj.age = 0
