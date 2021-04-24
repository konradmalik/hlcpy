import pathlib
from setuptools import setup, find_packages

__version__ = "0.0.2"
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

requirements = [
    "iso8601 >= 0.1.14",
]

setup(
    name="hlcpy",
    version=__version__,
    url="https://github.com/konradmalik/hlcpy.git",
    author="Konrad Malik",
    author_email="konrad.malik@gmail.com",
    license="MIT",
    description="Hybrid Logical Clock in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
