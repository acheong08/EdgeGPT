from setuptools import find_packages
from setuptools import setup

setup(
    name="EdgeGPT",
    version="0.1.11",
    license="GNU General Public License v2.0",
    author="Antonio Cheong",
    author_email="acheong@student.dalat.org",
    description="Reverse engineered Edge Chat API",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/acheong08/EdgeGPT",
    project_urls={"Bug Report": "https://github.com/acheong08/EdgeGPT/issues/new"},
    install_requires=[
        "httpx",
        "websockets",
        "rich",
        "certifi",
        "prompt_toolkit",
        "regex",
        "requests",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["EdgeGPT", "ImageGen"],
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
