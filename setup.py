from setuptools import setup, find_packages

requirements = [
]

setup(
    name='hlcpy',
    version='0.0.1',
    url='https://github.com/konradmalik/hlcpy.git',
    author='Konrad Malik',
    author_email='konrad.malik@gmail.com',
    description="Hybrid Logical Clock in Python",
    packages=find_packages(),
    install_requires=requirements,
)
