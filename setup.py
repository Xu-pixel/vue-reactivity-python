from setuptools import setup
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name='reactivity',
    version='0.0.1',
    py_modules=['reactivity'],
    description='a python vesion vue/reactivity api',
    long_description=README,
    url='https://gitee.com/Xu-pixel/vue-reactivity-python',
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    install_requires=[]
)

# 新版本先清理dist
# rm -r -fo dist