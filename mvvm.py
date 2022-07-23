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
    if not activeEffect:
        return
    deps = bucket[id(target)][key]
    deps.add(activeEffect)
    effect2deps[activeEffect].append(deps)


def trigger(target, key):
    effects = bucket[id(target)][key]
    effectsToRun = {effect for effect in effects if effect != activeEffect}
    for effect in effectsToRun:
        effect()


def cleanup(effectFn):
    for deps in effect2deps[effectFn]:
        deps.remove(effectFn)
    del effect2deps[effectFn]


def ref(raw=0):
    @dataclass
    class R:
        value: object

    return Proxy(R(raw))


def reactive(raw):
    return Proxy(raw)


def computed(getter):
    result = ref()
    def fn(): result.value = getter()
    effect(fn)
    return result


if __name__ == '__main__':
    @dataclass
    class Person:
        name: str
        age: int

    obj = Proxy(Person('wei', 21))
    effect(lambda: (print(obj.name) if obj.age else None))
    obj.age = 0
    obj.age = 1
    obj.age = 0
    obj.age = 0
    obj.age = 0

    v = ref(0)
    effect(lambda: (print(v.value)))
    v.value += 1

    a = computed(lambda: v.value + 1)
    v.value += 1
    print(a.value)
