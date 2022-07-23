# 仿制VUE reactivity
目前仅支持自定义类和字符串、数字，无法监听数组等的变化，需要大佬帮助。

## Usage 
```python
from reactivity import *
```
### ref

```python
effect(lambda: (print(v.value)))
v = ref(0)
v.value += 1 # 会自动触发注册的effect函数 
```

### reactive
```python
@dataclass
class Person:
    name: str
    age: int

effect(lambda: (print(obj.name) if obj.age else None))
obj = reactive(Person('wei', 21))
obj.name = 'waa' # 会自动触发注册的effect函数 
```

### computed
```python
v = ref(0)
# effect(lambda: (print(v.value)))
v.value += 1
ok = ref(0)
a = computed(lambda: v.value + 1 if ok.value else 999)
v.value += 1
v.value += 1
ok.value = 1
print(a.value)

#当ok.value被切换成1时,a.value会被自动更新成v.value + 1 而第1 、 2次v.value++都不会改变a.value的值。
```

## 参考

https://www.vuemastery.com/courses/vue-3-reactivity/vue3-reactivity

https://www.vuemastery.com/courses/vue3-deep-dive-with-evan-you/vue3-overview/

[Vuejs设计与实现](https://www.ituring.com.cn/book/2953)

https://github.com/cuixiaorui/mini-vue/tree/master/packages/reactivity/src
