from setuptools import setup

setup(
    name="yunomi",
    version="0.2.2",
    description="A Python metrics library with rate, statistical distribution, and timing information.",
    author="richzeng",
    author_email="richie.zeng@rackspace.com",
    url="https://github.com/richzeng/yunomi",
    packages=["yunomi", "yunomi.core", "yunomi.stats"],
    install_requires=["unittest2"]
)
