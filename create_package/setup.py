from setuptools import setup


with open("README.md","r") as fh:
    long_description = fh.read()
setup(
    name='helloworld',
    version='0.0.1',
    description='Say hello!',
    py_modules=["helloworld"],
    package_dir={'':'src'},
    install_requires = ["numpy >= 1.10.2"],
    extras_require={"dev":["pytest>=3.7",],},
    classifiers =[
        "Programming Language :: Python :: 3"
    ]
)