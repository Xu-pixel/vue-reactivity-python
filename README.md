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

## 参考

https://www.vuemastery.com/courses/vue3-deep-dive-with-evan-you/vue3-overview/

https://www.vuemastery.com/courses/vue-3-reactivity/vue3-reactivity

[Vuejs设计与实现](https://www.ituring.com.cn/book/2953)

https://github.com/cuixiaorui/mini-vue/tree/master/packages/reactivity/src
