from setuptools import find_packages
from setuptools import setup

setup(
    name="revBingGPT",
    version="0.0.1",
    license="GNU General Public License v2.0",
    author="Antonio Cheong",
    author_email="acheong@student.dalat.org",
    description="Reverse engineered Bing Chat API",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/acheong08/BingGPT",
    install_requires=["asyncio", "requests", "websockets"],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["BingGPT"],
)
