from setuptools import setup

setup(
    name="CopyrightArmor",
    version="0.0.1",
    author="Copy05",
    description="A tool that scans the web for pirated content",
    url="https://github.com/Copy05/CopyrightArmor/",
    install_requires=[
        "beautifulsoup4",
        "requests",
        "colorama",
        "selenium",
        "webdriver-manager"
    ],
)