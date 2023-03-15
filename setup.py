from setuptools import find_packages
from setuptools import setup

setup(
    name="EdgeGPT",
    version="0.0.56.1",
    license="GNU General Public License v2.0",
    author="Antonio Cheong",
    author_email="acheong@student.dalat.org",
    description="Reverse engineered Edge Chat API",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/acheong08/EdgeGPT",
    project_urls={"Bug Report": "https://github.com/acheong08/EdgeGPT/issues/new"},
    install_requires=["asyncio", "httpx", "aiohttp"],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["EdgeGPT"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
